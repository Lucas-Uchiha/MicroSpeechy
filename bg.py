from pygame import mixer  # Playing sound
from gtts import gTTS, gTTSError
from mutagen.mp3 import MP3
from multiprocessing import Process, Queue, Manager
from audioplayer import AudioPlayer
from utils import KEY_TYPE, KEY_VALUE, MSG, REC, STOP
import glob
import time
import uuid
import os
import gtts.tokenizer.symbols as sym
import multiprocessing


# Add custom abbreviations for pt-br
new_abbreviations = [
    ("krl", "caralho"),
    ("blz", "beleza"),
    ("lib", "libe")
]
sym.SUB_PAIRS.extend(new_abbreviations)

# Define sounds path and init mixer
SOUNDS_PATH = "sounds"
mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")


class TaskHandler(Process):
    def __init__(self, tasks: Queue, settings: Manager):
        super(TaskHandler, self).__init__()
        self.queue = tasks          # messages
        self.settings = settings    # UI user configs
        self._sound_list = []
        self.running = True

    def run(self) -> None:
        print("Starting TaskHandler")

        while self.running:
            item = self.queue.get()
            print(item)

            if item[KEY_TYPE] == MSG:
                try:
                    text = item[KEY_VALUE]
                    path = text_to_voice(text, self.settings["lang"])
                    play_sound(path)
                except AssertionError:
                    print("deixa de zoar krl")
                except gTTSError as err:
                    print(f"Error while saving file: \n{err.msg}")
            elif item[KEY_TYPE] == REC:
                path = item[KEY_VALUE]
                play_sound(path)
            elif item[KEY_TYPE] == STOP:
                stop_sound()
            else:
                print("Error in KEY_TYPE in bg.py method run().")

    def stop(self):
        print("Stoping TaskHandler...")
        self.running = False
        self.terminate()
        self.join()


process = {'ref': None}


def play_sound(path=""):
    duration = get_sound_duration(path)

    if process["ref"] is not None:
        process["ref"].kill()

    mixer.music.load(path)      # Load the mp3
    mixer.music.play()
    process["ref"] = multiprocessing.Process(target=play_sound_local, args=(duration, path,))
    process["ref"].start()


def play_sound_local(duration, path=""):
    player = AudioPlayer(path)  # play sound in local speakers
    player.play()
    time.sleep(duration)  # wait until the end


def stop_sound():
    mixer.music.stop()

    if process["ref"] is not None:
        process["ref"].kill()



def text_to_voice(text="", language="pt-br"):
    file_name = f"{SOUNDS_PATH}/voice-{uuid.uuid4()}.mp3"
    tts = gTTS(text, lang=language)
    tts.save(file_name)

    return file_name


def create_sound_dir():
    if not os.path.isdir(SOUNDS_PATH):
        os.mkdir(SOUNDS_PATH)


def read_recs_dir():
    res = []
    data = glob.glob("recs/*.mp3")

    for item in data:
        res.append(item.replace("\\", "/"))

    return res


def get_sound_duration(path):
    mp3 = MP3(path)
    return mp3.info.length


def init_settings():
    settings = Manager().dict()
    settings["lang"] = "pt-br"

    return settings
