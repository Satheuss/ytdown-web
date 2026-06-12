import re


def is_valid_youtube_url(url: str) -> bool:
    """Valida se a URL informada é um link válido do YouTube
    (vídeo, shorts ou playlist)."""
    patterns = [
        r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w\-]+",
        r"(https?://)?(www\.)?youtube\.com/shorts/[\w\-]+",
        r"(https?://)?(www\.)?youtube\.com/playlist\?list=[\w\-]+",
    ]
    return any(re.search(p, url) for p in patterns)
