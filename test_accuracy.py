import os
from audio_engine import AudioEngine
from bird_classifier import BirdClassifier
from naturalist import NaturalistEngine

demo_dir = r"D:\trailwhisper\demo_sounds"
for fname in sorted(os.listdir(demo_dir)):
    if fname.endswith(".wav"):
        sr, audio = AudioEngine.load_audio(os.path.join(demo_dir, fname))
        features = AudioEngine.extract_bioacoustic_features(audio, sr)
        res = BirdClassifier.classify(features)
        guide = NaturalistEngine.get_field_guidance(res)
        print(f"{fname:28s} => {res['common_name']:34s} ({res['confidence_pct']})")
