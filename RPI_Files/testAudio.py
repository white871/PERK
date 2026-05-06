from piper import PiperVoice, SynthesisConfig
import wave
import subprocess
model = "en_US-amy-medium.onnx"
voice = PiperVoice.load(model)

syn = SynthesisConfig(volume = 1.5)
with wave.open("ready.wav", "wb") as f:
    voice.synthesize_wav("Ready",f, syn_config=syn)
with wave.open("search.wav", "wb") as f:
    voice.synthesize_wav("Searching for networks", f, syn_config=syn)
with wave.open("off.wav", "wb") as f:
    voice.synthesize_wav("Power off", f, syn_config=syn)
with wave.open("fail.wav", "wb") as f:
    voice.synthesize_wav("No network found", f, syn_config=syn)

