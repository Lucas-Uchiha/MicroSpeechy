from tkinter import Tk, ttk, TOP, NW, SW, BOTTOM, X, SUNKEN, Label, Frame, END, BOTH, LEFT, RAISED
from multiprocessing import Queue, Manager
from typing import List
from utils import KEY_TYPE, KEY_VALUE, MSG, REC

LANGUAGES = [
    "pt",
    "en",
    "es",
    "fr",
    "ja"
]


class Application:
    def __init__(self, recs: List[str], tasks: Queue, settings: Manager):
        self.recs = recs
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
        self._send_msg()

    def on_button_recs_click(self, event, arg):
        self.queue.put({
            KEY_TYPE: REC,
            KEY_VALUE: arg
        })

    def on_enter_key(self, event):
        self._send_msg()

    def _send_msg(self):
        text = self.get_text()

        if len(text) > 0:
            self._insert_in_history(text)
            self.queue.put({
                KEY_TYPE: MSG,
                KEY_VALUE: text
            })

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

        self._render_recs_buttons()

        self._main_frame.pack(fill=BOTH, side=TOP, anchor=NW)
        self.bottom_frame.pack(fill=BOTH, side=BOTTOM, padx=5, pady=5)

        # Configure attributes
        self.window.resizable(height=False, width=True)     # Block window height resize
        self.window.attributes('-topmost', 'true')          # Make window remain on top of other windows.
        self.window.winfo_toplevel().title("MicroSpeechy")  # Set window title
        self._comboBox.current(0)                           # Set default value of comboBox

        self.window.update()
        self.window.minsize(300, 30)
        self.window.mainloop()

    def _render_recs_buttons(self):
        if len(self.recs) < 4:
            num_lines = 1
        else:
            num_lines = int(len(self.recs) / 3)  # divide into 3 columns

        counter = 0

        for row in range(num_lines):
            # TODO: make a better responsive solution
            self.bottom_frame.columnconfigure(row, weight=5)
            self.bottom_frame.rowconfigure(row, weight=1)

            for col in range(4):
                frame = Frame(
                    master=self.bottom_frame,
                    borderwidth=1
                )
                frame.grid(row=row, column=col)

                try:
                    path = self.recs[counter]
                    text = path.replace("recs/", "").replace(".mp3", "")
                    btn = ttk.Button(frame, text=text)
                    btn.bind("<Button-1>", lambda event, arg=path: self.on_button_recs_click(event, arg))
                    btn.pack()
                    counter += 1
                except IndexError:
                    break
