import requests
import json
from config.config import OLLAMA_MODEL, OLLAMA_BASE_URL

def generate_metadata(topic, script):
    prompt = f"""Give YouTube metadata for: "{topic}"
Reply in JSON only:
{{"title": "short title", "description": "short description", "tags": ["tag1","tag2","tag3"], "hashtags": ["#tag1","#tag2"]}}"""


    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )
    
    result = response.json()
    text = result["response"].strip()
    
    # Extract JSON from response
    start = text.find('{')
    end = text.rfind('}') + 1
    json_str = text[start:end]
    metadata = json.loads(json_str)
    return metadata

if __name__ == "__main__":
    topic = "I spent my whole career building passive income. Here's what I got wrong"
    script = "Sample script about passive income mistakes"
    
    print("Generating metadata...")
    metadata = generate_metadata(topic, script)
    
    print("\n--- METADATA ---")
    print(f"Title: {metadata['title']}")
    print(f"Description: {metadata['description']}")
    print(f"Tags: {', '.join(metadata['tags'])}")
    print(f"Hashtags: {', '.join(metadata['hashtags'])}")