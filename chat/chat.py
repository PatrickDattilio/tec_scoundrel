__author__ = 'Pmoney'


class Chat:
    def __init__(self, scoundrel_print):
        self.scoundrel_print = scoundrel_print
        self.tag = "[T] "

    def post_process(self, line):
        if "thinks aloud:" in line:
            self.scoundrel_print(self.tag + line, "think")