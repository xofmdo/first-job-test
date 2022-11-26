import json

import pandas as pd
from itemadapter import ItemAdapter


class PhonePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("os"):
            if adapter["os"].endswith(".x"):
                adapter["os"] = adapter["os"][:-2]
        return item

class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open("data.json", 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


# class JsonWriterPipeline:
#     def open_spider(self, spider):
#         self.phones = []
#
#     def close_spider(self, spider):
#         with open("data.json", "w", encoding="utf8") as json_file:
#             json.dump(self.phones, json_file, ensure_ascii=False)
#
#     def process_item(self, item, spider):
#         self.phones.append(ItemAdapter(item).asdict())
#         return item


class DataWriterPipeline:
    def open_spider(self, spider):
        self.list_os = []

    def close_spider(self, spider):
        series = pd.Series(self.list_os)
        data = series.value_counts()
        data.to_csv("data.csv")

    def process_item(self, item, spider):
        self.list_os.append(ItemAdapter(item).asdict()["os"])
        return item
