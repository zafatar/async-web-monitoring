"""Link entity and LinkAccessLog entity"""

from datetime import datetime

from pydantic import BaseModel


class Link(BaseModel):
    id: int
    title: str
    description: str
    url: str
    search_regex: str
    access_interval: int
    created_at: datetime
    updated_at: datetime

    def __str__(self):
        return f"""{self.__class__.__name__} #{self.id} |
                   {self.title} |
                   {self.url} |
                   {self.access_interval}"""


class LinkAccessLog(BaseModel):
    link_id: int
    status_code: int
    content: str
    created_at: datetime
    updated_at: datetime
