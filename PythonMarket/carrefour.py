from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def buscar_productos(query):
    # Configura las opciones de Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")  # Ajusta el tamaño de la ventana
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Configura el servicio de ChromeDriver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL de búsqueda en Carrefour
    url = f"https://www.carrefour.com.ar/{query}"
    driver.get(url)

    # Desplazarse hacia abajo para cargar todos los productos
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Esperar a que la página cargue más elementos
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extraer el HTML de la página después de ajustar la ventana
    html = driver.page_source

    # Usar BeautifulSoup para parsear el HTML
    soup = BeautifulSoup(html, 'html.parser')

    productos = []

    # Extraer los productos de la página
    for item in soup.find_all('div', class_='valtech-carrefourar-search-result-0-x-galleryItem valtech-carrefourar-search-result-0-x-galleryItem--normal pa4'):
        # Extraer el enlace del producto
        enlace_producto = item.find('a')['href'] if item.find('a') else 'No disponible'
        enlace_producto = f"https://www.carrefour.com.ar{enlace_producto}"
        
        # Extraer la sección del producto
        producto_section = item.find('section', class_='vtex-product-summary-2-x-container vtex-product-summary-2-x-container--contentProduct vtex-product-summary-2-x-containerNormal vtex-product-summary-2-x-containerNormal--contentProduct overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc')

        if producto_section:
            # Extraer el contenedor del producto
            producto_article = producto_section.find('article', class_='vtex-product-summary-2-x-element vtex-product-summary-2-x-element--contentProduct pointer pt3 pb4 flex flex-column h-100')

            if producto_article:
                # Obtener el nombre del producto
                nombre_element = producto_article.find('span', class_='vtex-product-summary-2-x-productBrand')
                nombre = nombre_element.text.strip() if nombre_element else 'No disponible'

                # Obtener la promoción
                promocion_element = item.find('div', class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--rowBadges')
                if promocion_element:
                    promocion_text = promocion_element.find('span', class_='valtech-carrefourar-product-highlights-0-x-productHighlightText')
                    promocion = promocion_text.get_text(strip=True) if promocion_text else 'No tiene promoción'
                else:
                    promocion = 'No tiene promoción'

                # Obtener el precio rebajado
                precio_rebajado_element = item.find('span', class_='valtech-carrefourar-product-price-0-x-sellingPriceValue')
                if precio_rebajado_element:
                    precio_rebajado = precio_rebajado_element.get_text(separator='', strip=True)
                else:
                    precio_rebajado = 'No disponible'

                # Obtener el precio original (tachado)
                precio_original_element = item.find('span', class_='valtech-carrefourar-product-price-0-x-listPriceValue strike')
                if precio_original_element:
                    precio_original = precio_original_element.get_text(separator='', strip=True)
                else:
                    precio_original = 'No disponible'

                # Obtener el precio por litro
                precio_por_litro_container = item.find('div', class_='valtech-carrefourar-dynamic-weight-price-0-x-container')
                if precio_por_litro_container:
                    precio_por_litro_element = precio_por_litro_container.find('span', class_='valtech-carrefourar-dynamic-weight-price-0-x-currencyContainer')
                    if precio_por_litro_element:
                        precio_por_litro = precio_por_litro_element.get_text(separator='', strip=True)
                    else:
                        precio_por_litro = 'No disponible'
                else:
                    precio_por_litro = 'No disponible'

                # Obtener el link de la imagen
                imagen_element = producto_article.find('img', class_='vtex-product-summary-2-x-image')
                imagen_url = imagen_element['src'] if imagen_element else 'No disponible'

                # Añadir los datos al diccionario
                productos.append({
                    'nombre': nombre,
                    'promocion': promocion,
                    'precio_rebajado': precio_rebajado,
                    'precio_original': precio_original,
                    'imagen_url': imagen_url,
                    'precio_por_litro': precio_por_litro,
                    'enlace': enlace_producto
                })

    driver.quit()
    return productos

# Ejemplo de uso
productos_encontrados = buscar_productos('coca')

contador = 0
for producto in productos_encontrados:
    contador += 1
    print(f"\nProducto n° {contador}")
    print(f"Nombre: {producto['nombre']}")
    print(f"Promoción: {producto['promocion']}")
    print(f"Precio Rebajado: {producto['precio_rebajado']}")
    print(f"Precio Original: {producto['precio_original']}")
    print(f"Imagen URL: {producto['imagen_url']}")
    print(f"Precio por Litro: {producto['precio_por_litro']}")
    print(f"Enlace: {producto['enlace']}")
