# Source: https://www.youtube.com/watch?v=D22QqJ18rFg&list=PLj4hN6FewnwoUArmA8kifDHZYvRn6egg5&index=31

# Este script tiene que estar en la misma carpeta que scrapy.cfg

from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings

# Importar la clase del spider
from ProperatiScraper.spiders.Properati_spider import ProperatiSpider


# Esto se va a correr en la consola
def main():
    # Llamar al archivo settings.py del proyecto
    settings = get_project_settings()
    # Iniciar un crawler (equivalente a escribir "scrapy crawl ..." en la consola)
    process = CrawlerProcess(settings)
    # Iniciar el spider
    process.crawl(ProperatiSpider)
    process.start()

# Verificar si este archivo se esta corriendo en la consola, y correr la funcion main()
#   (esto es una formula tipica cuando queremos correr un .py en la consola)
if __name__ == '__main__':
    main()