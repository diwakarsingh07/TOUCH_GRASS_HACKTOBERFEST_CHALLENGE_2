# 🌿 TrailWhisper: Dual-Engine Multimodal Bioacoustic Scout

> **Built for Hacktoberfest Weekend Challenge: Touch Grass (October 2026)**  
> *Get off your screen and out into the wild. Dual-engine multimodal audio intelligence + offline bioacoustics, zero cell reception required, Bluetooth earbud voice guidance, and an automatic screen-blanker.*

---

## 🌲 The "Touch Grass" Problem
When people hike into nature, they often hear fascinating bird vocalizations or wildlife rustles in the canopy. But when they pull out their phones:
1. **Zero Cell Reception:** Deep in canyons, mountain passes, and national forest trails, there is no 5G. Proprietary AI apps and ChatGPT fail with *"No Internet Connection"*.
2. **Screen Traps & Notification Pollution:** Commercial apps trap users staring at glowing glass, doomscrolling social notifications instead of looking at nature.
3. **Expensive Cloud Subscriptions:** Proprietary apps lock audio databases behind monthly paywalls.

**TrailWhisper solves this by making the screen the shortest part of the experience.**

---

## ⚡ How TrailWhisper Works

```
[ Trail Audio / Phone Mic / YouTube Video ]
                       │
                       ▼
         [ Dual-Engine Ingestion ]
           ├── Connected: ✨ Google Gemini Flash Multimodal Audio AI (Zero-shot recognition)
           └── Offline:   🌲 Calibrated Bioacoustic Spectral Matcher (STFT + Flatness + Cadence)
                       │
                       ▼
          [ Naturalist Guidance Engine ]
    ("Where to look in the real canopy with your eyes")
                       │
                       ├──────────> [ Bluetooth Earbuds Voice: Web Speech API & Local Speech ]
                       │
                       └──────────> [ "Touch Grass" Screen-Blanker: Puts display to sleep ]
```

1. **Dual-Engine Multimodal Audio:** Uses Google Gemini Flash for frontier acoustic understanding across all species, animals, rain, and human speech, with an automated 100% offline bioacoustic matcher fallback for remote wilderness trails.
2. **Physical Field Guidance ("Look With Your Eyes"):** Instead of generic trivia, it tells you *where to look in the real world* (e.g., *"Look 15 feet up on dead birch twigs"* or *"Scan low on the trail for pigeons foraging on weed seeds"*).
3. **Bluetooth Earbud Voice:** Speaks directly through your headphones using the browser's Web Speech API and native offline speech synthesis so you don't even need to look at the screen.
4. **Touch Grass Auto-Blank:** Shuts down the screen into a dim leaf Zen mode so you put your phone in your pocket and touch grass.
5. **100% Free Hosting on Render:** Configured for Render's free tier with native SSL (`https://`), ensuring phone browsers grant microphone access seamlessly.

---

## 🛠️ Quickstart (Run Locally)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch TrailWhisper
```bash
streamlit run app.py
```

### 3. Open in Browser
Visit `http://localhost:8501`. Test with calibrated audio presets, upload phone voice recordings, or record live through your microphone.

---

## 🚀 Deploy to Render (100% Free)

See the complete guide in [`DEPLOY_TO_RENDER.md`](DEPLOY_TO_RENDER.md).
1. Push this repository to GitHub.
2. Create a Free Web Service on [Render](https://render.com).
3. Open `https://your-app.onrender.com` on your mobile phone to use your phone's microphone over HTTPS.

---

## 📁 Repository Structure

```
├── audio_engine.py       # 2D STFT spectrogram & spectral feature extraction (RMS, Flatness, Cadence)
├── bird_classifier.py    # Dual-Engine: Google Gemini Flash Multimodal AI + Offline Bioacoustics
├── naturalist.py         # Open naturalist knowledge base & physical field guidance
├── voice_out.py          # Native offline earbud voice dispatcher
├── app.py                # Streamlit UI with Web Speech API & Touch Grass screen-blanker
├── demo_sounds/          # Calibrated wilderness WAV audio samples (8 species & nature sounds)
├── render.yaml           # Infrastructure-as-code for Render deployment
├── Procfile              # Cloud process execution command
├── DEPLOY_TO_RENDER.md   # Step-by-step free deployment guide
└── SUBMISSION.md         # Official DEV.to Hacktoberfest submission post
```

---

## 📄 License
MIT License. Built for open outdoor innovation.
