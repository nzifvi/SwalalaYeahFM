import os
os.environ['PATH'] = r'C:\Users\benja\AppData\Local\Programs\Python\Python313\Lib\site-packages\static_sox\bin\sox-14.4.2-win32' + ';' + os.environ['PATH']

import soundfile
import torch
print("Importing model...")
from qwen_tts import Qwen3TTSModel

print("Loading model weights...")
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    token="your_new_token_here",
    device_map="cuda",
    torch_dtype=torch.bfloat16
)
print("Model loaded!")

def speak(model: Qwen3TTSModel, text: str, speaker: str = "uncle_fu", outputPath: str = "output.wav") -> str:
    print(f"Generating speech for: {text}")
    wavs, sample_rate = model.generate_custom_voice(
        text=text,
        speaker=speaker,
        language="english",
        do_sample=True
    )
    print("Speech generated, writing file...")
    soundfile.write(outputPath, wavs[0], sample_rate)
    print(f"Done! Saved to {outputPath}")
    return outputPath

speak(model, "hello. i am a soldier. i have been homeless for nearly 1000 nights. 1000 nights i have nearly been homeless. i served in syria. syria")