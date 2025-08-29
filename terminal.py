from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import datetime, random, time

Window.size = (360, 640)

class Terminal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.start_time = time.time()
        self.history = []

        # Вивід команд
        self.output_scroll = ScrollView(size_hint=(1, 0.9))
        self.output_label = Label(size_hint_y=None, text="", markup=True)
        self.output_label.bind(texture_size=self.update_height)
        self.output_scroll.add_widget(self.output_label)
        self.add_widget(self.output_scroll)

        # Панель вводу
        self.input_box = BoxLayout(size_hint=(1, 0.1))
        self.cmd_input = TextInput(multiline=False)
        self.cmd_input.bind(on_text_validate=self.run_command)
        self.run_btn = Button(text="▶")
        self.run_btn.bind(on_release=self.run_command)
        self.input_box.add_widget(self.cmd_input)
        self.input_box.add_widget(self.run_btn)
        self.add_widget(self.input_box)

    def update_height(self, instance, value):
        self.output_label.height = self.output_label.texture_size[1]
        self.output_scroll.scroll_y = 0

    def run_command(self, instance=None):
        cmd = self.cmd_input.text.strip()
        if not cmd:
            return
        self.output_label.text += f"\n$ {cmd}"
        self.history.append(cmd)

        parts = cmd.split()
        base = parts[0]
        args = parts[1:]

        result = self.execute(base, args)
        if result:
            self.output_label.text += f"\n{result}"

        self.cmd_input.text = ""

    def execute(self, base, args):
        try:
            # 14 стабільних команд
            if base == "help":
                return "Команди: help, echo, date, time, random, clear, about, whoami, pwd, ls, cd, touch, cat, rm"
            elif base == "echo":
                return " ".join(args)
            elif base == "date":
                return datetime.date.today().strftime("%Y-%m-%d")
            elif base == "time":
                return datetime.datetime.now().strftime("%H:%M:%S")
            elif base == "random":
                return str(random.randint(0, 100))
            elif base == "clear":
                self.output_label.text = ""
                return ""
            elif base == "about":
                return "Android Terminal (Kivy Classic)"
            elif base == "whoami":
                return "pydroid_user"
            elif base == "pwd":
                return "~"
            elif base == "ls":
                return "file1.txt\nfile2.txt\nfolder1"
            elif base == "cd":
                return "Поточна папка змінена (імітація)"
            elif base == "touch":
                return f"Файл {args[0] if args else 'newfile.txt'} створено"
            elif base == "cat":
                return f"Вміст файлу {args[0] if args else 'file.txt'}:\nHello World"
            elif base == "rm":
                return f"Файл {args[0] if args else 'file.txt'} видалено"
            else:
                return f"{base}: command not found"

        except Exception as e:
            return f"Error: {e}"

class TerminalApp(App):
    def build(self):
        return Terminal()

if __name__ == "__main__":
    TerminalApp().run()