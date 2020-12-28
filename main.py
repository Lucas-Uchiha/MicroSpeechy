from multiprocessing import Queue
from bg import TaskHandler, create_sound_dir
from ui import Application


def main():
    # create sounds dir if it not exists
    create_sound_dir()

    # initialize UI and BG
    tasks = Queue()
    handler = TaskHandler(tasks)
    app = Application(tasks)

    # initialize processes
    handler.start()
    app.start()

    # stop BG process when UI is closed
    handler.stop()


if __name__ == '__main__':
    main()

