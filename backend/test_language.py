import asyncio
import httpx
from app.main import app

async def test():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        # Test 1: same-language shortcut
        r = await c.post("/api/internal/language/translate", json={
            "text": "hello",
            "source_lang": "en",
            "target_lang": "en"
        })
        print(f"Translate same-lang: {r.status_code} {r.json()}")
        assert r.status_code == 200
        assert r.json()["translated_text"] == "hello"
        assert r.json()["detected_lang"] == "en"

        # Test 2: translate with bad API key → graceful fallback
        r2 = await c.post("/api/internal/language/translate", json={
            "text": "namaste",
            "source_lang": "hi",
            "target_lang": "en"
        })
        print(f"Translate fallback: {r2.status_code} {r2.json()}")
        assert r2.status_code == 200
        assert r2.json()["translated_text"] == "namaste"  # returned unchanged

        # Test 3: TTS with bad API key → graceful fallback
        r3 = await c.post("/api/internal/language/tts", json={
            "text": "test",
            "language": "en"
        })
        print(f"TTS fallback: {r3.status_code} {r3.json()}")
        assert r3.status_code == 200
        assert r3.json()["audio_base64"] == ""
        assert r3.json()["format"] == "mp3"

    print("\nAll language endpoint tests PASSED!")

asyncio.run(test())
