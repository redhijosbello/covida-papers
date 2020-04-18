from datetime import datetime
from typing import Optional


class PaperData:
    def __init__(self, title: str, link: str, dateTime: Optional[datetime]):
        self.title = title
        self.link = link
        self.dateTime = dateTime

    def toDTO(self) -> dict:
        return {
            'title': self.title,
            'link': self.link,
            'dateTime': self.dateTime.strftime('%m/%d/%Y') if self.dateTime is not None else None
        }
