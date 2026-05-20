import requests
import urllib.parse
import urllib.request

from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import os
from config.config import (
    OUTPUT_DIR, VOICE_DIR, THUMBNAILS_DIR,
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS
)

def fetch_image_for_scene(text, index):
    """Fetch a relevant image using Pexels API"""
    try:
        keywords = ' '.join(text.split()[:4])
        headers = {
            'Authorization': 'mgiY1cW84roAr1XSyNlFBYYKuNglcYLB2Ivt1r8yo9rNfqGJ9VgBaD56',
            'User-Agent': 'Mozilla/5.0'
        }
        params = {
            'query': keywords,
            'per_page': 1,
            'orientation': 'landscape'
        }
        response = requests.get(
            'https://api.pexels.com/v1/search',
            headers=headers,
            params=params,
            timeout=30
        )
        data = response.json()
        if data.get('photos'):
            img_url = data['photos'][0]['src']['large']
            img_response = requests.get(img_url, timeout=30)
            if img_response.status_code == 200:
                img_path = os.path.join(OUTPUT_DIR, f"scene_{index}.jpg")
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Image fetched for scene {index}")
                return img_path
        print(f"No images found for scene {index}")
        return None
    except Exception as e:
        print(f"Image fetch failed for scene {index}: {e}")
        return None



def create_text_clip(text, duration, fontsize=50, color='white', bg_color=(20,20,40), index=0):
    """Create a video clip with AI background image and text overlay"""
    
    img_path = fetch_image_for_scene(text, index)
    
    if img_path and os.path.exists(img_path):
        try:
            img = Image.open(img_path).resize((VIDEO_WIDTH, VIDEO_HEIGHT))
            overlay = Image.new('RGBA', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 140))
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay).convert('RGB')
        except Exception as e:
            print(f"Image open failed: {e}, using solid background")
            img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), color=bg_color)
    else:
        img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), color=bg_color)

    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", fontsize)
    except:
        font = ImageFont.load_default()
    
    words = text.split()
    lines = []
    current = []
    for word in words:
        current.append(word)
        if len(' '.join(current)) > 35:
            lines.append(' '.join(current[:-1]))
            current = [word]
    lines.append(' '.join(current))
    
    y = VIDEO_HEIGHT // 2 - (len(lines) * (fontsize + 10)) // 2
    for line in lines:
        draw.text((62, y + 4), line, fill=(0,0,0), font=font)
        draw.text((60, y), line, fill='white', font=font)
        y += fontsize + 10
    
    temp_path = os.path.join(OUTPUT_DIR, f"temp_frame_{index}.png")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img.save(temp_path)
    
    clip = ImageClip(temp_path).set_duration(duration)
    return clip

def assemble_video(script, audio_path, thumbnail_path, topic="",  output_filename="final_video.mp4"):
    """Assemble final video from script, audio and thumbnail"""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
   
    # Extract Narrator voiceover lines as scenes
    # Extract Narrator voiceover lines as scenes
    scenes = []
    for line in script.split('\n'):
        line = line.strip()
        if 'Narrator' in line and ':' in line:
            text = line.split(':', 1)[1].strip()
            text = text.strip('"').strip("'").strip()
            # Split each narrator line into individual sentences
            sentences = [s.strip() for s in text.replace('?','.').replace('!','.').split('.') if s.strip() and len(s.strip()) > 10]
            scenes.extend(sentences)
    
    print(f"Total scenes from script: {len(scenes)}")

    print(f"Creating {len(scenes)} scenes...")
    
    # Load audio
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    scene_duration = total_duration / max(len(scenes), 1)
    print(f"Audio duration: {total_duration:.1f}s, Each scene: {scene_duration:.1f}s")
    
    # Create video clips for each scene
    clips = []
    for i, scene in enumerate(scenes):
        print(f"Creating scene {i+1}...")
        bg_colors = [
            (20, 20, 40), (40, 20, 20),
            (20, 40, 20), (40, 20, 40),
            (20, 40, 40), (40, 40, 20)
        ]
        clip = create_text_clip(
            scene,
            duration=scene_duration,
            bg_color=bg_colors[i % len(bg_colors)],
            index=i
        )
        clips.append(clip)
    
    # Create title slide at the start
    print("Creating title slide...")
    title_clip = create_text_clip(
        topic,
        duration=4,
        fontsize=55,
        color='yellow',
        bg_color=(10, 10, 30)
    )
    clips.insert(0, title_clip)

    # Concatenate all clips
    print("Assembling video...")
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.set_audio(audio)
    
    # Export
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    final_video.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec='libx264',
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    
    # Save transcript
    transcript_path = os.path.join(OUTPUT_DIR, "transcript.txt")
    with open(transcript_path, 'w') as f:
        f.write("SCENES/TRANSCRIPT\n")
        f.write("="*40 + "\n")
        for i, scene in enumerate(scenes):
            f.write(f"Scene {i+1} ({scene_duration:.1f}s):\n{scene}\n\n")
    
    print(f"Video saved to: {output_path}")
    print(f"Transcript saved to: {transcript_path}")
    return output_path

if __name__ == "__main__":
    sample_script = """
    After decades of chasing passive income, I discovered some hard earned lessons.
    I made risky bets without understanding the market, and it cost me dearly.
    Diversification is key to long term success.
    Neglecting finances was a huge mistake. Track expenses and save aggressively.
    Follow me for more insights and subscribe for weekly updates.
    """
    
    audio_path = "D:/youtube-agent/voice_generation/voiceover.mp3"
    thumbnail_path = "D:/youtube-agent/thumbnails/thumbnail.png"
    
    print("Assembling final video...")
    path = assemble_video(sample_script, audio_path, thumbnail_path)
    print(f"Done! Video at: {path}")