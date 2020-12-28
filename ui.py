from tkinter import Tk, Button, Entry, Frame, END, BOTH, LEFT
from multiprocessing import Queue


class Application:
    def __init__(self, tasks: Queue):
        self.queue = tasks
        self._history_list = []
        self._history_pos = 0
        self.window = Tk()
        self._frame1 = Frame(master=self.window, width=200, height=100, borderwidth=6)
        self._frame2 = Frame(master=self.window, width=100, borderwidth=3)
        self.text_box = Entry(self._frame1)
        self.send_button = Button(self._frame2, text="Send")

    def get_text(self):
        text = self.text_box.get()
        self.text_box.delete(0, END)
        return text

    def _insert_in_history(self, text):
        self._history_list.append(text)
        self._history_pos = 0

    def on_button_click(self, event):
        text = self.get_text()

        if len(text) > 0:
            self._insert_in_history(text)
            self.queue.put(text)

    def on_enter_key(self, event):
        text = self.get_text()

        if len(text) > 0:
            self._insert_in_history(text)
            self.queue.put(text)

    def _on_key_up(self, event):
        self._history_pos += 1

        # let user go to the top of list
        if self._history_pos < len(self._history_list) + 1:
            item = self._history_list[- self._history_pos]
            self.text_box.delete(0, END)
            self.text_box.insert(0, item)
        else:
            self._history_pos -= 1

    def _on_key_down(self, event):
        self._history_pos -= 1

        # let user go back in the list
        if self._history_pos > 0:
            item = self._history_list[- self._history_pos]
        else:
            item = ""
            self._history_pos = 0

        self.text_box.delete(0, END)
        self.text_box.insert(0, item)

    def start(self):
        print("Starting UI")
        # Make window remain on top until destroyed, or attribute changes.
        self.window.attributes('-topmost', 'true')

        self.window.winfo_toplevel().title("MicroSpeechy")
        self.text_box.bind("<Return>", self.on_enter_key)
        self.text_box.bind("<Up>", self._on_key_up)
        self.text_box.bind("<Down>", self._on_key_down)
        self.send_button.bind("<Button-1>", self.on_button_click)
        self.text_box.pack(fill=BOTH)
        self.send_button.pack()
        self._frame1.pack(fill=BOTH, side=LEFT, expand=True)
        self._frame2.pack(fill=BOTH, side=LEFT, expand=False)
        self.window.resizable(height=False, width=True)

        self.window.update()
        self.window.minsize(300, 30)
        self.window.mainloop()


def test_ui():
    q = Queue()
    app = Application(q)
    app.start()


if __name__ == "__main__":
    test_ui()
