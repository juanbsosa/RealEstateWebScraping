:cd C:\Users\Usuario\Documents\3F\SIVyS\1.WebScraping\ProperatiScraper
: Primero definir el directorio donde esta el scprit de Python para iniciar el escrapeo. (Para que funcione, este archivo tiene que estar guardado en la misma carpeta que el script.)
setlocal
cd /d %~dp0
py "run_ProperatiSpider.py"