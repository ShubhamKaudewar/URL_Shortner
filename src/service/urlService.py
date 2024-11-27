
from hashlib import md5
from base64 import urlsafe_b64encode
import logging
logger = logging.getLogger(__name__)
from src.dao.urlDao import UrlDao

class URLService:
    def __init__(self):
        self.url_dao = UrlDao()


    def generate_short_link_model(self, shortUrl, longUrl):
        from src.utils.dateUtil import current_time_in_millis
        from src.models.db_models import ShortURL
        from src.resources.variables import EXPIRY_AFTER

        current_time = current_time_in_millis()
        print(f'current_time: {current_time}')
        short_url_obj = ShortURL(
            shortUrl=shortUrl,
            longUrl=longUrl,
            createTime=current_time,
            expiry=current_time+(EXPIRY_AFTER*3600000),
            expired=False,
            counter=0
        )
        return short_url_obj

    def generate_response_struct(self, url_obj):
        from src.utils.dateUtil import get_date_in_string_from_millis
        from src.resources.variables import DOMAIN
        response_struct = {
            "shortUrl": f'{DOMAIN}/{url_obj.shortUrl}',
            "longUrl": url_obj.longUrl,
            "createdAt": get_date_in_string_from_millis(url_obj.createTime),
            "expiryDateTime": get_date_in_string_from_millis(url_obj.expiry)
        }
        return response_struct

    def generate_short_link(self, long_url):
        model_obj = UrlDao().get_by_long_url_value(long_url)
        if not model_obj:
            hashed = md5(long_url.encode('utf-8')).hexdigest()
            b64_value = urlsafe_b64encode(hashed[:11].encode('utf-8')).decode()
            shorten_value = b64_value[:7]
            print(f'shorten_value: {shorten_value}')
            model_obj = self.generate_short_link_model(shorten_value, long_url)
            self.url_dao.insert_to_db(model_obj)
        response = self.generate_response_struct(model_obj)
        return response
