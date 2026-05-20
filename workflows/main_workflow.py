import sys
import os
sys.path.append('D:/youtube-agent')

from agents.trend_agent import fetch_trending_topics, select_best_topic
from agents.script_agent import generate_script
from agents.voice_agent import generate_voiceover
from agents.thumbnail_agent import generate_thumbnail
from agents.metadata_agent import generate_metadata
from agents.video_agent import assemble_video
from agents.caption_agent import generate_captions

def run_pipeline():
    print("="*50)
    print("  YOUTUBE AGENT PIPELINE STARTING")
    print("="*50)
    
    # Step 1: Find trending topic
    print("\n[1/7] Finding trending topics...")
    topics = fetch_trending_topics()
    topic = select_best_topic(topics)
    print(f"Selected topic: {topic}")
    
    # Step 2: Generate script
    print("\n[2/7] Generating script...")
    script = generate_script(topic)
    print("Script generated!")
    
    # Step 3: Generate voiceover
    print("\n[3/7] Generating voiceover...")
    audio_path = generate_voiceover(script, topic=topic)
    print(f"Audio saved: {audio_path}")
    
    # Step 4: Generate thumbnail
    print("\n[4/7] Generating thumbnail...")
    thumbnail_path = generate_thumbnail(topic)
    print(f"Thumbnail saved: {thumbnail_path}")
    
    # Step 5: Generate metadata
    print("\n[5/7] Generating metadata...")
    metadata = generate_metadata(topic, script)
    print(f"Title: {metadata['title']}")
    print(f"Tags: {', '.join(metadata['tags'])}")
    
    # Step 6: Generate captions
    print("\n[6/7] Generating captions...")
    captions_path = generate_captions(audio_path)
    print(f"Captions saved: {captions_path}")
    
    # Step 7: Assemble video
    print("\n[7/7] Assembling final video...")
    video_path = assemble_video(script, audio_path, thumbnail_path, topic=topic)
    
    # Save metadata to file
    metadata_path = os.path.join('D:/youtube-agent/output', 'metadata.txt')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(f"TOPIC: {topic}\n\n")
        f.write(f"TITLE: {metadata['title']}\n\n")
        f.write(f"DESCRIPTION: {metadata['description']}\n\n")
        f.write(f"TAGS: {', '.join(metadata['tags'])}\n\n")
        f.write(f"HASHTAGS: {', '.join(metadata['hashtags'])}\n\n")
        f.write(f"SCRIPT:\n{script}\n")
    
    print("\n" + "="*50)
    print("  PIPELINE COMPLETE!")
    print("="*50)
    print(f"Video: {video_path}")
    print(f"Thumbnail: {thumbnail_path}")
    print(f"Captions: {captions_path}")
    print(f"Metadata: {metadata_path}")
    print(f"Audio: {audio_path}")

if __name__ == "__main__":
    run_pipeline()