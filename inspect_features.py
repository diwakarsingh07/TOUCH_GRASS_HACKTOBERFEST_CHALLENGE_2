import os
from audio_engine import AudioEngine
from bird_classifier import BirdClassifier
from naturalist import NaturalistEngine

p = r"D:\trailwhisper\demo_sounds"
print("-" * 75)
print(f"{'FILE NAME':<28} | {'CLASSIFIED SPECIES':<25} | {'CONFIDENCE'}")
print("-" * 75)
for f in sorted(os.listdir(p)):
    if f.endswith(".wav"):
        sr, audio = AudioEngine.load_audio(os.path.join(p, f))
        feat = AudioEngine.extract_bioacoustic_features(audio, sr)
        res = BirdClassifier.classify(feat)
        guide = NaturalistEngine.get_field_guidance(res)
        print(f"{f:<28} | {res['common_name']:<25} | {res['confidence_pct']}")
print("-" * 75)
