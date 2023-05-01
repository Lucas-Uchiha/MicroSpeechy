import multiprocessing
from multiprocessing import Queue
from bg import TaskHandler, create_sound_dir, read_recs_dir, init_settings
from ui import Application
from os import environ


def main():
    # hide duplicated "Hello from the pygame community" messages.
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    # create sounds dir if it not exists
    create_sound_dir()

    # read recs files
    #recs = ["test.mp3", "abc.mp3", "aba.mp3", "test5.mp3", "abc54.mp3", "ab54a.mp3"]  # TODO: actually read the recs
    recs = read_recs_dir()

    # initialize UI and BG
    tasks = Queue()
    settings = init_settings()
    handler = TaskHandler(tasks, settings)
    app = Application(recs, tasks, settings)

    # initialize processes
    handler.start()
    app.start()

    # stop BG process when UI is closed
    handler.stop()


if __name__ == '__main__':
    multiprocessing.freeze_support()    # Allow pyinstaller use
    main()

