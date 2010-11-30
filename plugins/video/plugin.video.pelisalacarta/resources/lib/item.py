class Item(object):
    channel = ""
    title = ""
    url = ""
    thumbnail = ""
    plot = ""
    duration = ""
    fanart = ""
    folder = True
    action = ""
    server = ""
    extra = ""
    category = ""
    show = ""

    def __init__(self, channel="", title="", url="", thumbnail="", plot="", duration="", fanart="", action="", server="", extra="", category = "", show = "" , folder=True):
        self.channel = channel
        self.title = title
        self.url = url
        self.thumbnail = thumbnail
        self.plot = plot
        self.duration = duration
        self.fanart = fanart
        self.folder = folder
        self.server = server
        self.action = action
        self.extra = extra
        self.category = category
        self.show = show

    def tostring(self):
        return "title=["+self.title+"], url=["+self.url+"], thumbnail=["+self.thumbnail+"]"