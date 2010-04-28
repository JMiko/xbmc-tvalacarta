class Item(object):
    title = ""
    url = ""
    thumbnail = ""
    plot = ""

    def __init__(self, title="", url="", thumbnail="", plot=""):
        self.title = title
        self.url = url
        self.thumbnail = thumbnail
        self.plot = plot
