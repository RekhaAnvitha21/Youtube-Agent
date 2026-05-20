import requests
from config.config import OLLAMA_MODEL, OLLAMA_BASE_URL

def generate_script(topic):
    """Generate a YouTube script for the given topic"""
    
    prompt = f"""Write a short YouTube script for: "{topic}"
    Include: hook, main points, call to action.
    Keep it under 200 words."""
    
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
    return result["response"].strip()

if __name__ == "__main__":
    topic = "I spent my whole career building passive income. Here's what I got wrong"
    print("Generating script... (may take 2-3 minutes on CPU)")
    script = generate_script(topic)
    print("\n--- SCRIPT ---")
    print(script)