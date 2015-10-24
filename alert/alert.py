import datetime


class Alert:
    def __init__(self, scoundrel_print):
        self.scoundrel_print = scoundrel_print
        self.tag = "[A] "

    def fatigue_update(self, value):
        self.alert_print("Fatigue: "+value)
        if int(value) <= 0:
            self.alert_print("Exhausted!")
            self.bell()

    def post_process(self, line):
        if "to you" in line:
            self.bell()
        elif "walks in" in line:
            self.bell()

    def bell(self):
        print('\a')

    def alert_print(self, text):
        self.scoundrel_print(self.tag + text)

    def toggle(self, enabled):
        self.alert_print(str(datetime.datetime.now())[11:-7] + (" Enabled" if enabled.get() else " Disabled"))