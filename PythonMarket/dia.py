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

    # Navega al sitio web de búsqueda
    driver.get(f'https://diaonline.supermercadosdia.com.ar/{query}')

    # Espera a que los productos se carguen
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'vtex-flex-layout-0-x-flexColChild'))
        )

        # Desplázate hacia abajo para cargar todos los productos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # Espera para asegurar que los productos se carguen

    except Exception as e:
        print(f"Error al cargar la página: {e}")
        driver.quit()
        return

    # Obtiene el contenido de la página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Encuentra los productos
    productos = soup.find_all('div', class_='diaio-search-result-0-x-galleryItem')

    resultados = []
    for producto in productos:
        enlace = producto.find('a')['href']
        nombre = producto.find('span', class_='vtex-product-summary-2-x-brandName').text.strip()
        precio = producto.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
        precio = precio.get_text(strip=True) if precio else 'Precio no disponible'
        
        # Extrae el precio por litro
        especificaciones = producto.find_all('div', class_='pr0 items-stretch vtex-flex-layout-0-x-stretchChildrenWidth flex')
        precio_por_litro = 'Precio por litro no disponible'
        for especificacion in especificaciones:
            valor = especificacion.find('span', {'data-specification-name': 'PrecioPorUnd'})
            if valor:
                precio_por_litro = valor.get_text(strip=True)
                break

        # Extrae todas las promociones
        promociones = producto.find_all('span', class_='vtex-product-highlights-2-x-productHighlightText')
        if promociones:
            promocion_textos = [promo.get_text(strip=True) for promo in promociones]
            promocion = ', '.join(promocion_textos)
        else:
            promocion = 'No tiene promoción'

        resultados.append({
            'nombre': nombre,
            'enlace': f"https://diaonline.supermercadosdia.com.ar{enlace}",
            'precio': precio,
            'precio_por_litro': precio_por_litro,
            'promocion': promocion
        })

    driver.quit()
    return resultados

# Ejemplo de uso
productos = buscar_productos('alfajor')
contador = 0
for producto in productos:
    contador+=1
    print(f"Producto n {contador}")
    print(f"Nombre: {producto['nombre']}")
    print(f"Enlace: {producto['enlace']}")
    print(f"Precio: {producto['precio']}")
    print(f"Precio por litro: {producto['precio_por_litro']}")
    print(f"Promoción: {producto['promocion']}")
    print('---')
