import os
import numpy as np
from audio_engine import AudioEngine
from bird_classifier import BirdClassifier
from naturalist import NaturalistEngine

sr = 22050

# 1. Silence test
silence = np.zeros(sr, dtype=np.float32)
feat_silence = AudioEngine.extract_bioacoustic_features(silence, sr)
res_silence = BirdClassifier.classify(feat_silence)
print(f"Silence test               => {res_silence['common_name']}")

# 2. Human Speech simulation (formants at 500 Hz, 1500 Hz, 2200 Hz with moderate noise)
t = np.linspace(0, 2, sr * 2)
speech = (
    0.3 * np.sin(2 * np.pi * 500 * t) +
    0.2 * np.sin(2 * np.pi * 1500 * t) +
    0.1 * np.sin(2 * np.pi * 2200 * t) +
    0.05 * np.random.uniform(-1, 1, len(t))
).astype(np.float32)
feat_speech = AudioEngine.extract_bioacoustic_features(speech, sr)
res_speech = BirdClassifier.classify(feat_speech)
print(f"Human speech simulation    => {res_speech['common_name']}")

# 3. Unrecognized frequency (e.g., 1850 Hz whistle with low bird energy)
weird = (0.3 * np.sin(2 * np.pi * 1850 * t)).astype(np.float32)
feat_weird = AudioEngine.extract_bioacoustic_features(weird, sr)
res_weird = BirdClassifier.classify(feat_weird)
print(f"Unrecognized whistle (1850Hz) => {res_weird['common_name']}")

# 4. Crow caw simulation (800 Hz harsh rasp)
crow = (
    0.4 * np.sin(2 * np.pi * 850 * t) +
    0.3 * np.sin(2 * np.pi * 1700 * t) +
    0.15 * np.random.uniform(-1, 1, len(t))
).astype(np.float32)
feat_crow = AudioEngine.extract_bioacoustic_features(crow, sr)
res_crow = BirdClassifier.classify(feat_crow)
print(f"Crow caw simulation        => {res_crow['common_name']}")

# 5. Rain/Stream simulation (broadband white noise)
rain = (0.2 * np.random.uniform(-1, 1, len(t))).astype(np.float32)
feat_rain = AudioEngine.extract_bioacoustic_features(rain, sr)
res_rain = BirdClassifier.classify(feat_rain)
print(f"Rain/Stream simulation     => {res_rain['common_name']}")
