from multiprocessing import Queue, Manager
from bg import TaskHandler, create_sound_dir, init_settings
from ui import Application


def main():
    # create sounds dir if it not exists
    create_sound_dir()

    # initialize UI and BG
    tasks = Queue()
    settings = init_settings()
    handler = TaskHandler(tasks, settings)
    app = Application(tasks, settings)

    # initialize processes
    handler.start()
    app.start()

    # stop BG process when UI is closed
    handler.stop()


if __name__ == '__main__':
    main()

