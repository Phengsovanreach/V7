from downloader import download_video


async def handle_message(text: str):
    text = text.lower()

    if "http" in text:
        return await download_video(text)

    if "start" in text:
        return "🚀 Welcome to V7 ULTRA PRO Downloader"

    if "help" in text:
        return (
            "📌 Commands:\n"
            "- Send video link\n"
            "- YouTube / TikTok / Facebook supported\n"
        )

    return "❌ Send a valid link or /help"