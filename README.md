# YouTube Agent - Autonomous AI Video Pipeline

An end-to-end autonomous AI system that runs a YouTube channel with zero human intervention.

## What it does
1. Discovers trending topics from RSS feeds
2. Selects the best topic using Mistral LLM
3. Generates a complete YouTube script
4. Converts script to voiceover audio
5. Creates a branded thumbnail
6. Fetches relevant scene images
7. Assembles a final MP4 video
8. Generates SRT captions
9. Produces SEO-optimized metadata

## Tech Stack
- **LLM**: Mistral via Ollama (runs locally)
- **Agent Framework**: CrewAI
- **Voice**: gTTS / pyttsx3
- **Captions**: OpenAI Whisper
- **Video**: MoviePy + FFmpeg
- **Thumbnails**: Pillow
- **Dashboard**: Streamlit
- **Images**: Pexels API

## Hardware Note
Built and tested on CPU-only machine (Intel i5, 8GB RAM).
Wan2GP and Stable Diffusion require a dedicated GPU.
Pexels API is used as a fallback for scene visuals.

## How to Run
1. Install Ollama and pull Mistral: `ollama pull mistral`
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run pipeline: `python -m workflows.main_workflow`
6. Run dashboard: `streamlit run dashboard/app.py`

## Folder Structure
/agents          - Individual AI agents
/workflows       - Pipeline orchestration
/dashboard       - Streamlit UI
/config          - Configuration
/output          - Generated videos
/thumbnails      - Generated thumbnails
/captions        - SRT caption files
/voice\_generation - Audio files

## Agents
| Agent | Role |
|-------|------|
| Trend Agent | Discovers trending topics |
| Script Agent | Writes YouTube scripts |
| Voice Agent | Generates voiceover |
| Thumbnail Agent | Creates thumbnails |
| Metadata Agent | SEO optimization |
| Caption Agent | Generates SRT captions |
| Video Agent | Assembles final video |



