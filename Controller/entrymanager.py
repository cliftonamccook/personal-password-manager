class EntryManager:
    def __init__(self):
        self.entries = []

    def flush(self):
        self.entries.clear()

    def createEntry(self, i):
        return Entry(
            i["name"],
            i["url"],
            i["username"],
            i["password"],
            i["notes"],
            i["id"]
        )


class Entry:
    def __init__(self, name, url, username, password, notes, id=None):
        self.id = id
        self.name = name
        self.url = url
        self.username = username
        self.password = password
        self.notes = notes

    def encode(self):
        self.name = self.name.encode()
        self.url = self.url.encode()
        self.username = self.username.encode()
        self.password = self.password.encode()
        self.notes = self.notes.encode()
