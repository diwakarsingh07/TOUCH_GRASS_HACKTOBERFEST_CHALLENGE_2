"""
TrailWhisper: Offline Audio & Bioacoustic Spectrogram Engine
============================================================
Processes raw trail audio entirely locally without cloud dependencies.
Supports WAV, MP3, M4A, OGG, and FLAC recorded directly from mobile phones.
"""

import io
import numpy as np

try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False

from scipy.io import wavfile
from scipy.signal import spectrogram
from typing import Tuple, Dict, Any

class AudioEngine:
    @staticmethod
    def load_audio(file_path: str) -> Tuple[int, np.ndarray]:
        """Loads WAV audio file and converts to mono float normalized between -1.0 and 1.0."""
        sr, data = wavfile.read(file_path)
        if data.ndim > 1:
            data = data.mean(axis=1) # Convert stereo to mono
        if np.issubdtype(data.dtype, np.integer):
            max_val = np.iinfo(data.dtype).max
            data = data.astype(np.float32) / max_val
        else:
            data = data.astype(np.float32)
        return sr, data

    @staticmethod
    def load_audio_from_buffer(buffer) -> Tuple[int, np.ndarray]:
        """
        Loads audio from an in-memory buffer (e.g. uploaded or recorded on mobile).
        Supports WAV, OGG, FLAC, MP3, M4A using soundfile / scipy.
        """
        # Try soundfile first (supports WAV, OGG, FLAC)
        if HAS_SOUNDFILE:
            try:
                buffer.seek(0)
                data, sr = sf.read(buffer)
                if data.ndim > 1:
                    data = data.mean(axis=1)
                return sr, data.astype(np.float32)
            except Exception:
                pass

        # Fallback to scipy wavfile
        try:
            buffer.seek(0)
            sr, data = wavfile.read(buffer)
            if data.ndim > 1:
                data = data.mean(axis=1)
            if np.issubdtype(data.dtype, np.integer):
                data = data.astype(np.float32) / np.iinfo(data.dtype).max
            return sr, data.astype(np.float32)
        except Exception:
            pass

        # Fallback to pydub for MP3 / M4A
        try:
            from pydub import AudioSegment
            buffer.seek(0)
            seg = AudioSegment.from_file(buffer)
            seg = seg.set_channels(1)
            samples = np.array(seg.get_array_of_samples(), dtype=np.float32)
            max_val = float(2 ** (seg.sample_width * 8 - 1))
            return seg.frame_rate, samples / max_val
        except Exception as e:
            raise ValueError(f"Could not decode audio format: {e}")

    @staticmethod
    def compute_spectrogram(audio: np.ndarray, sample_rate: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes 2D Spectrogram (frequencies, times, decibel intensities).
        Optimized for avian vocalization range (200 Hz to 10 kHz).
        """
        nperseg = int(sample_rate * 0.025) # 25ms windows
        noverlap = int(sample_rate * 0.015) # 15ms overlap
        
        freqs, times, Sxx = spectrogram(audio, fs=sample_rate, nperseg=nperseg, noverlap=noverlap)
        
        # Limit to 0 - 10,000 Hz
        mask = freqs <= 10000
        freqs = freqs[mask]
        Sxx = Sxx[mask, :]
        
        # Convert to Decibels (dB) with safe floor
        Sxx_db = 10 * np.log10(Sxx + 1e-9)
        return freqs, times, Sxx_db

    @staticmethod
    def extract_bioacoustic_features(audio: np.ndarray, sample_rate: int) -> Dict[str, Any]:
        """
        Extracts rich mathematical fingerprints of animal & wilderness calls:
        - RMS energy (silence vs active sound)
        - Peak frequency (Hz)
        - Spectral centroid (Hz) & Spectral Rolloff (85%)
        - Spectral Flatness (tonal bird whistle vs noisy speech/wind)
        - Energy distribution across bioacoustic bands
        - Zero crossing rate & temporal drumming rhythm
        """
        # Ensure 1D audio
        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        # 1. RMS Energy
        rms = float(np.sqrt(np.mean(audio ** 2)))

        fft_vals = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), 1.0 / sample_rate)

        # 2. Peak Frequency
        peak_idx = int(np.argmax(fft_vals))
        peak_freq = float(freqs[peak_idx])

        # 3. Spectral Centroid
        total_mag = np.sum(fft_vals) + 1e-9
        spectral_centroid = float(np.sum(freqs * fft_vals) / total_mag)

        # 4. Spectral Flatness (Tonal purity measure)
        # Bird whistles have near-zero flatness (< 0.05); wind/speech has higher flatness (> 0.15)
        mag_pos = fft_vals[fft_vals > 1e-7]
        if len(mag_pos) > 0:
            power = mag_pos ** 2
            geo_mean = np.exp(np.mean(np.log(power + 1e-12)))
            arith_mean = np.mean(power) + 1e-12
            spectral_flatness = float(geo_mean / arith_mean)
        else:
            spectral_flatness = 0.0

        # 5. Energy Bands
        total_power = np.sum(fft_vals ** 2) + 1e-9
        sub_bass_power = np.sum(fft_vals[freqs < 250] ** 2)
        low_power = np.sum(fft_vals[(freqs >= 200) & (freqs < 800)] ** 2)
        speech_power = np.sum(fft_vals[(freqs >= 300) & (freqs < 2400)] ** 2)
        bird_power = np.sum(fft_vals[(freqs >= 1500) & (freqs <= 8000)] ** 2)
        ultra_high_power = np.sum(fft_vals[(freqs >= 5500) & (freqs <= 10000)] ** 2)

        sub_bass_ratio = float(sub_bass_power / total_power)
        low_ratio = float(low_power / total_power)
        speech_ratio = float(speech_power / total_power)
        bird_ratio = float(bird_power / total_power)
        ultra_high_ratio = float(ultra_high_power / total_power)

        # 6. Zero Crossing Rate
        zero_crossings = np.sum(np.abs(np.diff(np.sign(audio)))) / (2.0 * len(audio))

        # 7. Temporal Pulse / Drumming rhythm
        frame_len = max(int(sample_rate * 0.05), 10)
        hop = max(int(sample_rate * 0.025), 5)
        if len(audio) > frame_len:
            envelope = [np.max(np.abs(audio[i:i+frame_len])) for i in range(0, len(audio)-frame_len, hop)]
            env = np.array(envelope)
            peaks = (env[1:-1] > env[:-2]) & (env[1:-1] > env[2:]) & (env[1:-1] > 0.12)
            pulse_count = int(np.sum(peaks))
        else:
            pulse_count = 0

        return {
            "rms_energy": round(rms, 4),
            "peak_frequency_hz": round(peak_freq, 1),
            "spectral_centroid_hz": round(spectral_centroid, 1),
            "spectral_flatness": round(spectral_flatness, 5),
            "zero_crossing_rate": round(float(zero_crossings), 4),
            "bird_band_energy_ratio": round(bird_ratio, 3),
            "speech_band_energy_ratio": round(speech_ratio, 3),
            "low_band_energy_ratio": round(low_ratio, 3),
            "sub_bass_energy_ratio": round(sub_bass_ratio, 3),
            "ultra_high_energy_ratio": round(ultra_high_ratio, 3),
            "pulse_count": pulse_count,
            "duration_seconds": round(len(audio) / sample_rate, 2)
        }

