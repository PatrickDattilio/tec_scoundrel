from tkinter import LabelFrame, N, BooleanVar, Checkbutton


class Plugin:
    def __init__(self):
        self.alert_enabled = BooleanVar()

    def fatigue_update(self, value):
        if value <= 0:
            self.bell()

    def draw(self, plugin_area):
        label_frame = LabelFrame(plugin_area, text="Alerts")
        label_frame.grid(row=0, column=0, sticky=N)

        self.draw_toggles(label_frame)
        self.draw_text(label_frame)

    def draw_toggles(self, label_frame):
        combat_toggle = Checkbutton(label_frame, text="Alert", variable=self.alert_enabled, command=self.bell)
        combat_toggle.grid(row=0, column=0, sticky=N)

    def bell(self):
        print('\a')