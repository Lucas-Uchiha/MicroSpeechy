from tkinter import Tk, ttk, TOP, NW, SW, BOTTOM, X, SUNKEN, Label, Frame, END, BOTH, LEFT
from multiprocessing import Queue, Manager

LANGUAGES = [
    "pt",
    "en",
    "es",
    "fr",
    "ja"
]


class Application:
    def __init__(self, tasks: Queue, settings: Manager):
        self.queue = tasks
        self.settings = settings
        self._history_list = []
        self._history_pos = 0
        self.window = Tk()

        # Create frames
        self._main_frame = Frame(master=self.window)
        self.bottom_frame = Frame(master=self.window)
        self._frame1 = Frame(master=self._main_frame, width=200, height=100, borderwidth=6)
        self._frame2 = Frame(master=self._main_frame, width=100, borderwidth=3)
        self._frame3 = Frame(master=self._main_frame, width=100, borderwidth=4)

        # Create UI components
        self.text_box = ttk.Entry(self._frame1)
        self.send_button = ttk.Button(self._frame2, text="Enviar", width=7)
        self._comboBox = ttk.Combobox(self._frame3, values=LANGUAGES, state="readonly", width=5)

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

    def _on_language_selected(self, event):
        value = self._comboBox.get()
        self.settings["lang"] = value

    def start(self):
        print("Starting UI")

        # Bind components
        self.text_box.bind("<Return>", self.on_enter_key)
        self.text_box.bind("<Up>", self._on_key_up)
        self.text_box.bind("<Down>", self._on_key_down)
        self.send_button.bind("<Button-1>", self.on_button_click)
        self._comboBox.bind("<<ComboboxSelected>>", self._on_language_selected)

        # Pack components
        self.text_box.pack(fill=BOTH)
        self.send_button.pack()
        self._comboBox.pack(fill=BOTH)

        self._frame1.pack(fill=BOTH, side=LEFT, expand=True)
        self._frame2.pack(fill=BOTH, side=LEFT, expand=False)
        self._frame3.pack(fill=BOTH, side=LEFT, expand=False)

        self._main_frame.pack(fill=BOTH, side=TOP, anchor=NW)

        # Configure attributes
        self.window.resizable(height=False, width=True)     # Block window height resize
        self.window.attributes('-topmost', 'true')          # Make window remain on top of other windows.
        self.window.winfo_toplevel().title("MicroSpeechy")  # Set window title
        self._comboBox.current(0)                           # Set default value of comboBox

        self.window.update()
        self.window.minsize(300, 30)
        self.window.mainloop()
