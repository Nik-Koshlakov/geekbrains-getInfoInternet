import scrapy
import hashlib
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class AvitoparserPipeline:
    def process_item(self, item, spider):
        if item['character_name']:
            tmp = []
            for i in range(len(item['character_name'])):
                tmp.append({
                    "character_name": item['character_name'][i],
                    "character_value": item['character_value'][i]})
        return item


class AvitoPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{item["name"]}/{image_guid}.jpg'
