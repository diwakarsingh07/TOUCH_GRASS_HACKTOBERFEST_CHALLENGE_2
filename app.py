"""
TrailWhisper: 100% Offline Bioacoustic Companion (Mobile & Field Ready)
======================================================================
Theme: Touch Grass (Hacktoberfest Challenge #2)
Core: Open-Weight Bioacoustic Models + Phone Voice Recording + Offline Earbud Voice
"""

import os
import io
import time
import streamlit as st
import numpy as np
import plotly.graph_objects as go

from audio_engine import AudioEngine
from bird_classifier import BirdClassifier
from naturalist import NaturalistEngine
from voice_out import speak_offline
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TrailWhisper // Offline Wilderness Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- OUTDOOR NATURE MINIMALIST STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 0%, #15221b 0%, #0c1410 50%, #070b09 100%);
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hero Header */
    .hero-box {
        background: rgba(20, 35, 27, 0.75);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #4ade80 0%, #22c55e 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 12px;
    }

    .badge-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .nature-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-offline {
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid #22c55e;
        color: #86efac;
    }
    .badge-zero-cost {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #f59e0b;
        color: #fde68a;
    }
    .badge-screen {
        background: rgba(14, 165, 233, 0.15);
        border: 1px solid #0ea5e9;
        color: #7dd3fc;
    }
    .badge-mobile {
        background: rgba(168, 85, 247, 0.15);
        border: 1px solid #a855f7;
        color: #d8b4fe;
    }

    /* Result Cards */
    .nature-card {
        background: rgba(18, 30, 24, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35);
    }
    .look-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(20, 83, 45, 0.25) 100%);
        border: 1px solid #22c55e;
        border-radius: 12px;
        padding: 18px;
        margin-top: 16px;
    }

    /* Touch Grass Zen Screen */
    .zen-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 65vh;
        text-align: center;
        padding: 40px;
    }
    .zen-leaf {
        font-size: 4.5rem;
        margin-bottom: 16px;
    }
    .zen-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #4ade80;
        margin-bottom: 12px;
    }
    .zen-subtitle {
        color: #94a3b8;
        font-size: 1.15rem;
        max-width: 500px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

DEMO_DIR = r"D:\trailwhisper\demo_sounds"

# Session State for "Touch Grass" Zen Mode
if "touch_grass_mode" not in st.session_state:
    st.session_state.touch_grass_mode = False

# --- ZEN MODE (TOUCH GRASS SCREEN-OFF) ---
if st.session_state.touch_grass_mode:
    st.markdown("""
<div class="zen-container">
    <div class="zen-leaf">🌿</div>
    <div class="zen-title">SCREEN ASLEEP. YOU ARE OUTSIDE.</div>
    <div class="zen-subtitle">
        Put your phone back in your pocket. Listen to the forest canopy, feel the autumn breeze, and touch grass.
    </div>
</div>
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("👁️ Tap to Wake Screen (Hike Paused)", use_container_width=True):
            st.session_state.touch_grass_mode = False
            st.rerun()
    st.stop()

# --- HERO BANNER ---
st.markdown("""
<div class="hero-box">
    <div class="hero-title">TRAILWHISPER 🌿</div>
    <div class="hero-subtitle">Open-Weight Wilderness Bioacoustic Scout & Fall Foliage Field Companion</div>
    <div class="badge-bar">
        <span class="nature-badge badge-mobile">📱 RUNS ON PHONE / MOBILE RECORDER</span>
        <span class="nature-badge badge-offline">● 100% OFFLINE (ZERO CELL SIGNAL NEEDED)</span>
        <span class="nature-badge badge-screen">● SCREEN TIME: &lt; 5 SECONDS</span>
        <span class="nature-badge badge-zero-cost">● OPEN-WEIGHT BIOACOUSTICS ($0 CLOUD COST)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SINGLE CLEAN DETERMINISTIC INPUT CONTROLLER ---
input_mode = st.radio(
    "Choose Audio Source:",
    [
        "🌲 Calibrated Trail Audio Presets (Test 7 Species)",
        "📱 Upload Phone Voice Recording (WAV/MP3/M4A/OGG)",
        "🎙️ In-Browser Mic Widget"
    ],
    horizontal=True
)

audio_data = None
sample_rate = 22050
raw_audio_bytes = None

if input_mode == "🌲 Calibrated Trail Audio Presets (Test 7 Species)":
    sample_files = [
        "mourning_dove_pigeon.wav",
        "black_capped_chickadee.wav",
        "northern_cardinal.wav",
        "american_robin.wav",
        "great_horned_owl.wav",
        "red_tailed_hawk.wav",
        "downy_woodpecker.wav",
        "ambient_forest_wind.wav"
    ]
    
    clean_names = {
        "mourning_dove_pigeon.wav": "🕊️ Mourning Dove / Rock Pigeon (Soft Hollow Cooing)",
        "black_capped_chickadee.wav": "🌲 Black-capped Chickadee ('Fee-bee' Whistle)",
        "northern_cardinal.wav": "🔴 Northern Cardinal (Rapid Metallic Sweet Whistles)",
        "american_robin.wav": "🍂 American Robin (Cheerful Liquid Warble)",
        "great_horned_owl.wav": "🦉 Great Horned Owl (Deep Resonant Night Hoot)",
        "red_tailed_hawk.wav": "🦅 Red-tailed Hawk (Piercing Descending Scream)",
        "downy_woodpecker.wav": "🪵 Downy Woodpecker (Fast Mechanical Drum Roll)",
        "ambient_forest_wind.wav": "💨 Ambient Forest (Wind & Rustling Leaves Only)"
    }

    selected_sample = st.selectbox(
        "Select Bird or Trail Sound:",
        sample_files,
        format_func=lambda x: clean_names.get(x, x)
    )
    
    audio_path = os.path.join(DEMO_DIR, selected_sample)
    sample_rate, audio_data = AudioEngine.load_audio(audio_path)
    try:
        with open(audio_path, "rb") as f:
            raw_audio_bytes = f.read()
    except Exception:
        pass
    st.audio(audio_path, format="audio/wav")

elif input_mode == "📱 Upload Phone Voice Recording (WAV/MP3/M4A/OGG)":
    st.markdown("<small style='color: #94a3b8;'>Tap below on your phone to open your native Voice Recorder app:</small>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose an audio recording from your phone",
        type=["wav", "mp3", "m4a", "ogg", "flac"]
    )
    if uploaded_file is not None:
        try:
            raw_audio_bytes = uploaded_file.getvalue()
            sample_rate, audio_data = AudioEngine.load_audio_from_buffer(uploaded_file)
            st.success("✅ Phone audio loaded successfully!")
            st.audio(uploaded_file)
        except Exception as e:
            st.error(f"Error reading phone audio: {e}")

else: # In-Browser Mic Widget
    live_audio = st.audio_input("Record audio with browser mic")
    if live_audio is not None:
        try:
            raw_audio_bytes = live_audio.getvalue()
            sample_rate, audio_data = AudioEngine.load_audio_from_buffer(live_audio)
            st.success("✅ In-browser audio recording captured!")
            st.audio(live_audio)
        except Exception as e:
            st.error(f"Error reading mic: {e}")

# Analysis trigger button
st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("🎧 IDENTIFY SOUND & LISTEN IN EARBUDS", use_container_width=True, type="primary")

# Run Analysis
if audio_data is not None:
    features = AudioEngine.extract_bioacoustic_features(audio_data, sample_rate)
    with st.spinner("🎧 Multimodal AI analyzing audio acoustic signatures..."):
        classification = BirdClassifier.classify(features, audio_bytes=raw_audio_bytes)
        guidance = NaturalistEngine.get_field_guidance(classification)

    if analyze_btn:
        # 1. Desktop offline speech synthesis (Windows)
        speak_offline(guidance["earbuds_voice_script"])

        # 2. Browser & Mobile Earbuds speech synthesis (Web Speech API)
        clean_voice = guidance["earbuds_voice_script"].replace("'", "\\'").replace('"', '\\"')
        components.html(f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const u = new SpeechSynthesisUtterance('{clean_voice}');
                u.rate = 1.0;
                u.pitch = 1.0;
                window.speechSynthesis.speak(u);
            }}
        </script>
        """, height=0)

    # --- RESULTS SECTION ---
    col_res, col_spec = st.columns([1, 1])

    with col_res:
        if classification["identified"]:
            card_html = f"""<div class="nature-card">
<div style="font-size: 0.78rem; color: #22c55e; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
● {guidance.get('engine', 'MULTIMODAL AI AUDIO MATCH')}
</div>
<div style="font-size: 1.8rem; font-weight: 800; color: #f8fafc; margin-top: 4px;">
{guidance['species']}
</div>
<div style="font-style: italic; color: #94a3b8; font-size: 0.95rem;">
{guidance['scientific_name']} &nbsp;|&nbsp; Confidence: <b style="color: #4ade80;">{guidance['confidence']}</b>
</div>
<div style="margin-top: 14px; font-size: 0.9rem; color: #cbd5e1;">
<b>Vocalization Pattern:</b> {guidance['vocalization']}
</div>
<div class="look-card">
<div style="font-weight: 700; color: #4ade80; font-size: 1.05rem; margin-bottom: 6px;">
👁️ WHERE TO LOOK IN NATURE RIGHT NOW:
</div>
<div style="color: #f1f5f9; font-size: 0.95rem; margin-bottom: 8px;">
{guidance['look_where']}
</div>
<div style="color: #cbd5e1; font-size: 0.88rem; margin-bottom: 6px;">
<b>Visual Clues:</b> {guidance['visual_clues']}
</div>
<div style="color: #fcd34d; font-size: 0.88rem;">
<b>Autumn Behavior:</b> {guidance['fall_behavior']}
</div>
</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)
        else:
            ambient_html = f"""<div class="nature-card">
<div style="font-size: 0.75rem; color: #f59e0b; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">
● {guidance.get('engine', 'WILDERNESS AMBIENT')}
</div>
<div style="font-size: 1.4rem; font-weight: 800; color: #f59e0b;">
🍂 {classification['common_name']}
</div>
<div style="color: #94a3b8; margin-top: 6px;">
{classification['vocalization']}
</div>
<div class="look-card" style="border-color: #f59e0b; background: rgba(245, 158, 11, 0.1);">
<div style="color: #fde68a; font-weight: 700;">
🌿 Naturalist Observation:
</div>
<div style="color: #f1f5f9; font-size: 0.9rem; margin-top: 4px;">
{guidance.get('touch_grass_action', 'Take a deep breath of crisp autumn air, listen to the gentle breeze in the canopy, and keep walking the trail.')}
</div>
</div>
</div>"""
            st.markdown(ambient_html, unsafe_allow_html=True)

    with col_spec:
        st.markdown('<div style="font-weight: 700; color: #e2e8f0; margin-bottom: 8px;">📊 2D Spectrogram (Acoustic Frequency Bands)</div>', unsafe_allow_html=True)
        
        freqs, times, Sxx_db = AudioEngine.compute_spectrogram(audio_data, sample_rate)
        
        fig = go.Figure(data=go.Heatmap(
            z=Sxx_db,
            x=times,
            y=freqs,
            colorscale='Viridis',
            colorbar=dict(title='dB', thickness=12)
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 23, 42, 0.5)',
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis=dict(title='Time (s)', color='#94a3b8', showgrid=False),
            yaxis=dict(title='Frequency (Hz)', color='#94a3b8', range=[200, 8000], showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

# --- TOUCH GRASS BLANK-SCREEN TRIGGER ---
st.markdown("---")
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    if st.button("🌿 TOUCH GRASS NOW (BLANK SCREEN & LOOK UP)", use_container_width=True, type="secondary"):
        st.session_state.touch_grass_mode = True
        st.rerun()
