import tkinter as tk

from chat.chat import Chat

from combat.action import Action
from alert.alert import Alert
from combat import Combat


class Plugin:
    def __init__(self):
        self.in_combat = False
        self.free = True
        self.action = Action.nothing
        self.queue = []
        self.combat = Combat(self.scoundrel_print, self.add_action, self.remove_action, self.queue, self.free,
                             self.action)
        self.combat_enabled = tk.BooleanVar()
        self.alert = Alert(self.scoundrel_print)
        self.chat = Chat(self.scoundrel_print_with_tag)
        self.alert_enabled = tk.BooleanVar()

    def set_send_command(self, send_command):
        self.send_command = send_command
        self.combat.set_send_command(send_command)

    def set_echo(self, echo):
        self.echo = echo
        self.combat.set_echo(echo)

    def fatigue_update(self, value):
        if self.alert_enabled.get():
            self.alert.fatigue_update(value)

    def post_process(self, line):
        if self.alert_enabled.get():
            self.alert.post_process(line)

        if self.in_combat and self.combat_enabled.get():
            self.combat.handle_combat_line(line)
        elif "You are no longer busy" in line:
            self.free = True
            # self.perform_action()
        elif ("] A" in line) and "You retrieve the line" not in line:
            self.scoundrel_print("Combat")
            self.in_combat = True
        elif "retreat" in line and "You retreat." not in line and "retreat first" not in line and "retreats." not in line:
            self.scoundrel_print("Retreating")
            self.add_action(Action.retreat)

    def add_action(self, action):
        if action not in self.queue:
            self.queue.append(action)
            self.queue.sort()

    def remove_action(self, action):
        if action in self.queue:
            self.queue.remove(action)
            self.queue.sort()

    def draw(self, plugin_area):
        label_frame = tk.LabelFrame(plugin_area, text="Scoundrel")
        label_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.S)
        self.draw_toggles(label_frame)
        self.draw_text(label_frame)

    def draw_toggles(self, label_frame):
        combat_toggle = tk.Checkbutton(label_frame, text="Combat", variable=self.combat_enabled,
                                       command=lambda enabled=self.combat_enabled: self.combat.toggle(enabled))
        combat_toggle.grid(row=0, column=0, sticky=tk.N)
        alert_toggle = tk.Checkbutton(label_frame, text="Alert", variable=self.alert_enabled,
                                      command=lambda enabled=self.alert_enabled: self.alert.toggle(enabled))
        alert_toggle.grid(row=0, column=3, sticky=tk.N)

    def draw_text(self, label_frame):
        scrollbar = tk.Scrollbar(label_frame)
        scrollbar.grid(row=1, column=4, sticky=tk.N + tk.S)
        self.scoundrel_output = tk.Text(
            label_frame,
            name="scoundrel_output",
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        self.scoundrel_output.tag_configure('think', fill='blue')
        scrollbar.config(command=self.scoundrel_output.yview)
        self.scoundrel_output.scrollbar = scrollbar
        self.scoundrel_output.grid(row=1, column=0, columnspan=5, sticky=tk.N + tk.W + tk.S)

    def scroll_output(self):
        self.scoundrel_output.see(tk.END)

    def scoundrel_print(self, line):
        self.scoundrel_print_with_tag(line, None)

    def scoundrel_print_with_tag(self, line, tag):
        self.scoundrel_output.insert(tk.END, line + "\n", tag)
        self.scroll_output()

    def perform_action(self):
        if self.in_combat and self.combat_enabled.get():
            self.combat.perform_action()
