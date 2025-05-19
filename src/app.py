import requests
import pandas as pd
from lxml import html  # <-- IMPORTACIÓN QUE FALTABA

# Set the URL of the website to scrape
url = "https://lenguaje.com/generacion-del-27/"

response = requests.get(url) 
# Verificar que la solicitud fue exitosa
if response.status_code != 200:
    print("Error al acceder a la página")
print("estado", response.status_code)

# Parsear el contenido con lxml
tree = html.fromstring(response.content)

# Buscar todos los <li> dentro del <ol class= "wp-block-list">
items = tree.xpath('//ol[@class="wp-block-list"]/li')

# Lista para almacenar los datos
autores_data = []

# Extraer los elementos y extraer datos
autores = []
for item in items:
    texo = item.text_content().strip()

    try:
        nombre_y_fechas, obras = texo.split('Obras:', 1)
    except ValueError:
        nombre_y_fechas = texo
        obras = ''
    # Extraer el nombre del autor y las fechas
    if '(' in nombre_y_fechas:
        nombre, fechas = nombre_y_fechas.split('(', 1)
        nombre = nombre.strip()
        fechas = fechas.strip(') ').replace("–", "-")  # normalizar guion
    else:
        nombre = nombre_y_fechas.strip()
        fechas = ''

    autores_data.append((nombre, fechas, obras))

# Crear el DataFrame
df = pd.DataFrame(autores_data, columns=['Autor', 'Fechas', 'Obras'])

# Mostrarlo por pantalla
print(df)

# Guardarlo en un archivo CSV
df.to_csv('autores_generacion_27_separados.csv', index=False)
