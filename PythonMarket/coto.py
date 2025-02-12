from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

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

    # URL de búsqueda en Coto
    url = f"https://www.cotodigital3.com.ar/sitios/cdigi/browse?_dyncharset=utf-8&Dy=1&Ntt={query}&Nty=1&Ntk=&siteScope=ok&_D%3AsiteScope=+&atg_store_searchInput={query}&idSucursal=200&_D%3AidSucursal=+&search=Ir&_D%3Asearch=+&_DARGS=%2Fsitios%2Fcartridges%2FSearchBox%2FSearchBox.jsp"
    driver.get(url)
    
    # Espera para que la página cargue completamente
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'atg_store_main'))
        )

         # Desplázate hacia abajo para cargar todos los productos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        
    except Exception as e:
        print(f"Error al cargar la página: {e}")
        driver.quit()
        return
    
    # Desplazamiento hacia abajo para cargar todos los productos
    for _ in range(5):  # Ajusta el número de veces que deseas desplazarte hacia abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Ajusta el tiempo de espera según sea necesario

    # Obtiene el HTML de la página y lo analiza con BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Encuentra los productos en la página
    productos = soup.select('#atg_store_main .category .grid.grid_center .aside1 .found_box ul.grid li')

    contador = 0
    for producto in productos:
        try:
            # Encuentra el div principal del producto
            div_producto = producto.select_one('.leftList')
            if not div_producto:
                continue
            
            # Extrae el precio del producto
            precio = div_producto.select_one('.atg_store_newPrice')
            precio_texto = precio.text.strip() if precio else "No disponible"
            
            # Extrae el enlace del producto
            enlace_producto = div_producto.select_one('a')
            enlace_url = enlace_producto['href'] if enlace_producto else "No disponible"
            
            # Extrae la descripción completa
            descripcion = enlace_producto.select_one('.descrip_full')
            descripcion_texto = descripcion.text.strip() if descripcion else "No disponible"
            
            # Extrae el precio por litro
            precio_litro = div_producto.select_one('.unit')
            if precio_litro:
                # Limpia el texto del precio por litro
                precio_litro_texto = ' '.join(precio_litro.stripped_strings)
                # Usa una expresión regular para limpiar espacios adicionales
                precio_litro_texto = re.sub(r'\s+', ' ', precio_litro_texto).strip()
            else:
                precio_litro_texto = "No disponible"
            
            # Extrae el enlace de la imagen
            imagen = producto.select_one('img')
            imagen_url = imagen['src'] if imagen else "No disponible"
            
            # Extrae las promociones y el precio de la promoción
            promocion = producto.select_one('.product_discount')
            oferta_texto = "No tiene promoción"
            precio_descuento_texto = "No disponible"
            
            if promocion:
                # Buscar las promociones regulares
                oferta = promocion.select_one('.image_discount_container span')
                oferta_texto = oferta.text.strip() if oferta else "No tiene promoción"
                
                # Buscar el precio de descuento en dos posibles ubicaciones
                precio_descuento = promocion.select_one('.price_discount')
                if not precio_descuento:
                    precio_descuento = promocion.select_one('.price_discount_gde')
                
                precio_descuento_texto = precio_descuento.text.strip() if precio_descuento else "No disponible"
                
            contador += 1    
            
            print(f"Producto n {contador}")
            print(f'Imagen: {imagen_url}')
            print(f'Enlace del producto: {enlace_url}')
            print(f'Descripción: {descripcion_texto}')
            print(f'Precio por litro: {precio_litro_texto}')
            print(f'Precio: {precio_texto}')
            print(f'Promoción: {oferta_texto}')
            print(f'Precio de la promoción: {precio_descuento_texto}')
            print('---')
        except Exception as e:
            print(f"Error al procesar un producto: {e}")
    
    # Cierra el navegador
    driver.quit()

# Ejemplo de uso
buscar_productos('arroz')
