# Configuration for YouTube Agent System

OLLAMA_MODEL = "mistral"
OLLAMA_BASE_URL = "http://localhost:11434"

# Output paths
OUTPUT_DIR = "D:/youtube-agent/output"
THUMBNAILS_DIR = "D:/youtube-agent/thumbnails"
CAPTIONS_DIR = "D:/youtube-agent/captions"
VOICE_DIR = "D:/youtube-agent/voice_generation"
VIDEO_DIR = "D:/youtube-agent/video_generation"

# Trend sources
RSS_FEEDS = [
    "https://hnrss.org/frontpage",
    "https://www.reddit.com/r/technology/.rss",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
]

# Video settings
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
VIDEO_FPS = 24
FONT_SIZE = 40