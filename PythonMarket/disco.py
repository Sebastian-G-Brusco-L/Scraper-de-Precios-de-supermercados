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
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless
    chrome_options.add_argument("--window-size=1920,1080")  # Ajusta el tamaño de la ventana
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Configura el servicio de ChromeDriver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navega a la página de resultados de búsqueda
        url = f"https://www.disco.com.ar/{query}"
        driver.get(url)

        # Espera a que se carguen los productos
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vtex-search-result-3-x-galleryItem"))
        )

        # Desplázate hacia abajo para cargar todos los productos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # Espera para asegurar que los productos se carguen

        # Extrae el HTML de la página
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Encuentra todos los productos
        productos = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')

        resultados = []

        for producto in productos:
            # Link al producto
            link_producto = producto.find('a')['href']
            link_producto = f"https://www.disco.com.ar{link_producto}"

            # Imagen del producto
            img_container = producto.find('div', class_='vtex-product-summary-2-x-imageStackContainer')
            img_link = img_container.find('img')['src'] if img_container else "No disponible"

            # Descripción del producto
            descripcion_container = producto.find('div', class_='vtex-product-summary-2-x-nameContainer')
            descripcion = descripcion_container.find('span').text.strip() if descripcion_container else "No disponible"

            # Obtener el contenedor de precios y promociones
            precio_section = producto.find('div', class_='vtex-flex-layout-0-x-flexColChild pb0')
            if precio_section:
                # Precio
                divs = precio_section.find_all('div')
                if len(divs) >= 3:
                    precio_div = divs[2]  # Tercer div
                    precio = precio_div.text.strip() if precio_div else "No disponible"
                else:
                    precio = "No disponible"

                # Precio por litro
                precio_litro_container = producto.find('div', class_='discoargentina-store-theme-1QiyQadHj-1_x9js9EXUYK')
                precio_litro = precio_litro_container.text.strip() if precio_litro_container else "No disponible"

                # Promociones
                promociones = []

                # Buscar en la primera clase de promoción
                promocion_container_1 = producto.find('div', class_='discoargentina-store-theme-1LCA-xHQ8NgNHQ062m5gTL')
                if promocion_container_1:
                    promociones.append(promocion_container_1.text.strip())

                # Buscar en la segunda clase de promoción
                promocion_container_2 = producto.find('span', class_='discoargentina-store-theme-3Hc7_vKK9au6dX_Su4b0Ae')
                if promocion_container_2:
                    promociones.append(promocion_container_2.text.strip())

                 # Buscar en el span específico para promociones
                promocion_span = precio_section.find('span', class_='discoargentina-store-theme-Aq2AAEuiQuapu8IqwN0Aj')
                if promocion_span:
                    promociones.append(promocion_span.text.strip())

                # Formatear promociones
                promociones = ', '.join(promociones) if promociones else "No disponible"
            else:
                precio = "No disponible"
                precio_litro = "No disponible"
                promociones = "No disponible"

            # Agregar a la lista de resultados
            resultados.append({
                'link_producto': link_producto,
                'img_link': img_link,
                'descripcion': descripcion,
                'precio': precio,
                'precio_litro': precio_litro,
                'promociones': promociones
            })

        return resultados

    finally:
        driver.quit()

# Ejemplo de uso
productos = buscar_productos("coca")
for i, producto in enumerate(productos, 1):
    print(f"Producto {i}:")
    print(f"  - Link al producto: {producto['link_producto']}")
    print(f"  - Link de la imagen: {producto['img_link']}")
    print(f"  - Descripción: {producto['descripcion']}")
    print(f"  - Precio: {producto['precio']}")
    print(f"  - Precio por litro: {producto['precio_litro']}")
    print(f"  - Promociones: {producto['promociones']}")
    print("-" * 40)
