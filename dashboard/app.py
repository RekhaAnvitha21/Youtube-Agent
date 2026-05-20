import streamlit as st
import os
import subprocess

st.set_page_config(
    page_title="YouTube Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
section[data-testid="stSidebar"]{display:none}
#MainMenu{display:none}
footer{display:none}
header{display:none}
[data-testid="stHeader"]{display:none}
[data-testid="stToolbar"]{display:none}
.stDeployButton{display:none}
div[data-testid="stDecoration"]{display:none}
.block-container{padding:0 !important;max-width:100% !important}
.stApp{background:#0d0f12}

.topbar{display:flex;align-items:center;justify-content:space-between;padding:18px 32px;border-bottom:1px solid #1e2530;background:#0d0f12}
.logo-wrap{display:flex;align-items:center;gap:10px}
.logo-icon{width:34px;height:34px;background:#7c3aed;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:17px}
.logo-text{font-size:15px;font-weight:700;color:#f1f5f9}
.logo-sub{font-size:11px;color:#475569;margin-top:1px}
.sys-badge{background:#0f2a1a;color:#4ade80;border:1px solid #166534;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600}

.body-wrap{padding:24px 32px;background:#0d0f12}

.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px}
.stat-card{background:#111827;border:1px solid #1e2530;border-radius:10px;padding:16px 18px}
.stat-label{font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}
.stat-val{font-size:24px;font-weight:700;color:#f1f5f9;margin-bottom:8px}
.pill{display:inline-flex;align-items:center;gap:4px;font-size:11px;padding:3px 9px;border-radius:20px}
.pill-green{background:#0f2a1a;color:#4ade80;border:1px solid #166534}
.pill-red{background:#2a0f0f;color:#f87171;border:1px solid #991b1b}
.pill-gray{background:#1e2530;color:#475569;border:1px solid #334155}

.sec-label{font-size:10px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:12px;margin-top:4px}

.pipeline-card{background:#111827;border:1px solid #1e2530;border-radius:10px;padding:20px 20px 16px;margin-bottom:20px}
.steps-row{display:flex;align-items:center;margin-bottom:18px}
.step-wrap{display:flex;flex-direction:column;align-items:center;flex:1}
.step-dot{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-bottom:5px}
.dot-done{background:#0f2a1a;color:#4ade80;border:2px solid #166534}
.dot-pending{background:#1e2530;color:#475569;border:2px solid #334155}
.step-lbl{font-size:9px;color:#475569;text-align:center;line-height:1.3}
.step-line{flex:1;height:1px;margin-bottom:22px}
.line-done{background:#166534}
.line-pending{background:#1e2530}

.log-box{background:#080c10;border:1px solid #1e2530;border-radius:6px;padding:14px;font-family:monospace;font-size:11px;color:#4ade80;line-height:1.9;margin-top:12px;white-space:pre-wrap;max-height:220px;overflow-y:auto}
.log-err{color:#f87171}

.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}
.panel{background:#111827;border:1px solid #1e2530;border-radius:10px;padding:16px}

.meta-row{display:flex;justify-content:space-between;align-items:flex-start;padding:9px 0;border-bottom:1px solid #1a2030;gap:16px}
.meta-row:last-child{border:none}
.mk{font-size:11px;color:#475569;flex-shrink:0;padding-top:1px}
.mv{font-size:11px;color:#cbd5e1;text-align:right;font-weight:500;line-height:1.4}
.tags-wrap{display:flex;flex-wrap:wrap;gap:4px;margin-top:10px}
.tag{background:#1e1b4b;color:#818cf8;border:1px solid #312e81;border-radius:20px;padding:2px 9px;font-size:10px}
.htag{background:#022c22;color:#34d399;border:1px solid #065f46;border-radius:20px;padding:2px 9px;font-size:10px}

.cap-box{background:#080c10;border:1px solid #1e2530;border-radius:6px;padding:14px;font-family:monospace;font-size:11px;color:#94a3b8;line-height:1.9;max-height:180px;overflow-y:auto}

div.stButton > button{
    background:#7c3aed !important;
    color:#fff !important;
    border:none !important;
    border-radius:8px !important;
    font-size:14px !important;
    font-weight:600 !important;
    padding:11px 20px !important;
    width:100% !important;
    margin-top:0 !important;
}
div.stButton > button:hover{background:#6d28d9 !important}
</style>
""", unsafe_allow_html=True)

OUTPUT_DIR = "D:/youtube-agent/output"
THUMBNAILS_DIR = "D:/youtube-agent/thumbnails"
CAPTIONS_DIR = "D:/youtube-agent/captions"
VOICE_DIR = "D:/youtube-agent/voice_generation"

video_path   = f"{OUTPUT_DIR}/final_video.mp4"
audio_path   = f"{VOICE_DIR}/voiceover.mp3"
thumb_path   = f"{THUMBNAILS_DIR}/thumbnail.png"
caption_path = f"{CAPTIONS_DIR}/captions.srt"
meta_path    = f"{OUTPUT_DIR}/metadata.txt"
transcript_path = f"{OUTPUT_DIR}/transcript.txt"

def exists(p): return os.path.exists(p)
def fsize(p):
    if not exists(p): return "—"
    s = os.path.getsize(p)
    return f"{s/1024/1024:.1f} MB" if s > 1024*1024 else f"{s/1024:.0f} KB"
def pill(ok):
    if ok: return '<span class="pill pill-green">✓ Ready</span>'
    return '<span class="pill pill-red">✗ Missing</span>'

st.markdown(f"""
<div class="topbar">
  <div class="logo-wrap">
    <div class="logo-icon">🎬</div>
    <div>
      <div class="logo-text">YouTube Agent</div>
      <div class="logo-sub">Autonomous AI video pipeline</div>
    </div>
  </div>
  <span class="sys-badge">● System Ready</span>
</div>
<div class="body-wrap">
<div class="stats-grid">
  <div class="stat-card"><div class="stat-label">Final Video</div><div class="stat-val">{fsize(video_path)}</div>{pill(exists(video_path))}</div>
  <div class="stat-card"><div class="stat-label">Voiceover</div><div class="stat-val">{fsize(audio_path)}</div>{pill(exists(audio_path))}</div>
  <div class="stat-card"><div class="stat-label">Thumbnail</div><div class="stat-val">{fsize(thumb_path)}</div>{pill(exists(thumb_path))}</div>
  <div class="stat-card"><div class="stat-label">Captions</div><div class="stat-val">{fsize(caption_path)}</div>{pill(exists(caption_path))}</div>
</div>
""", unsafe_allow_html=True)

all_done = all([exists(video_path), exists(audio_path), exists(thumb_path), exists(caption_path)])
steps = ["Trend","Script","Voice","Thumb","Meta","Captions","Video"]
steps_html = ""
for i, s in enumerate(steps):
    dot_cls = "dot-done" if all_done else "dot-pending"
    lbl = "✓" if all_done else str(i+1)
    steps_html += f'<div class="step-wrap"><div class="step-dot {dot_cls}">{lbl}</div><div class="step-lbl">{s}</div></div>'
    if i < len(steps)-1:
        line_cls = "line-done" if all_done else "line-pending"
        steps_html += f'<div class="step-line {line_cls}"></div>'

st.markdown(f"""
<div class="sec-label">Pipeline stages</div>
<div class="pipeline-card">
  <div class="steps-row">{steps_html}</div>
""", unsafe_allow_html=True)

if st.button("🚀  Run Full Pipeline"):
    with st.spinner("Running pipeline... this takes 5-10 minutes"):
        result = subprocess.run(
            [r"D:\youtube-agent\venv\Scripts\python.exe", "-m", "workflows.main_workflow"],
            capture_output=True, text=True, cwd="D:/youtube-agent"
        )
    if result.returncode == 0:
        st.success("Pipeline completed!")
        st.markdown(f'<div class="log-box">{result.stdout}</div>', unsafe_allow_html=True)
        st.rerun()
    else:
        st.error("Pipeline failed!")
        st.markdown(f'<div class="log-box log-err">{result.stderr[-3000:]}</div>', unsafe_allow_html=True)

if exists(transcript_path):
    with open(transcript_path,'r') as f:
        transcript = f.read()
    st.markdown(f'<div class="log-box" style="color:#94a3b8;">{transcript}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="body-wrap" style="padding-top:0"><div class="two-col">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="sec-label">Thumbnail preview</div>', unsafe_allow_html=True)
    if exists(thumb_path):
        st.image(thumb_path, use_container_width=True)
    else:
        st.markdown('<div class="panel" style="text-align:center;color:#334155;padding:3rem;font-size:13px;">No thumbnail yet</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="sec-label">Generated metadata</div>', unsafe_allow_html=True)
    if exists(meta_path):
        with open(meta_path,'r',encoding='utf-8') as f:
            lines = f.readlines()
        meta = {}
        script_start = False
        for line in lines:
            if line.startswith('SCRIPT:'): 
                script_start = True
                continue
            if not script_start and ':' in line:
                k,v = line.split(':',1)
                meta[k.strip()] = v.strip()
        
        rows = ""
        for k in ['TOPIC','TITLE','DESCRIPTION']:
            if k in meta:
                rows += f'<div class="meta-row"><span class="mk">{k.title()}</span><span class="mv">{meta[k][:80]}</span></div>'
        
        tags_html = ""
        if 'TAGS' in meta:
            for t in meta['TAGS'].split(','):
                tags_html += f'<span class="tag">{t.strip()}</span>'
        if 'HASHTAGS' in meta:
            for h in meta['HASHTAGS'].split(','):
                tags_html += f'<span class="htag">{h.strip()}</span>'
        
        st.markdown(f'<div class="panel">{rows}<div class="tags-wrap">{tags_html}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="panel" style="text-align:center;color:#334155;padding:3rem;font-size:13px;">Run pipeline first</div>', unsafe_allow_html=True)

st.markdown('<div style="padding:0 0 8px 0"><div class="sec-label">Captions preview</div>', unsafe_allow_html=True)
if exists(caption_path):
    with open(caption_path,'r') as f:
        caps = f.read()
    st.markdown(f'<div class="cap-box">{caps[:600]}</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)