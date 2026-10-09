"""
Generate realistic synthetic audio samples of bird vocalizations and wilderness sounds.
Enables 100% offline testing of TrailWhisper bioacoustic engine without internet.
"""

import os
import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 22050
DURATION = 3.0 # seconds
OUT_DIR = r"D:\trailwhisper\demo_sounds"

def save_wav(name: str, audio: np.ndarray):
    # Normalize to 16-bit PCM
    audio = audio / (np.max(np.abs(audio)) + 1e-9)
    audio_int16 = (audio * 32767).astype(np.int16)
    wavfile.write(os.path.join(OUT_DIR, name), SAMPLE_RATE, audio_int16)
    print(f"Generated: {name}")

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)

# 1. Black-capped Chickadee: Classic "Fee-bee" two-tone whistle (3800 Hz -> 3300 Hz)
chickadee = np.zeros_like(t)
# Note 1: 0.2s - 0.7s at 3800 Hz
m1 = (t >= 0.2) & (t <= 0.7)
chickadee[m1] = np.sin(2 * np.pi * 3800 * t[m1]) * np.sin(np.pi * (t[m1] - 0.2) / 0.5)
# Note 2: 0.9s - 1.5s at 3250 Hz
m2 = (t >= 0.9) & (t <= 1.5)
chickadee[m2] = np.sin(2 * np.pi * 3250 * t[m2]) * np.sin(np.pi * (t[m2] - 0.9) / 0.6)
# Repeat
m3 = (t >= 1.8) & (t <= 2.3)
chickadee[m3] = np.sin(2 * np.pi * 3800 * t[m3]) * np.sin(np.pi * (t[m3] - 1.8) / 0.5)
save_wav("black_capped_chickadee.wav", chickadee)

# 2. Northern Cardinal: Sharp rapid rising frequency sweeps (2400 Hz -> 4200 Hz)
cardinal = np.zeros_like(t)
for start_t in [0.2, 0.7, 1.2, 1.8, 2.3]:
    m = (t >= start_t) & (t <= start_t + 0.35)
    t_rel = t[m] - start_t
    freq = 2400 + 1800 * (t_rel / 0.35)
    cardinal[m] = np.sin(2 * np.pi * freq * t_rel) * np.sin(np.pi * t_rel / 0.35)
save_wav("northern_cardinal.wav", cardinal)

# 3. American Robin: Melodic varied carol chirps (2600 - 3400 Hz)
robin = np.zeros_like(t)
notes = [(0.2, 0.45, 2800), (0.55, 0.8, 3300), (0.95, 1.25, 2700), (1.5, 1.8, 3100), (2.0, 2.35, 2900)]
for st, et, freq in notes:
    m = (t >= st) & (t <= et)
    t_rel = t[m] - st
    dur = et - st
    robin[m] = (np.sin(2 * np.pi * freq * t_rel) + 0.3 * np.sin(2 * np.pi * (freq * 1.5) * t_rel)) * np.sin(np.pi * t_rel / dur)
save_wav("american_robin.wav", robin)

# 4. Great Horned Owl: Deep resonant rhythmic hoots (260 - 340 Hz)
owl = np.zeros_like(t)
hoots = [(0.2, 0.5), (0.65, 0.9), (1.1, 1.35), (1.5, 2.0)]
for st, et in hoots:
    m = (t >= st) & (t <= et)
    dur = et - st
    owl[m] = (np.sin(2 * np.pi * 310 * t[m]) + 0.25 * np.sin(2 * np.pi * 620 * t[m])) * (np.sin(np.pi * (t[m] - st) / dur) ** 2)
save_wav("great_horned_owl.wav", owl)

# 5. Red-Tailed Hawk: Piercing high descending scream (4800 Hz down to 2600 Hz)
hawk = np.zeros_like(t)
m = (t >= 0.3) & (t <= 2.2)
t_rel = t[m] - 0.3
dur = 1.9
freq = 4800 - 2200 * (t_rel / dur)
noise = np.random.normal(0, 0.15, len(t_rel))
hawk[m] = (np.sin(2 * np.pi * freq * t_rel) + noise) * np.sin(np.pi * t_rel / dur)
save_wav("red_tailed_hawk.wav", hawk)

# 6. Woodpecker: Rapid periodic acoustic drumming bursts
woodpecker = np.zeros_like(t)
for tap_time in np.linspace(0.4, 1.8, 22):
    m = (t >= tap_time) & (t <= tap_time + 0.02)
    woodpecker[m] = np.sin(2 * np.pi * 950 * (t[m] - tap_time)) * np.exp(-150 * (t[m] - tap_time))
save_wav("downy_woodpecker.wav", woodpecker)

# 7. Ambient Forest: Soft wind & rustling foliage (Low frequency pink noise)
np.random.seed(42)
white_noise = np.random.normal(0, 1, len(t))
# Simple low-pass filter via moving average
ambient = np.convolve(white_noise, np.ones(80)/80, mode='same')
save_wav("ambient_forest_wind.wav", ambient * 0.3)

print("All sample audio files generated successfully!")
