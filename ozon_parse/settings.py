BOT_NAME = 'ozon_parse'

SPIDER_MODULES = ['ozon_parse.spiders']
NEWSPIDER_MODULE = 'ozon_parse.spiders'

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

DOWNLOADER_MIDDLEWARES = {"ozon_parse.middlewares.SeleniumMiddleWare": 200}

ITEM_PIPELINES = {
    "ozon_parse.pipelines.PhonePipeline": 100,
    "ozon_parse.pipelines.JsonWriterPipeline": 300,
    "ozon_parse.pipelines.DataWriterPipeline": 500,
}
