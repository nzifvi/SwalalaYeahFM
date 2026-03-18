import soundfile
import torch
print("Importing model...")
from qwen_tts import Qwen3TTSModel
import random
from transformers import BitsAndBytesConfig
import librosa

class Queue:
    def __init__(self):
        self.queue = []

    def dequeue(self):
        return self.queue.pop(0)

    def enqueue(self, item):
        self.queue.append(item)

    def size(self):
        return len(self.queue)

class Speaker:
    def __init__(self, speakerName:str):
        self.speakerName = speakerName
        uncompiledModel = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
            token="your_new_token_here",
            device_map="cuda",
            dtype=torch.bfloat16
        )
        uncompiledModel.model = torch.compile(uncompiledModel.model)
        self.model = uncompiledModel
        self.pastStories = []
        self.randomWords = [
            "AHHHHH!!!!!!!",
            "oh, oh, oh, oh, oh",
            "durhhhhhh",
            "hahahahahahaha... HAHAHAHAHAHAHA..."
        ]
        self.processingQueue = Queue()

    def speak(self, outputPath:str) -> str:
        i = 0
        while self.processingQueue.size() > 0:
            wavs, sampleRate = self.model.generate_custom_voice(
                text=self.processingQueue.dequeue(),
                speaker = self.speakerName,
                language = "english",
                do_sample = False
            )
            i += 1
            wav = librosa.effects.pitch_shift(wavs[0], sr=sampleRate, n_steps=4)
            soundfile.write(
                outputPath + str(i) + ".wav",
                wav,
                sampleRate
            )

    def parseStories(self, stories:list) -> list:
        newStories = []
        for story in stories:
            if story["title"] not in self.pastStories:
                newStories.append(story)
                self.pastStories.append(
                    story["title"]
                )
        return newStories

    def mergeStories(self, stories:list) -> None:
        self.processingQueue.enqueue(item = "New stories for you! ")
        for story in stories:
            script = ""
            script += story["title"] + ": " + story["summary"] + "..." + random.choice(self.randomWords) + "..."
            self.processingQueue.enqueue(item = script)
        self.processingQueue.enqueue(item = "That is all!")

    def clearAudioFiles(self, filePath:str) -> None:
        pass

