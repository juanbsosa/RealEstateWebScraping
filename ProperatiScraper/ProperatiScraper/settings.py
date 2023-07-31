# Scrapy settings for ProperatiScraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "ProperatiScraper"

SPIDER_MODULES = ["ProperatiScraper.spiders"]
NEWSPIDER_MODULE = "ProperatiScraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "ProperatiScraper (+http://www.yourdomain.com)"
# Poner el User Agent de un explorador y no el de scrapy porque sino la pagina te banea
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False # no obedecer el robots.txt de la pagina

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 32
#CONCURRENT_REQUESTS_PER_IP = 16

# Que no falle si se rompe una respuesta
DOWNLOAD_FAIL_ON_DATALOSS = True

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "ProperatiScraper.middlewares.ProperatiscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "ProperatiScraper.middlewares.ProperatiscraperDownloaderMiddleware": 543,
#}

# Middleware para rotar agentes
# (Instalar scrapy-user-agents)
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None, # apagar el middleware de user agents de scrapy
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400, # y prender el que me baje 
}

# USER_AGENTS = [
    # ('Mozilla/5.0 (X11; Linux x86_64) '
    #  'AppleWebKit/537.36 (KHTML, like Gecko) '
    #  'Chrome/57.0.2987.110 '
    #  'Safari/537.36'),  # chrome
    # ('Mozilla/5.0 (X11; Linux x86_64) '
    #  'AppleWebKit/537.36 (KHTML, like Gecko) '
    #  'Chrome/61.0.3163.79 '
    #  'Safari/537.36'),  # chrome
    # ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
    #  'Gecko/20100101 '
    #  'Firefox/55.0')  # firefox
# ]

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "ProperatiScraper.pipelines.ProperatiscraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AutoThrottle is a built-in Scrapy extension that continuously calculates the 
# optimal delay between your requests to minimise the load on the website you 
# are crawling. It does this by adjusting the delay based on the latency of 
# each response and if the response is valid or not.
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Exportar la lista de publicaciones a un csv
from datetime import date
fecha_actual = date.today().isoformat()
anio_mes = date.today().strftime("%Y-%m")

    # Fijarse si ya existe la carpeta para ese mes, sino crearla
import os
if not os.path.exists(f'archivos_scrapeo'):
    os.makedirs(f'archivos_scrapeo')
if not os.path.exists(f'archivos_scrapeo/{anio_mes}'):
    os.makedirs(f'archivos_scrapeo/{anio_mes}')

#    Definir el archivo de destino
FEEDS = {
    f'archivos_scrapeo/{anio_mes}/properati_{fecha_actual}.csv': {'format': 'csv', 
                 'overwrite': False}
}
# FEED_FORMAT = 'csv'

# # FEED_URI = f'archivos_scrapeo/output_{fecha_actual}.csv'
# FEED_URI = f'archivos_scrapeo/probando.csv'

# Limitar la cantidad de requests cada vez que se corre el spider
# CLOSESPIDER_ITEMCOUNT = 25



# Agregar formato al resultado de la consola
import copy
from colorlog import ColoredFormatter
import scrapy.utils.log
# Definir el formato de la consola usando un objeto ColoredFormatter del paquete colorlog
color_formatter = ColoredFormatter(
    (   '%(log_color)s%(levelname)-5s%(reset)s '
        '%(yellow)s[%(asctime)s]%(reset)s'
        '%(white)s %(name)s %(funcName)s %(bold_purple)s:%(lineno)d%(reset)s '
        '%(log_color)s%(message)s%(reset)s'),
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={'DEBUG': 'green',
                'INFO': 'bold_cyan',
                'WARNING': 'red',
                'ERROR': 'bg_bold_red',
                'CRITICAL': 'red,bg_white',})
# Hacer una shallow copy del metodo get handler de scrapy
_get_handler = copy.copy(scrapy.utils.log._get_handler)
# Crear una nueva funcion get_handler_custom, que tenga todos los argumentos
#   de la funcion original, excepto por el Formatter
def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    handler.setFormatter(color_formatter)
    return handler
# Definir el metodo _get_handler de scrapy como la nueva funcion
scrapy.utils.log._get_handler = _get_handler_custom
