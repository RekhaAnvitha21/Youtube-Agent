import feedparser
import requests
from config.config import OLLAMA_MODEL, OLLAMA_BASE_URL, RSS_FEEDS

def fetch_trending_topics():
    """Fetch trending topics from RSS feeds"""
    topics = []
    
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                topics.append({
                    "title": entry.title,
                    "summary": entry.get("summary", "")[:200]
                })
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}")
    
    return topics

def select_best_topic(topics):
    """Use Mistral to pick the best topic for a YouTube video"""
    
    topic_list = "\n".join([f"- {t['title']}" for t in topics])
    
    prompt = f"""
    You are a YouTube content strategist.
    From this list of trending topics, pick the BEST one for a YouTube video.
    Consider: viewer interest, uniqueness, educational value.
    
    Topics:
    {topic_list}
    
    Respond with ONLY the chosen topic title. Nothing else.
    """
    
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    
    result = response.json()
    return result["response"].strip()

if __name__ == "__main__":
    print("Fetching trending topics...")
    topics = fetch_trending_topics()
    print(f"Found {len(topics)} topics")
    
    print("\nSelecting best topic with AI...")
    best = select_best_topic(topics)
    print(f"\nBest topic: {best}")