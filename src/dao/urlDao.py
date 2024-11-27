from src.models.db_models import Instance, ShortURL
from tinydb import Query, table

class UrlDao:
    def __init__(self):
        self.db = Instance

    def insert_to_db(self, obj) -> None:
        obj_dict = obj.model_dump()
        print(f'{obj_dict} inserted')
        self.db.insert(obj_dict)

    def update_to_db(self, doc_id, obj) -> None:
        self.db.upsert(table.Document(obj.model_dump(), doc_id=doc_id))

    def get_long_url_by_shorten_value(self, shorten_value):
        result = self.db.get(Query().shortUrl == shorten_value)
        obj = None
        if result:
            obj = ShortURL(**result)
            doc_id = result.doc_id
            print(f'document id is {doc_id}')
            from src.utils.dateUtil import current_time_in_millis as ct
            if obj.expiry <= ct():
                obj.expired = True
            obj.counter += 1
            self.update_to_db(doc_id, obj)
        return obj

    def get_by_long_url_value(self, long_url):
        result = self.db.get(Query().longUrl == long_url)
        obj = None
        if result:
            obj = ShortURL(**result)
        return obj