# date: yyyy/mm/dd

class Reminder:
    def __init__(self, message, title, time, nag_interval):
        self.author = message.author
        self.title = title
        self.time = time
        self.nag_interval = nag_interval
