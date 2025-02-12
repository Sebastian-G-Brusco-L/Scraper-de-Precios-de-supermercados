# Scraper de Precios de Supermercados

Este repositorio contiene **7 scripts en Python** que utilizan Selenium y BeautifulSoup para **scrapear productos de 7 supermercados** en función de una consulta de búsqueda.

## 🏪 Supermercados Soportados

- **Carrefour**
- **Coto**
- **Disco**
- **Vea**
- **Jumbo**
- **Día**
- **Changomás**

Cada script accede a la página del supermercado correspondiente, busca los productos relacionados con la consulta ingresada y extrae información clave como:

- 📌 **Nombre del producto**
- 💰 **Precio original y precio con descuento**
- 🎁 **Promociones disponibles**
- 🖼️ **Imagen del producto**
- 🔗 **Enlace al producto en la web del supermercado**

## 🚀 Requisitos

Para ejecutar los scripts, necesitas:

- **Python 3.x**
- **Google Chrome** instalado
- **Chromedriver** compatible con tu versión de Chrome
- Librerías de Python:
  ```bash
  pip install selenium beautifulsoup4
  ```

## 🛠️ Uso

Cada script tiene una función `buscar_productos(query)`, donde `query` es el producto que deseas buscar.

Ejemplo de uso:
```python
from carrefour_scraper import buscar_productos

productos = buscar_productos("coca cola")
for producto in productos:
    print(producto)
```

Puedes ejecutar cada script de forma independiente o integrarlos en una aplicación más grande.

## ⚠️ Consideraciones

- Los sitios web pueden actualizar su estructura, lo que podría romper el scraping. En ese caso, será necesario actualizar los selectores de los elementos HTML.
- Evita hacer solicitudes excesivas para no ser bloqueado por los supermercados.



