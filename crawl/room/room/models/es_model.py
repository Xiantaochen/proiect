from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text,DocType

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

class RoomType(DocType):
    """添加es映射"""
    creat_Date = Text()
    pass

    class Meta:
        index = "lianjia"
        doc_type = "room"


if __name__ == '__main__':
    RoomType.init()