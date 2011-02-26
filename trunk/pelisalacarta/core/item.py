class Item(object):
    channel = ""
    title = ""
    url = ""
    page = ""
    thumbnail = ""
    plot = ""
    duration = ""
    fanart = ""
    folder = ""
    action = ""
    server = "directo"
    extra = ""
    show = ""
    category = ""
    childcount = 0
    language = ""
    type = ""
    context = 0

    def __init__(self, channel="", title="", url="", page="", thumbnail="", plot="", duration="", fanart="", action="", server="directo", extra="", show="", category = "" , language="" , type = "" , folder=True, context = 0):
        self.channel = channel
        self.title = title
        self.url = url
        if page=="":
            self.page = url
        else:
            self.page = page
        self.thumbnail = thumbnail
        self.plot = plot
        self.duration = duration
        self.fanart = fanart
        self.folder = folder
        self.server = server
        self.action = action
        self.extra = extra
        self.show = show
        self.category = category
        self.childcount = 0
        self.language = language
        self.type = type
        self.context = context

    def tostring(self):
        return "title=["+self.title+"], url=["+self.url+"], thumbnail=["+self.thumbnail+"], action=["+self.action+"], show=["+self.show+"], category=["+self.category+"]"