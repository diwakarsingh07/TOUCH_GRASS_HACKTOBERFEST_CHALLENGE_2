"""
TrailWhisper: 100% Offline Earbud Voice Dispatcher
==================================================
Speaks bird identification and field instructions directly into hikers' earbuds
using Windows native offline speech synthesis. Zero internet or cloud APIs required.
"""

import os
import sys
import threading
import subprocess

def speak_offline(text: str):
    """Speaks text in a non-blocking background thread using native Windows speech."""
    def _run():
        try:
            # Escape single quotes for PowerShell
            clean_text = text.replace("'", "")
            cmd = f'powershell -Command "Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Rate = 1; $synth.Speak(\'{clean_text}\')"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            pass # Fail gracefully if audio device busy

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
