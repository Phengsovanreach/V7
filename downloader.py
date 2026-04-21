import yt_dlp
import asyncio


async def download_video(url: str):
    loop = asyncio.get_event_loop()

    def run():
        ydl_opts = {
            "format": "best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info.get("title", "unknown")

    title = await loop.run_in_executor(None, run)

    return f"✅ Downloaded: {title}"