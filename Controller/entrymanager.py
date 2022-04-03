import re

class EntryManager:
    def __init__(self) -> None:
        self.entries = []

    def flush(self) -> None:
        self.entries.clear()

    def cache(self, entry):
        self.entries.append(entry)

    def filterEntries(self, string):
        txt = string
        for i in self.entries:
            if not any([
                re.search(txt, i.name.decode()),
                re.search(txt, i.url.decode()),
                re.search(txt, i.username.decode()),
                re.search(txt, i.password.decode()),
                re.search(txt, i.notes.decode())
            ]):
                self.entries.remove(i)

    def createEntry(self, i: dict):
        return Entry(
            i["name"],
            i["url"],
            i["username"],
            i["password"],
            i["notes"]
        )

    def createEntryFromDB(self, i: dict):
        return Entry(
            i["name"],
            i["url"],
            i["username"],
            i["password"],
            i["notes"],
            i["id"]
        )


class Entry:
    def __init__(self, name: str, url: str, username: str, password: str, notes: str, id=None) -> None:
        self.id = id
        self.name = name
        self.url = url
        self.username = username
        self.password = password
        self.notes = notes

    def encode(self) -> None:
        self.name = self.name.encode()
        self.url = self.url.encode()
        self.username = self.username.encode()
        self.password = self.password.encode()
        self.notes = self.notes.encode()
