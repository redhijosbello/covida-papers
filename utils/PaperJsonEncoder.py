from json import JSONEncoder

from dataTypes.PaperData import PaperData


class PaperJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, PaperData):
            return o.toDTO()
        return o.__dict__
