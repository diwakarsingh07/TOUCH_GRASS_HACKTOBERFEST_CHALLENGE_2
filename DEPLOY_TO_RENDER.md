# 🚀 Deploying TrailWhisper to Render (100% Free)

This guide shows how to deploy TrailWhisper to **Render** completely free ($0/month), giving you a public `https://trailwhisper.onrender.com` URL that unlocks native mobile phone microphone access and provides a live demo link for hackathon judges.

---

## 💡 Why Deploy on Render (Free Tier)?

1. **Unlocks Mobile Phone Microphone Permanently (`https://`)**:
   - Modern mobile browsers (iOS Safari, Android Chrome) block microphone access on plain HTTP local addresses (`http://192.168.x.x:8502`).
   - Render automatically provisions a free SSL certificate (`https://`), so when you open the link on your phone on the trail, mobile microphone recording works seamlessly with one tap.
2. **Preserves 100% of Your $100 MLH Cloud Credits**:
   - Render's Web Service free tier costs **$0.00**.
   - Your $100 MLH credits stay untouched in your cloud account for future hackathons (where you'll need heavy GPU compute or database clusters).
3. **Judge Submission Link**:
   - Hackathon judges and DEV.to readers can test the live demo on their own phones and laptops immediately.

---

## 📋 3-Minute Deployment Steps

### Step 1: Push `D:\trailwhisper` to GitHub
Open your terminal in `D:\trailwhisper` and run:
```bash
git init
git add .
git commit -m "feat: complete TrailWhisper bioacoustic nature app"
git branch -M main
# Link to your GitHub repository:
git remote add origin https://github.com/<your-username>/trailwhisper.git
git push -u origin main
```

### Step 2: Create Free Web Service on Render
1. Go to [render.com](https://render.com) and log in (with GitHub).
2. Click **New +** (top right) -> **Web Service**.
3. Select your `trailwhisper` repository.
4. Render will auto-detect the configuration, or fill in these fields:
   - **Name**: `trailwhisper` (or any name you choose)
   - **Region**: `Oregon (US West)` or `Frankfurt`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false`
   - **Instance Type**: **Free** ($0 / month)
5. Click **Create Web Service**.

### Step 3: Test on Your Mobile Phone!
1. Render will build the environment and deploy within 1–2 minutes.
2. Render gives you your live URL: `https://trailwhisper.onrender.com`.
3. Open this link on your smartphone in the woods or park:
   - The browser microphone works automatically over HTTPS.
   - Tap **"Record audio with browser mic"** or upload a bird sound.
   - Hit **"IDENTIFY SOUND & LISTEN IN EARBUDS"**.
   - Your phone will speak the species and where to look directly into your Bluetooth earbuds!
   - Tap **"TOUCH GRASS NOW"** to blank the screen and look up!
