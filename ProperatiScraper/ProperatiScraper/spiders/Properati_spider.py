# PENDIENTES:
# - Agregar docstrings a todas las funciones y clases
# - Ver si agregar prints utiles, como el url front que se esta escrapeando

import os
from datetime import date
import random
import logging
import glob
import pandas as pd

import scrapy
from scrapy.utils.log import configure_logging

from ..items import ItemPublicacion

class ProperatiSpider(scrapy.Spider):

    # Definir nombre del spider para llamarlo desde la consola de scrapy
    name = 'ProperatiSpider'
    publicaciones_visitadas_antes = set()
    cant_publicaciones_visitadas_hoy = 0
    cant_publicaciones_visitadas_sin_info_hoy = 0
    limite_publicaciones_sin_info = 100
    url_madre = 'https://www.properati.com.ar'

    # LOGGING: guardar el log de la consola por si se quiere chequear posteriormente
    # El objetivo es guardarlo, pero que tambien se vea el resultado en la consola

    # Crear nombre del archivo para guardar el log
    fecha_actual = date.today().isoformat()
    if not os.path.exists('log_files'):
        os.makedirs('log_files')
    log_filename = f'log_files/scrapy_log_{fecha_actual}.txt'

    # Cambiar la configuracion default de scrapy que solo imprime el log en la 
    #   consola pero no lo guarda
    configure_logging(settings={
        "LOG_STDOUT": True
    })
    # Si no quisiesemos que se vea el resultado en la consola, bastaria con esto
    # configure_logging(install_root_handler=False)
    # # Configurar el sistema de logging
    # logging.basicConfig(
    #     filename=log_filename, 
    #     filemode='a',
    #     format='[%(asctime)s] [%(name)s] %(levelname)s:    %(message)s',
    #     datefmt = '%H:%M:%S',
    #     level=logging.INFO
    # )

    # Cambiar la configuracion del log usando el paquete logging de Python base
    file_handler = logging.FileHandler(log_filename, 
                                       mode="a") # agregar info, no sobreescribir
    # Definir el formato de los prints
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(name)s] %(levelname)s:    %(message)s",
        datefmt="%H:%M:%S"
        )
    file_handler.setFormatter(formatter)

    logging.root.addHandler(file_handler)

    # Cargar los URLs ya visitados en el mes
        # Get the current year and month
    fecha_actual = date.today().isoformat()
    anio_mes = date.today().strftime("%Y-%m")

        # Construct the folder path
    folder_path = f'archivos_scrapeo/{anio_mes}'

        # Search for CSV files in the folder
    file_pattern = os.path.join(folder_path, "*.csv")
    csv_files = glob.glob(file_pattern)
    # print(f"Archivos con consultas previas: \n {csv_files}")

        # Read only the "url" column from each CSV file
    publicaciones_visitadas_antes = []
    for archivo in csv_files:
        print(f"Consultando archivo: \n {archivo}")
        try:
            df = pd.read_csv(archivo)            
            if "url" in df.columns:
                publicaciones_visitadas_antes.extend(df["url"])
        except Exception as e:
            print(f"Error leyendo el archivo CVS: {str(e)}")
            continue

    # Verificar si hay URLs para visitar

    # Reportar publicaciones ya visitadas
    print(f"Cantidad de publicaciones ya visitadas en el mes: \n {len(publicaciones_visitadas_antes)}")

    # Sacarle la URL madre
    publicaciones_visitadas_antes = [url.replace('https://www.properati.com.ar', '') for url in publicaciones_visitadas_antes]


    # Definir metodo para iniciar las consultas a las URLs
    def start_requests(self):

        urls = []

        # filename = f"properati_{self.fecha_actual}.csv"

        localidades_3f = [
            "tres-de-febrero",
            "villa-bosch",
            "saenz-pena",
            "caseros",
            "ciudadela",
            "santos-lugares",
            "loma-hermosa",
            "martin-coronado",
            "ciudad-jardin-lomas-del-palomar",
            "el-libertador",
            "churruca",
            "pablo-podesta",
            "villa-raffo",
            "jose-ingenieros",
            "once-de-septiembre"
        ]

        # Ordenar lista de localidades aleatoriamente para evitar siempre seguir 
        # el mismo patron
        random.shuffle(localidades_3f)

        for localidad in localidades_3f:
            urls.append("/".join([self.url_madre, "s", localidad, "alquiler"]))
            urls.append("/".join([self.url_madre, "s", localidad, "venta"]))

        # Hacer una request para cada localidad y parsear los datos con el 
        #   metodo parse_front
        for url in urls:
            print(f"Scrapeando la siguiente página: \n {url}")
            yield scrapy.Request(url=url, callback=self.parse_front)


    # Definir metodo para parsear la pagina elegida, que tiene los links a las 
    #   publicaciones de propiedades obtenidas de la busqueda
    def parse_front(self, response):

        # Extraer los links a las publicaciones
        sufijos_de_links_a_posteos = response.xpath('//div[@id="listings"]//div[@id="listings-content"]//a/@href').extract()

        # Reportar cantidad de publicaciones encontradas (visitadas o no)
        print(f"Cantidad de publicaciones encontradas en {response.request.url}: \n {len(sufijos_de_links_a_posteos)}")

        # Quedarse con los links no visitados
        sufijos_de_links_a_posteos = [link for link in sufijos_de_links_a_posteos if link not in self.publicaciones_visitadas_antes]

        # Reportar cantidad de publicaciones encontradas (no visitadas)
        print(f"Cantidad de publicaciones encontradas y no visitadas en {response.request.url}: \n {len(sufijos_de_links_a_posteos)}")

        # Si hay algo para scrapear...
        if(len(sufijos_de_links_a_posteos)>0):

            # Construir URLs completas
            links_a_posteos = [self.url_madre + link for link in sufijos_de_links_a_posteos]

            # Ordenar lista de urls de publicaciones aleatoriamente para evitar 
            #   siempre seguir el mismo patron
            random.shuffle(links_a_posteos)
        
            # Parsear el link de cada publicacion con el metodo parse_listing()
            for url in links_a_posteos:
                print(f"Consultando publicacion no visitada en: \n {url}")
                yield scrapy.Request(url, callback=self.parse_listing)   
                      
        # Veriricar si ya esta en la ultima pagina de publicaciones
        ultima_pagina = response.xpath('//div[@class="pagination"]//div[@id="pagination-next"]/@data-islast').get()

        # Si no esta en la ultima pagina, repetir el metodo parse_front para la pagina siguiente
        if ultima_pagina=='false':
            url_proxima_pagina = response.xpath('//div[@class="pagination"]//a[div[@id="pagination-next"]]/@href').get()
            yield scrapy.Request(url=url_proxima_pagina, callback=self.parse_front)
        

    # Definir metodo para parsear la pagina con la informacion de la publicacion
    def parse_listing(self, response):

        print(f"Parseando publicacion no visitada en: \n {response.request.url}")

        # Obtener informacion de la publicacion
        url = response.request.url

        url_primera_imagen = response.xpath('//div[@class="photos"]//img/@src').extract_first()

        titulo = response.xpath('//div[@class="main-title"]/h1/text()').extract_first()

        precio = response.xpath('//div[@class="prices-and-fees__price"]/text()').extract_first()
        # precio = re.sub(r'[^\d]', '', precio) # extraer numeros (sacar moneda y decimales)
        # !!! agregar: precio_frecuencia
        # !!! agregar: precio_moneda

        precio_frecuencia_mensual = response.xpath('//div[@class="prices-and-fees__month"]/text()').extract_first()
        ubicacion = response.xpath('//div[@class="location"]/text()').extract_first()
        dormitorios = response.xpath('//div[@class="details-item" and div[@class="details-item-icon" and i[@class="details-item__icon-bed"]]]/div[@class="details-item-value"]/text()').extract_first()
        # dormitorios = [int(i) for i in dormitorios.split() if i.isdigit()]
        banios = response.xpath('//div[@class="details-item" and div[@class="details-item-icon" and i[@class="details-item__icon-bath"]]]/div[@class="details-item-value"]/text()').extract_first()
        # baions = [int(i) for i in baions.split() if i.isdigit()]
        area = response.xpath('//div[@class="details-item" and div[@class="details-item-icon" and i[@class="details-item__icon-area"]]]/div[@class="details-item-value"]/text()').extract_first()
        # area = [int(i) for i in baions.split() if i.isdigit()]
        tipo_propiedad = response.xpath('//div[@class="property-type"]/span[@class="place-features__values"]/text()').extract_first()
        tipo_operacion = response.xpath('//div[@class="operation-type"]/span[@class="place-features__values"]/text()').extract_first()
        anio_construccion = response.xpath('//div[@class="year"]/span[@class="place-features__values"]/text()').extract_first()
        tiempo_desde_publicacion_y_usuario_publicador = response.xpath('//div[@class="date"]/text()').extract_first()
        descripcion = response.xpath('//div[@id="description-text"]/text()').extract_first()
        caracteristicas_de_la_vivienda = response.xpath('//div[@class="facilities__item"]//text()').extract()
        ubicacion2 = response.xpath('//div[@class="location-map__location-address-map"]/text()').extract_first()

        # Crear un item publicacion
        publicacion = ItemPublicacion()

        # LLenar el item con sus variables
        publicacion['url'] = url
        publicacion['url_primera_imagen'] = url_primera_imagen
        publicacion['titulo'] = titulo
        publicacion['precio'] = precio
        publicacion['precio_frecuencia_mensual'] = precio_frecuencia_mensual
        publicacion['ubicacion'] = ubicacion
        publicacion['dormitorios'] = dormitorios
        publicacion['banios'] = banios
        publicacion['area'] = area
        publicacion['tipo_propiedad'] = tipo_propiedad
        publicacion['tipo_operacion'] = tipo_operacion
        publicacion['anio_construccion'] = anio_construccion
        publicacion['tiempo_desde_publicacion_y_usuario_publicador'] = tiempo_desde_publicacion_y_usuario_publicador
        publicacion['descripcion'] = descripcion
        publicacion['caracteristicas_de_la_vivienda'] = caracteristicas_de_la_vivienda
        publicacion['ubicacion2'] = ubicacion2
        publicacion['fecha_scrapeo'] = date.today().isoformat()        

        # Verificar si la consulta no devuelve informacion
        if publicacion.get("titulo") is None:
            self.log("No se ha logrado obtener informacion de esta publicacion.")
            self.cant_publicaciones_visitadas_sin_info_hoy += 1

            # A partir de X publicaciones sin info, terminar el scrapeo
            if self.cant_publicaciones_visitadas_sin_info_hoy >= self.limite_publicaciones_sin_info:
                razon = f"Se recibieron {self.limite_publicaciones_sin_info} publicaciones sin informacion. Se frena el scrapeo."
                raise scrapy.exceptions.CloseSpider(reason=razon)
            else:
                return
        # Si tiene info, contar y agregar al CSV
        else:
            # Contar como publicacion viistada hoy
            self.cant_publicaciones_visitadas_hoy += 1

            yield publicacion

    # Reportes finales
    def closed(self, reason):
        # Cantidad de publicaciones visitadas en esta sesion
        self.log(f"Cantidad de publicaciones visitadas hoy con informacion: \n {self.cant_publicaciones_visitadas_hoy}")