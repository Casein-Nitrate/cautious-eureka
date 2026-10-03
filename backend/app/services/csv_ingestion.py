"""
CSV Ingestion Pipeline for Division 2 - Evidence Repository.
Reads MSDE outcome data from CSV files, validates rows, and stores
evidence in the evidence_repository table with provenance tracking.
"""

import csv
import io
import json
import logging
import re
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.evidence import EvidenceModel

logger = logging.getLogger(__name__)

# Required CSV columns that must exist in the header
REQUIRED_COLUMNS = [
    "evidence_id", "trade", "district", "state", "data_source", "data_period"
]


def _safe_int(value: Optional[str]) -> Optional[int]:
    """Convert string to int, returning None for empty/invalid values."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _safe_str(value: Optional[str]) -> Optional[str]:
    """Return stripped string or None for empty values."""
    if value is None:
        return None
    stripped = str(value).strip()
    return stripped if stripped else None


def _parse_progression_path(value: Optional[str]) -> Optional[list]:
    """Parse progression_path from JSON string, returning None on failure."""
    if value is None or str(value).strip() == "":
        return None
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return parsed
        return None
    except (json.JSONDecodeError, TypeError):
        return None


def _validate_placement_rate(value: Optional[str]) -> Optional[str]:
    """Validate placement_rate format: 'XX%' or NULL."""
    if value is None or str(value).strip() == "":
        return None
    stripped = str(value).strip()
    if re.match(r'^\d+%$', stripped):
        return stripped
    return None  # Invalid format → treat as NULL


class CSVIngestionService:
    """
    Service for validating, parsing, and ingesting MSDE outcome CSV data.
    """

    def __init__(self, required_columns: Optional[list[str]] = None):
        self.required_columns = required_columns or REQUIRED_COLUMNS

    def validate_csv_structure(self, file_obj) -> tuple[bool, list[str]]:
        """Validate that the CSV has the expected headers."""
        try:
            reader = csv.DictReader(file_obj)
            if reader.fieldnames is None:
                return False, ["CSV has no header row"]
            missing = [c for c in self.required_columns if c not in reader.fieldnames]
            if missing:
                return False, [f"CSV missing required columns: {', '.join(missing)}"]
            return True, []
        except Exception as e:
            return False, [f"Failed to read CSV headers: {str(e)}"]

    def parse_csv_content(self, csv_text: str) -> tuple[list[dict], list[str]]:
        """Parse raw CSV string into validated record dicts and error messages."""
        reader = csv.DictReader(io.StringIO(csv_text))
        valid_records = []
        errors = []

        if reader.fieldnames is None:
            return [], ["CSV has no header row"]

        missing = [c for c in self.required_columns if c not in reader.fieldnames]
        if missing:
            return [], [f"CSV missing required columns: {', '.join(missing)}"]

        for row_num, row in enumerate(reader, start=2):
            evidence_id = _safe_str(row.get("evidence_id"))
            trade = _safe_str(row.get("trade"))
            district = _safe_str(row.get("district"))
            state = _safe_str(row.get("state"))
            data_source = _safe_str(row.get("data_source"))
            data_period = _safe_str(row.get("data_period"))

            if not all([evidence_id, trade, district, state, data_source, data_period]):
                errors.append(f"Row {row_num}: missing required field(s)")
                continue

            earnings_min = _safe_int(row.get("earnings_min"))
            earnings_max = _safe_int(row.get("earnings_max"))
            if earnings_min is not None and earnings_max is not None and earnings_min > earnings_max:
                errors.append(f"Row {row_num}: earnings_min ({earnings_min}) > earnings_max ({earnings_max})")
                continue

            placement_rate = _validate_placement_rate(row.get("placement_rate"))
            trainee_quote = _safe_str(row.get("trainee_quote"))
            trainee_quote_source = _safe_str(row.get("trainee_quote_source"))
            if trainee_quote and not trainee_quote_source:
                trainee_quote = None

            valid_records.append({
                "evidence_id": evidence_id,
                "trade": trade,
                "district": district,
                "state": state,
                "data_source": data_source,
                "data_period": data_period,
                "placement_rate": placement_rate,
                "earnings_min": earnings_min,
                "earnings_max": earnings_max,
                "currency": _safe_str(row.get("currency")) or "INR",
                "nsqf_level": _safe_str(row.get("nsqf_level")),
                "progression_path": _parse_progression_path(row.get("progression_path")),
                "physical_demand": _safe_str(row.get("physical_demand")),
                "typical_day": _safe_str(row.get("typical_day")),
                "trainee_quote": trainee_quote,
                "trainee_quote_source": trainee_quote_source,
                "female_enrollment_pct": _safe_str(row.get("female_enrollment_pct")),
                "safety_infrastructure": _safe_str(row.get("safety_infrastructure")),
            })

        return valid_records, errors


async def ingest_csv(
    file_path: str,
    db: AsyncSession
) -> tuple[int, int, list[str]]:
    """
    Ingest MSDE outcome data from a CSV file into the evidence_repository.

    Args:
        file_path: Path to the CSV file.
        db: Async database session.

    Returns:
        Tuple of (success_count, error_count, error_messages).
    """
    success_count = 0
    error_count = 0
    error_messages: list[str] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Property 3: Validate required columns exist
            if reader.fieldnames is None:
                msg = f"CSV file '{file_path}' has no header row"
                logger.error(msg)
                return 0, 1, [msg]

            missing_cols = [
                col for col in REQUIRED_COLUMNS
                if col not in reader.fieldnames
            ]
            if missing_cols:
                msg = f"CSV missing required columns: {', '.join(missing_cols)}"
                logger.error(msg)
                return 0, 1, [msg]

            for row_num, row in enumerate(reader, start=2):  # Row 1 is header
                try:
                    # Extract and validate required fields
                    evidence_id = _safe_str(row.get("evidence_id"))
                    trade = _safe_str(row.get("trade"))
                    district = _safe_str(row.get("district"))
                    state = _safe_str(row.get("state"))
                    data_source = _safe_str(row.get("data_source"))
                    data_period = _safe_str(row.get("data_period"))

                    if not all([evidence_id, trade, district, state, data_source, data_period]):
                        msg = f"Row {row_num}: missing required field(s)"
                        error_messages.append(msg)
                        error_count += 1
                        logger.warning(msg)
                        continue

                    # Parse optional fields
                    earnings_min = _safe_int(row.get("earnings_min"))
                    earnings_max = _safe_int(row.get("earnings_max"))

                    # Property 4: Validate earnings range
                    if (earnings_min is not None and earnings_max is not None
                            and earnings_min > earnings_max):
                        msg = f"Row {row_num}: earnings_min ({earnings_min}) > earnings_max ({earnings_max}), swapping"
                        logger.warning(msg)
                        earnings_min, earnings_max = earnings_max, earnings_min

                    placement_rate = _validate_placement_rate(row.get("placement_rate"))
                    if row.get("placement_rate") and placement_rate is None:
                        logger.warning(
                            f"Row {row_num}: invalid placement_rate format "
                            f"'{row.get('placement_rate')}', set to NULL"
                        )

                    # Parse progression_path
                    progression_path = _parse_progression_path(row.get("progression_path"))

                    # Property 2: Validate trainee quote provenance
                    trainee_quote = _safe_str(row.get("trainee_quote"))
                    trainee_quote_source = _safe_str(row.get("trainee_quote_source"))
                    if trainee_quote and not trainee_quote_source:
                        logger.warning(
                            f"Row {row_num}: trainee_quote without source for "
                            f"evidence_id '{evidence_id}', setting quote to NULL"
                        )
                        trainee_quote = None

                    # Build embedding text representation
                    embedding_parts = [f"Trade: {trade}", f"Location: {district}, {state}"]
                    if placement_rate:
                        embedding_parts.append(f"Placement Rate: {placement_rate}")
                    if earnings_min is not None and earnings_max is not None:
                        currency = _safe_str(row.get("currency")) or "INR"
                        embedding_parts.append(
                            f"Earnings: {earnings_min}-{earnings_max} {currency}"
                        )
                    nsqf_level = _safe_str(row.get("nsqf_level"))
                    if nsqf_level:
                        embedding_parts.append(f"NSQF Level: {nsqf_level}")
                    physical_demand = _safe_str(row.get("physical_demand"))
                    if physical_demand:
                        embedding_parts.append(f"Physical Demand: {physical_demand}")
                    typical_day = _safe_str(row.get("typical_day"))
                    if typical_day:
                        embedding_parts.append(f"Typical Day: {typical_day}")
                    if trainee_quote:
                        embedding_parts.append(f"Trainee Experience: {trainee_quote}")

                    embedding_text = "\n".join(embedding_parts)

                    # Check for duplicate evidence_id
                    existing = await db.execute(
                        select(EvidenceModel.evidence_id).where(
                            EvidenceModel.evidence_id == evidence_id
                        )
                    )
                    if existing.scalar_one_or_none() is not None:
                        msg = f"Row {row_num}: duplicate evidence_id '{evidence_id}', skipping"
                        error_messages.append(msg)
                        error_count += 1
                        logger.warning(msg)
                        continue

                    # Create ORM model instance
                    evidence_record = EvidenceModel(
                        evidence_id=evidence_id,
                        trade=trade,
                        district=district,
                        state=state,
                        data_source=data_source,
                        data_period=data_period,
                        placement_rate=placement_rate,
                        earnings_min=earnings_min,
                        earnings_max=earnings_max,
                        currency=_safe_str(row.get("currency")) or "INR",
                        nsqf_level=nsqf_level,
                        progression_path=progression_path,
                        physical_demand=physical_demand,
                        typical_day=typical_day,
                        trainee_quote=trainee_quote,
                        trainee_quote_source=trainee_quote_source,
                        female_enrollment_pct=_safe_str(row.get("female_enrollment_pct")),
                        safety_infrastructure=_safe_str(row.get("safety_infrastructure")),
                        embedding_text=embedding_text,
                    )

                    db.add(evidence_record)
                    success_count += 1

                except Exception as e:
                    msg = f"Row {row_num}: {str(e)}"
                    error_messages.append(msg)
                    error_count += 1
                    logger.error(msg)

            # Commit all successful rows
            if success_count > 0:
                await db.commit()

    except FileNotFoundError:
        msg = f"CSV file not found: {file_path}"
        logger.error(msg)
        return 0, 1, [msg]
    except Exception as e:
        msg = f"CSV ingestion failed: {str(e)}"
        logger.error(msg)
        await db.rollback()
        return 0, 1, [msg]

    logger.info(
        f"CSV ingestion complete: {success_count} succeeded, "
        f"{error_count} errors from '{file_path}'"
    )
    return success_count, error_count, error_messages
