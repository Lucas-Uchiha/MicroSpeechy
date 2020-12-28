#from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
from pygame import mixer  # Playing sound
from gtts import gTTS
from mutagen.mp3 import MP3
from multiprocessing import Process, Queue
from audioplayer import AudioPlayer
import time
import uuid
import os


SOUNDS_PATH = "sounds"
mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")


class TaskHandler(Process):
    def __init__(self, tasks: Queue):
        super(TaskHandler, self).__init__()
        self.queue = tasks
        self._sound_list = []
        self.running = True

    def run(self) -> None:
        print("Starting TaskHandler")

        while self.running:
            item = self.queue.get()
            print(item)
            try:
                path = text_to_voice(item)
                play_sound(path)
            except AssertionError:
                print("deixa de zoar krl")

    def stop(self):
        print("Stoping TaskHandler...")
        self.running = False
        self.terminate()
        self.join()


def play_sound(path=""):
    duration = get_sound_duration(path)
    mixer.music.load(path)      # Load the mp3
    mixer.music.play()
    player = AudioPlayer(path)  # play sound in local speakers
    player.play()
    time.sleep(duration)        # wait until the end


def text_to_voice(text=""):
    file_name = f"{SOUNDS_PATH}/voice-{uuid.uuid4()}.mp3"
    tts = gTTS(text, lang="pt-br")
    tts.save(file_name)

    return file_name


def create_sound_dir():
    if not os.path.isdir(SOUNDS_PATH):
        os.mkdir(SOUNDS_PATH)


def get_sound_duration(path):
    mp3 = MP3(path)
    return mp3.info.length


def main():
    create_sound_dir()
    tasks = Queue()
    handler = TaskHandler(tasks)
    handler.start()
    handler.stop()


if __name__ == '__main__':
    main()
