# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# Definir las variables de cada item
class ItemPublicacion(scrapy.Item):
    url = scrapy.Field()
    url_primera_imagen = scrapy.Field()
    titulo = scrapy.Field()
    precio = scrapy.Field()
    precio_frecuencia_mensual = scrapy.Field()
    ubicacion = scrapy.Field()
    dormitorios = scrapy.Field()
    banios = scrapy.Field()
    area = scrapy.Field()
    tipo_propiedad = scrapy.Field()
    tipo_operacion = scrapy.Field()
    anio_construccion = scrapy.Field()
    tiempo_desde_publicacion_y_usuario_publicador = scrapy.Field()
    descripcion = scrapy.Field()
    caracteristicas_de_la_vivienda = scrapy.Field()
    ubicacion2 = scrapy.Field()
    fecha_scrapeo = scrapy.Field()

    # Elegir que atributos del item mostrar en la consola
    # def __repr__(self):
    #     return repr({"titulo": self.titulo,
    #                     "url": self.url})
    def __repr__(self):
        return repr({"titulo": self.get("titulo"),
                        "url": self.get("url")})
