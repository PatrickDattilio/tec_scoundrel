import datetime
import os

import pyglet


class Alert:
    def __init__(self, scoundrel_print):
        self.scoundrel_print = scoundrel_print
        self.tag = "[A] "
        self.beep = pyglet.media.load(
            os.path.dirname(os.path.realpath("__file__")) + '/plugins/tec_scoundrel/alert/chime.wav', streaming=False)
        self.enemies = ["plump brown", "pale white rat", "sickly yellow rat", "gaunt grey rat", "mottled wiry rat",
                        "grimy rat", "mangy looking rat", "filth-covered rat", "ragged looking rat"]

    def fatigue_update(self, value):
        self.alert_print("Fatigue: " + value)
        if int(value) <= 0:
            self.alert_print("Exhausted!")
            self.bell()

    def post_process(self, line):
        skip = False
        for enemy in self.enemies:
            if enemy in line:
                skip = True
                break
        if not skip:
            if "to you" in line:
                self.alert_print("To You: " + line)
                self.bell()
            elif "walks in" in line:
                self.alert_print("Incoming: " + line)
                self.bell()
            elif ("say" in line or "whisper" in line) and "thinks aloud:" not in line:
                self.alert_print("Communication: " + line)
                self.bell()

    def bell(self):
        self.beep.play()

    def alert_print(self, text):
        self.scoundrel_print(self.tag + text)

    def toggle(self, enabled):
        self.alert_print(str(datetime.datetime.now())[11:-7] + (" Enabled" if enabled.get() else " Disabled"))
        self.bell()