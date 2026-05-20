import sys
import os
sys.path.append('D:/youtube-agent')

from crewai import Agent, Task, Crew, Process
from agents.trend_agent import fetch_trending_topics, select_best_topic
from agents.script_agent import generate_script
from agents.voice_agent import generate_voiceover
from agents.thumbnail_agent import generate_thumbnail
from agents.metadata_agent import generate_metadata
from agents.video_agent import assemble_video
from agents.caption_agent import generate_captions

pipeline_state = {}

trend_agent = Agent(
    role="Trend Research Analyst",
    goal="Discover the most viral and engaging trending topics for YouTube",
    backstory="""You are an expert digital media analyst with years of experience 
    identifying viral content trends across YouTube, Reddit, and tech news.""",
    verbose=True,
    allow_delegation=False
)

script_agent = Agent(
    role="YouTube Script Writer",
    goal="Write compelling engaging YouTube video scripts that keep viewers watching",
    backstory="""You are a professional YouTube scriptwriter who has written scripts 
    for channels with millions of subscribers.""",
    verbose=True,
    allow_delegation=False
)

voice_agent = Agent(
    role="Voice Production Specialist",
    goal="Convert scripts into natural engaging voiceovers",
    backstory="""You are a voice production specialist who transforms written scripts 
    into professional audio narration.""",
    verbose=True,
    allow_delegation=False
)

thumbnail_agent = Agent(
    role="Thumbnail Design Specialist",
    goal="Create eye-catching YouTube thumbnails that maximize click-through rates",
    backstory="""You are a visual design expert specializing in YouTube thumbnails 
    that consistently achieve above-average CTR.""",
    verbose=True,
    allow_delegation=False
)

metadata_agent = Agent(
    role="SEO and Metadata Optimizer",
    goal="Generate optimized titles descriptions tags and hashtags for maximum YouTube reach",
    backstory="""You are a YouTube SEO expert who has helped dozens of channels 
    grow through strategic metadata optimization.""",
    verbose=True,
    allow_delegation=False
)

caption_agent = Agent(
    role="Caption and Accessibility Specialist",
    goal="Generate accurate captions and subtitles for video content",
    backstory="""You are an accessibility specialist who ensures all video content 
    is properly captioned using AI transcription tools.""",
    verbose=True,
    allow_delegation=False
)

video_agent = Agent(
    role="Video Production and Rendering Specialist",
    goal="Assemble all assets into a polished final YouTube video",
    backstory="""You are a video production expert who combines scripts voiceovers 
    visuals and captions into compelling final videos.""",
    verbose=True,
    allow_delegation=False
)

def run_crew_pipeline():
    print("="*55)
    print("   YOUTUBE AGENT CREW - STARTING PIPELINE")
    print("="*55)

    print("\n[Agent 1/7] Trend Research Analyst working...")
    topics = fetch_trending_topics()
    topic = select_best_topic(topics)
    pipeline_state['topic'] = topic
    print(f"Topic selected: {topic}")

    print("\n[Agent 2/7] Script Writer working...")
    script = generate_script(topic)
    pipeline_state['script'] = script
    print("Script generated!")

    print("\n[Agent 3/7] Voice Production Specialist working...")
    audio_path = generate_voiceover(script, topic=topic)
    pipeline_state['audio_path'] = audio_path
    print(f"Voiceover: {audio_path}")

    print("\n[Agent 4/7] Thumbnail Design Specialist working...")
    thumbnail_path = generate_thumbnail(topic)
    pipeline_state['thumbnail_path'] = thumbnail_path
    print(f"Thumbnail: {thumbnail_path}")

    print("\n[Agent 5/7] SEO and Metadata Optimizer working...")
    metadata = generate_metadata(topic, script)
    pipeline_state['metadata'] = metadata
    print(f"Title: {metadata['title']}")

    print("\n[Agent 6/7] Caption Specialist working...")
    captions_path = generate_captions(audio_path)
    pipeline_state['captions_path'] = captions_path
    print(f"Captions: {captions_path}")

    print("\n[Agent 7/7] Video Production Specialist working...")
    video_path = assemble_video(script, audio_path, thumbnail_path, topic=topic)
    pipeline_state['video_path'] = video_path

    output_meta = os.path.join('D:/youtube-agent/output', 'metadata.txt')
    with open(output_meta, 'w', encoding='utf-8') as f:
        f.write(f"TOPIC: {topic}\n\n")
        f.write(f"TITLE: {metadata['title']}\n\n")
        f.write(f"DESCRIPTION: {metadata['description']}\n\n")
        f.write(f"TAGS: {', '.join(metadata['tags'])}\n\n")
        f.write(f"HASHTAGS: {', '.join(metadata['hashtags'])}\n\n")
        f.write(f"SCRIPT:\n{script}\n")

    tasks = [
        Task(
            description="Research and identify the best trending topic for YouTube",
            expected_output="A single trending topic string",
            agent=trend_agent
        ),
        Task(
            description="Write a complete YouTube video script for the topic",
            expected_output="A complete YouTube script",
            agent=script_agent
        ),
        Task(
            description="Convert the script into an audio voiceover file",
            expected_output="File path to the voiceover MP3",
            agent=voice_agent
        ),
        Task(
            description="Design and generate a YouTube thumbnail",
            expected_output="File path to the thumbnail PNG",
            agent=thumbnail_agent
        ),
        Task(
            description="Generate optimized YouTube metadata",
            expected_output="Title description tags and hashtags",
            agent=metadata_agent
        ),
        Task(
            description="Generate accurate SRT captions from the voiceover",
            expected_output="File path to the SRT captions file",
            agent=caption_agent
        ),
        Task(
            description="Assemble the final YouTube video from all assets",
            expected_output="File path to the final MP4 video",
            agent=video_agent
        ),
    ]

    crew = Crew(
        agents=[
            trend_agent, script_agent, voice_agent,
            thumbnail_agent, metadata_agent, caption_agent, video_agent
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    print("\n" + "="*55)
    print("   PIPELINE COMPLETE!")
    print("="*55)
    print(f"\nCrew agents: {len(crew.agents)}")
    print(f"Tasks defined: {len(crew.tasks)}")
    print(f"\nOutputs:")
    print(f"  Video:     {video_path}")
    print(f"  Audio:     {audio_path}")
    print(f"  Thumbnail: {thumbnail_path}")
    print(f"  Captions:  {captions_path}")
    print(f"  Metadata:  {output_meta}")

if __name__ == "__main__":
    run_crew_pipeline()