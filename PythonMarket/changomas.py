from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def buscar_productos(query):
    # Configura las opciones de Chrome para modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Configura el servicio de ChromeDriver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navega a la página de resultados de búsqueda
        url = f"https://www.masonline.com.ar/{query}"
        driver.get(url)

        # Espera a que se carguen los productos
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vtex-search-result-3-x-galleryItem"))
        )

        # Desplázate hacia abajo para cargar todos los productos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        # Obtén el contenido de la página
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Encuentra todos los productos
        productos = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')

        resultados = []

        for producto in productos:
            # Extrae el enlace del producto
            enlace_producto = producto.find('a', class_='vtex-product-summary-2-x-clearLink')['href']
            enlace_producto = f"https://www.masonline.com.ar{enlace_producto}"

            # Extrae la imagen del producto
            imagen_producto = producto.find('img', class_='vtex-product-summary-2-x-imageNormal')['src']

            # Extrae la descripción del producto
            descripcion_producto = producto.find('span', class_='vtex-product-summary-2-x-productBrand').text.strip()

            # Extrae el precio por litro
            precio_litro = producto.find('div', class_='valtech-gdn-dynamic-weight-price-0-x-container')
            if precio_litro:
                precio_litro = ''.join(precio_litro.stripped_strings).replace(' ', '')
            else:
                precio_litro = "No disponible"

            # Extrae el precio total
            precio_total = producto.find('div', class_='valtech-gdn-dynamic-product-0-x-dynamicProductPrice')
            if precio_total:
                precio_total = precio_total.text.strip()
            else:
                precio_total = "No disponible"

          # Extrae la promoción del producto
            promocion_container = producto.find('div', class_='valtech-gdn-custom-highlights-0-x-customHighlightTextContainer')
            if promocion_container:
                promocion_spans = promocion_container.find_all('span')
                promocion = "No tiene promoción"
                for span in promocion_spans:
                    if 'highlight-undefined' in span.get('class', []):
                        promocion = span.text.strip()
                        break
            else:
                promocion = "No tiene promoción"

            resultados.append({
                'enlace_producto': enlace_producto,
                'imagen_producto': imagen_producto,
                'descripcion_producto': descripcion_producto,
                'precio_litro': precio_litro,
                'precio_total': precio_total,
                'promocion': promocion
            })

        return resultados

    finally:
        driver.quit()

# Ejemplo de uso
productos = buscar_productos("coca")
for i, producto in enumerate(productos, 1):
    print(f"Producto {i}:")
    print(f"  - Link al producto: {producto['enlace_producto']}")
    print(f"  - Link de la imagen: {producto['imagen_producto']}")
    print(f"  - Descripción: {producto['descripcion_producto']}")
    print(f"  - Precio: {producto['precio_total']}")
    print(f"  - Precio por litro: {producto['precio_litro']}")
    print(f"  - Promoción: {producto['promocion']}")
    print("-" * 40)
