from gtts import gTTS
import pyttsx3
import os
from config.config import VOICE_DIR

def generate_voiceover(script, filename="voiceover.mp3", topic=""):
    """Convert script text to speech"""
    
    lines = script.split('\n')
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        if 'Narrator' in line and ':' in line:
            text = line.split(':', 1)[1].strip()
            text = text.strip('"').strip("'").strip()
            if len(text) > 10:
                clean_lines.append(text)
    
    if topic:
        clean_lines.insert(0, topic)
    
    clean_script = ' '.join(clean_lines)
    print(f"Cleaned script length: {len(clean_script)} characters")
    
    os.makedirs(VOICE_DIR, exist_ok=True)
    output_path = os.path.join(VOICE_DIR, filename)
    
    # Try gTTS first, fall back to pyttsx3
    try:
        tts = gTTS(text=clean_script, lang='en', slow=False)
        tts.save(output_path)
        print(f"Voiceover saved (gTTS): {output_path}")
    except Exception as e:
        print(f"gTTS failed: {e}. Using pyttsx3 fallback...")
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        # pyttsx3 saves as wav, convert path
        wav_path = output_path.replace('.mp3', '.wav')
        engine.save_to_file(clean_script, wav_path)
        engine.runAndWait()
        # Remove existing file if exists before rename
        if os.path.exists(output_path):
            os.remove(output_path)
        os.rename(wav_path, output_path)
        print(f"Voiceover saved (pyttsx3): {output_path}")
    
    return output_path

if __name__ == "__main__":
    sample_script = """
    Narrator (Voiceover): "After decades of chasing passive income, I discovered some hard earned lessons."
    Narrator (Voiceover): "I made risky bets without understanding the market, and it cost me dearly."
    """
    print("Generating voiceover...")
    path = generate_voiceover(sample_script)
    print(f"Done! File saved at: {path}")