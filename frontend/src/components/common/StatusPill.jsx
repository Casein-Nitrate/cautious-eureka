import { STATUS } from '../../utils/constants.js';

export default function StatusPill({ status }) {
  const s = STATUS[status] || STATUS.not_raised;
  return <span className="pill" style={{ '--c': s.color }}><i />{s.label}</span>;
}
