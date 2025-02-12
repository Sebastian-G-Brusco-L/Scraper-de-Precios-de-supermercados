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
        url = f"https://www.jumbo.com.ar/{query}"
        driver.get(url)

        # Espera a que se carguen los productos
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vtex-search-result-3-x-galleryItem"))
        )

        # Desplázate hacia abajo para cargar todos los productos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        # Extrae el HTML de la página
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Encuentra todos los productos
        productos = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')

        resultados = []

        for producto in productos:
            # Link al producto
            link_producto = producto.find('a')['href']
            link_producto = f"https://www.jumbo.com.ar{link_producto}"

            # Imagen del producto
            img_container = producto.find('div', class_='vtex-product-summary-2-x-imageStackContainer')
            img_link = img_container.find('img')['src'] if img_container else "No disponible"

            # Descripción del producto
            descripcion_container = producto.find('div', class_='vtex-product-summary-2-x-nameContainer')
            descripcion = descripcion_container.find('span').text.strip() if descripcion_container else "No disponible"

            # Obtener el contenedor de precios y promociones
            precio_section = producto.find('div', class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--mainRow-price-box')
            if precio_section:
                precio_div = precio_section.find('div', class_='jumboargentinaio-store-theme-2t-mVsKNpKjmCAEM_AMCQH')
                precio = precio_div.text.strip() if precio_div else "No disponible"

                # Precio por litro
                precio_litro_container = precio_section.find('span', class_='jumboargentinaio-store-theme-1QiyQadHj-1_x9js9EXUYK')
                precio_litro = precio_litro_container.text.strip() if precio_litro_container else "No disponible"

                
                # Promociones
                promociones = []

                promocion_container = precio_section.find('div', class_='jumboargentinaio-store-theme-1oaMy8g_TkKDcWOQsx5V2i')
                promocion = promocion_container.text.strip() if promocion_container else "No disponible"

                # Precio de la promoción
                precio_promocion_container = precio_section.find('div', class_='jumboargentinaio-store-theme-1dCOMij_MzTzZOCohX1K7w')
                precio_promocion = precio_promocion_container.text.strip() if precio_promocion_container else "No disponible"

                # Segunda promoción (opcional)
                promocion_container_2 = producto.find('span', class_='jumboargentinaio-store-theme-3Hc7_vKK9au6dX_Su4b0Ae')
                if promocion_container_2:
                    promociones.append(promocion_container_2.text.strip())
                
                # Formatear promociones
                promociones = ', '.join(promociones) if promociones else "No disponible"

            else:
                precio = "No disponible"
                precio_litro = "No disponible"
                promocion = "No disponible"
                precio_promocion = "No disponible"

            # Agregar a la lista de resultados
            resultados.append({
                'link_producto': link_producto,
                'img_link': img_link,
                'descripcion': descripcion,
                'precio': precio,
                'precio_litro': precio_litro,
                'promocion': promocion,
                'precio_promocion': precio_promocion,
                'promocion_2': promociones if 'promocion_container_2' in locals() else "No disponible"
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
    print(f"  - Promoción: {producto['promocion']}")
    print(f"  - Precio de la promoción: {producto['precio_promocion']}")
    print(f"  - Segunda Promoción: {producto['promocion_2']}")
    print("-" * 40)
