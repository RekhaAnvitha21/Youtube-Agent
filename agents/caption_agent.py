import whisper
import os
from config.config import CAPTIONS_DIR, VOICE_DIR

def generate_captions(audio_path, filename="captions.srt"):
    """Generate SRT captions from audio using Whisper"""
    
    print("Loading Whisper model...")
    model = whisper.load_model("tiny")
    
    print("Transcribing audio...")
    result = model.transcribe(audio_path, language="en")
    
    os.makedirs(CAPTIONS_DIR, exist_ok=True)
    output_path = os.path.join(CAPTIONS_DIR, filename)
    
    # Write SRT format
    with open(output_path, 'w') as f:
        for i, segment in enumerate(result["segments"]):
            start = format_time(segment["start"])
            end = format_time(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")
    
    print(f"Captions saved to: {output_path}")
    return output_path

def format_time(seconds):
    """Convert seconds to SRT time format"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

if __name__ == "__main__":
    audio_path = "D:/youtube-agent/voice_generation/voiceover.mp3"
    print("Generating captions...")
    path = generate_captions(audio_path)
    print("Done!")