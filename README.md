# SteamWebScraper
Este script extrae los precios totales y actuales de los videojuegos de la plataforma [Steam](https://store.steampowered.com/search/?page=1)

El script se debe ejecutar de la siguiente manera:
```
python ws.py
```

Además, a la ejecución del script se le podrán añadir tres parámetros opcionaes:
* `--fp n` FirstPage: Página n desde la que comenzará el scraping (página 1 si se omite).
* `--lp n` LastPage: Página n hasta la que se realizará el scraping (máximo si se omite).
* `--t n`  Threads: Número de threads que utilizará el script (1 si se omite).
