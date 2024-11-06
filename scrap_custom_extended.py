
import requests
from bs4 import BeautifulSoup

logBusquedas = "log-"

def buscarPorUrl():
    url = input("Escribe la web a analizar:\n")
    url = "https://wikipedia.com" if len(url) <= 0 else url
    print(f"\nDominio a analizar : {url}")
    return url

def leerFichero():
    nombreFichero = input("Nombre del fichero: \n")
    try:
        with open(nombreFichero, 'r', encoding='utf-8') as archivo:
            lineasPasadasAString = archivo.read()
        return lineasPasadasAString
    except FileNotFoundError:
        print(f"Error: El archivo {nombreFichero} no se encuentra.")
        exit()

opciones_inicio = int(input("Fuente de datos:\n\t1. url a elegir\n\t2. Fichero HTML\n"))

while opciones_inicio < 1 or opciones_inicio > 2:
    opciones_inicio = int(input("Opción incorrecta. Repite: "))

response = ""
html_content = ""

if opciones_inicio == 1:
    url = buscarPorUrl()
    response = requests.get(url)
    if response.status_code != 200:
        print("Solicitud fallida con código de estado:", response.status_code)
        exit()
    else:
        print("Solicitud exitosa")
        html_content = response.text
        logBusquedas += "url"
elif opciones_inicio == 2:
    html_content = leerFichero()
    logBusquedas += "html"

soup = BeautifulSoup(html_content, 'html.parser')

def guardarResultados(nombreArchivo, componenteIn, extra=""):
    nombreArchivo = f"{nombreArchivo}.txt"
    try:
        with open(nombreArchivo, 'w', encoding='utf-8') as fichero:
            for componente in componenteIn:
                if extra == "sacarEnlaces":
                    componente = componente.get('href')
                elif extra == "buscarPorClass":
                    componente = componente.text
                elif extra == "sacarLinksImagenes":
                    componente = componente.get('src')
                else:
                    componente = componente.get(extra, componente)
                
                fichero.write(str(componente) + "\n")
        print(f"Fichero '{nombreArchivo}' escrito correctamente.")
    except Exception as e:
        print(f"Error escribiendo en el archivo: {e}")

# Opciones extendidas basadas en el script original
def buscarPorTag():
    tag = input("Tag a buscar: ")
    elementos = soup.find_all(tag)
    guardarResultados(logBusquedas + "-tag", elementos)

def buscarPorClass():
    clase = input("Clase a buscar: ")
    elementos = soup.find_all(class_=clase)
    guardarResultados(logBusquedas + "-class", elementos, "buscarPorClass")

def buscarPorId():
    id_elemento = input("ID a buscar: ")
    elemento = soup.find(id=id_elemento)
    guardarResultados(logBusquedas + "-id", [elemento])

def buscarString():
    texto = input("Texto a buscar: ")
    elementos = soup.find_all(string=texto)
    guardarResultados(logBusquedas + "-string", elementos)

def textoPlano():
    texto = soup.get_text()
    guardarResultados(logBusquedas + "-textoplano", [texto])

def sacarEnlaces():
    enlaces = soup.find_all('a')
    guardarResultados(logBusquedas + "-enlaces", enlaces, "sacarEnlaces")

def sacarLinksImagenes():
    global logBusquedas
    logBusquedas += "-imagenes"
    imagenes = soup.find_all('img')
    guardarResultados(logBusquedas, imagenes, "sacarLinksImagenes")

def tagCustomAtributoCustom():
    tag = input("Tag a buscar: ")
    atributo = input("Atributo a buscar dentro del tag: ")
    elementos = soup.find_all(tag)
    guardarResultados(logBusquedas + f"-{tag}-{atributo}", elementos, atributo)

# Hashmap de opciones
opciones_busqueda = {
    1: buscarPorTag,
    2: buscarPorClass,
    3: buscarPorId,
    4: buscarString,
    5: textoPlano,
    6: sacarEnlaces,
    7: sacarLinksImagenes,
    8: tagCustomAtributoCustom
}

opcion = int(input("Elige la operación que quieres hacer:\n1. Buscar por tag\n2. Buscar por class\n3. Buscar por ID\n4. Buscar por string\n5. Texto plano\n6. Sacar enlaces\n7. Sacar links de imágenes\n8. Buscar tag y atributo personalizado\n"))

while opcion not in opciones_busqueda:
    opcion = int(input("Opción incorrecta. Repite la opción a escoger: "))

opciones_busqueda[opcion]()  
