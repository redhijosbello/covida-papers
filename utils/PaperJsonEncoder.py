from json import JSONEncoder


class PaperJsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
