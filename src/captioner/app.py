import asyncio
import aiohttp
import json
import os
import wave
from pydub.utils import mediainfo
from tempfile import NamedTemporaryFile


DEEPGRAM_API_KEY = "229541dc15db454678a9f6bc22b126f66f4d9657"
S3_PRESIGNED_URL  = "https://stress-app-video-bucket-example.s3.us-east-1.amazonaws.com/harvard.wav?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCtOuYbsm6zegH9pobCo8SqCTa%2FpV8zfQIz8Oq0ACJppgIhALYGxOfhXwqvsHPDCDZC0irr73HkJSqvGSKVASZvN%2B%2F%2FKrkDCDoQABoMNTMzMjY3NDUzNzUxIgynAdTBVe994KYRE5wqlgMwOH2t5VHSPLYdPDs6srREo5LeWxzHY%2BlYlZLKYY8gCH0ENMOP1QOj8b56jpSOd86spQjdtiUJoZe1QBs5vFuSs0ohvcYjHYTX%2B8Zd3XLydzvnza8cdMCeo%2BKTVB%2F%2FqZPiC4L8Bi4Knv1TVeIi3aEQ0f6nBE0mZtmcpU%2FqDzGl%2FPSL71oSem%2Fk0XhXcFAGumlRVWMT9WDS4uXHz8osW8b%2Bz3BCOPuNL7N%2BqBW9SPFUmaMVZdPfl18DeeAyHJZIk8PNBTjufGBrQMY08G6lDvUzGaR%2BJSm979ciOks9jlXO3GkMnq6Wt%2B0lRZ2GkJN%2B%2FRTBDdiZBlqDcOWgvUk7w7S%2Bs%2BY2QegacuGzDhe3Qbb3mMZI75PvRIt9Z%2BgB0lWEeA0RdY5fp%2FYSHKpvEMPWliGZE0%2BgF6U5gmsfpvseHC1OrC7OT0bHYppKPvRADd0PtgsJQsKior%2FN6GQO%2BhejcaDMZ2a6HDTWaoID5l514mOx9OOC4U%2FAmF3rlLyZSY7kC0owT%2FU542dXO3JumKKcVAnwQEiOQGJiMJ3F5cAGOt0CSWWm4UNzLziREJ7ZOR3PDq2GekYzb%2BBdWrB8z2MakN8zKfuvRNW0aLs2m40auDnOiWO9FOMiBwuWx8uYZb5cRlRFP0kj0ebsEVpR7Uh6%2B32IOmCJOZbFgWP42%2BII0Be8Ntd18I7gdyBCsLGh81WcZFBbKdAUA%2F1JJnDBNtNiShZfLnB360xs3WYhGKfZAqIEo9GsTKXep6fOQ%2FL2HeMXGsiHJPDaWj53mSij2V4ezLxfl7BZAwxFETkggmnOqb6Opy7XvrOcyXMsysQH6c80VszFoGjyOwyGWmOw1BC5gwIN46k6ZoLkLD95pbzwgf%2FT92LD8J063D3UX0Lsr5Nij45CgjMbiwXg5zMdg5fcKNYPUYLvJbBosgG%2BTSjTNc9acsIW6wNK0F650SgzR0fJ3X9zv3EkfL8WfetrMjIlsbu%2BdMqWf8F2BYH74Z3hpsdoYoJWGEAAW9m%2B3D%2BERA%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAXYKJXS432KMLTPJ3%2F20250506%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250506T011716Z&X-Amz-Expires=3000&X-Amz-SignedHeaders=host&X-Amz-Signature=ce9ae79fbbba18621ee80ddaf3afaaf655f6b37a5fc448d5935a8126069b07b4"
DEEPGRAM_WS_URL = "wss://api.deepgram.com/v1/listen?punctuate=true"


async def download_audio_to_temp_file():
    """Download the S3 audio file to a temporary WAV file."""
    print("⬇️ Downloading audio from S3 pre-signed URL...")
    async with aiohttp.ClientSession() as session:
        async with session.get(S3_PRESIGNED_URL) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to download audio: {resp.status}")
            with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    tmp_file.write(chunk)
                return tmp_file.name
            

def get_audio_duration(file_path):
    """Use wave module to get duration of WAV file in seconds."""
    with wave.open(file_path, "rb") as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()
        return frames / float(rate)


async def stream_audio(ws, file_path):
    """Stream audio data over WebSocket to Deepgram."""
    with open(file_path, "rb") as audio:
        while chunk := audio.read(1024):
            await ws.send_bytes(chunk)
            await asyncio.sleep(0.01)  # Throttle for realistic streaming
    await ws.send_str(json.dumps({"type": "CloseStream"}))
    print("📤 Finished streaming audio")


async def receive_transcript(ws, total_duration):
    """Receive and print transcript with progress updates."""
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
                            print(f"⏳ {percentage}% processed ({last_processed:.2f}s of {total_duration:.2f}s)")
            except (KeyError, IndexError):
                pass

    with open("transcript.txt", "w") as f:
        f.write(" ".join(transcript))
    print("✅ Transcript saved to transcript.txt")


async def stream_from_s3():
    # Step 1: Download file from S3
    audio_path = await download_audio_to_temp_file()
    
    # Step 2: Get duration
    duration = get_audio_duration(audio_path)
    print(f"🎧 Audio duration: {duration:.2f} seconds")

    # Step 3: Stream to Deepgram via WebSocket
    session_headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}

    async with aiohttp.ClientSession(headers=session_headers) as session:
        async with session.ws_connect(DEEPGRAM_WS_URL) as ws:
            print("✅ Connected to Deepgram WebSocket")
            await asyncio.gather(
                stream_audio(ws, audio_path),
                receive_transcript(ws, duration)
            )

    # Clean up
    os.remove(audio_path)


if __name__ == "__main__":
    asyncio.run(stream_from_s3())
