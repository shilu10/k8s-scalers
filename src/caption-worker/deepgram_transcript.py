import asyncio
import aiohttp
import json
import os
import wave
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from logger import setup_rotating_logger

_logger = setup_rotating_logger()

async def download_audio_to_temp_file(s3_url: str) -> str:
    _logger.info("⬇️ Downloading audio from S3 pre-signed URL: %s", s3_url)

    async with aiohttp.ClientSession() as session:
        async with session.get(s3_url) as resp:
            if resp.status != 200:
                _logger.warning("❌ Failed to download audio: %s", resp.status)
                raise Exception(f"Failed to download audio: {resp.status}")

            total_size = int(resp.headers.get("Content-Length", 0))
            downloaded = 0

            with NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input_file:
                while True:
                    chunk = await resp.content.read(1024 * 32)
                    if not chunk:
                        break
                    tmp_input_file.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"Download progress: {percent:.2f}%", end="\r")
                input_path = tmp_input_file.name

    print("\n✅ Download complete: ", input_path)

    # Convert to WAV using pydub
    _logger.info("🎧 Converting MP4 to WAV...")
    audio = AudioSegment.from_file(input_path)
    output_path = input_path.replace(".mp4", ".wav")
    audio.export(output_path, format="wav")

    _logger.info("✅ Conversion complete: %s", output_path)
    return output_path


def get_audio_duration(file_path: str) -> float:
    """Return duration of WAV file in seconds using wave module."""
    with wave.open(file_path, "rb") as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()
        return frames / float(rate)


async def stream_audio(ws, file_path: str):
    """Stream audio data over WebSocket to Deepgram."""
    with open(file_path, "rb") as audio:
        while chunk := audio.read(1024):
            await ws.send_bytes(chunk)
            await asyncio.sleep(0.01)  # Throttle to simulate real-time
    await ws.send_str(json.dumps({"type": "CloseStream"}))
    _logger.info("📤 Finished streaming audio: %s", file_path)


async def receive_transcript(ws, total_duration: float, job_id: str, redis_client):
    """Receive and log transcript with progress updates."""
    last_processed = 0.0
    last_percentage = 0
    transcript = []

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            response = json.loads(msg.data)
            try:
                alt = response["channel"]["alternatives"][0]
                if "transcript" in alt and alt["transcript"].strip() != "":
                    transcript.append(alt["transcript"])

                words = alt.get("words", [])
                if words:
                    end_time = words[-1]["end"]
                    if end_time > last_processed:
                        last_processed = end_time
                        percentage = int((last_processed / total_duration) * 100)
                        if percentage > last_percentage:
                            last_percentage = percentage
                            redis_client.set(job_id, percentage)
                            redis_client.publish("my_channel", percentage)
                            _logger.info(f"⏳ {percentage}% processed ({last_processed:.2f}s / {total_duration:.2f}s)")
            except (KeyError, IndexError):
                continue

    with open("transcript.txt", "w") as f:
        f.write(" ".join(transcript))
    _logger.info("✅ Transcript saved to transcript.txt")


async def stream_from_s3(s3_url: str, deepgram_api_key: str, deepgram_ws_url: str, job_id: str, redis_client):
    """Main orchestration function: S3 download -> WAV convert -> stream to Deepgram."""
    # Step 1: Download and convert
    audio_path = await download_audio_to_temp_file(s3_url)

    # Step 2: Get duration
    duration = get_audio_duration(audio_path)
    _logger.info("🎧 Audio duration: %.2f seconds", duration)

    # Step 3: Connect and stream
    session_headers = {"Authorization": f"Token {deepgram_api_key}"}

    async with aiohttp.ClientSession(headers=session_headers) as session:
        async with session.ws_connect(deepgram_ws_url) as ws:
            _logger.info("✅ Connected to Deepgram WebSocket for job %s", job_id)
            await asyncio.gather(
                stream_audio(ws, audio_path),
                receive_transcript(ws, duration, job_id, redis_client)
            )

    os.remove(audio_path)
    _logger.info("🗑️ Temporary audio file deleted: %s", audio_path)
