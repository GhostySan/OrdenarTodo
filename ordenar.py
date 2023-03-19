import os
import shutil
import random
import string
from tqdm import tqdm
import secrets

# lista de extensiones para cada categoría
categorias = {
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".z", ".cab", ".iso", ".img", ".dmg", ".jar", ".war", ".ear"],
    "Imagenes": [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".bmp", ".dib", ".svg", ".svgz", ".tif", ".tiff", ".webp", ".ico", ".icon", ".jxr", ".hdp", ".wdp", ".cur", ".dds", ".exr", ".hdr", ".jng", ".mng", ".pcx", ".pict", ".psd", ".psb", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".kdc", ".dng", ".dcr", ".mos", ".pxn", ".raf", ".fff", ".3fr", ".qtk", ".rw2", ".sr2", ".srf", ".srw", ".x3f", ".avif", ".heic", ".heif", ".ai", ".eps"],
    "Audio": ['.aac', '.ac3', '.aiff', '.ape', '.au', '.dts', '.flac', '.m4a', '.m4b', '.m4p', '.mka', '.mp1', '.mp2', '.mp3', '.mpc', '.ogg', '.oma', '.pcm', '.ra', '.rm', '.tta', '.wav', '.wma', '.wv'],
    "Documentos": ['.doc', '.docx', '.dot', '.dotx', '.docm', '.dotm', '.rtf', '.odt', '.wpd', '.wps', '.xml', '.xps', '.mht', '.mhtml', '.txt', '.pdf', '.djvu', '.epub', '.fb2', '.mobi', '.pdb', '.prc', '.azw', '.azw3', '.cbz', '.cbr', '.cb7', '.cbt', '.cba', '.xps'],
    "Videos": ['.avi', '.mov', '.mp4', '.mpg', '.mpeg', '.flv', '.wmv', '.m4v', '.ts', '.mkv', '.webm', '.3gp', '.ogv', '.divx', '.xvid'],
    "Programas": [".exe", ".bat", ".cmd", ".com",".jse", ".msc", ".msi", ".msp", ".mst", ".pif", ".ps1", ".psm1", ".pyc", ".pyo", ".reg", ".scr", ".vb", ".vbe", ".vbs", ".ws", ".wsc", ".wsf", ".wsh"],
    "Programacion": ['.py', '.pyc', '.pyd', '.pyw', '.pyo', '.pyx', '.pyi', '.pxd', '.pxi', '.pyz', '.pyzw', '.pywz', '.ipynb', '.html', '.css', '.js', '.json', '.xml', '.yaml', '.csv', '.ini', '.cfg', '.conf', '.md', '.rst'],
    "No clasificado": []
}

# obtener la ruta de la carpeta actual
ruta_actual = os.getcwd()

# crear la carpeta Ordenado si no existe
carpeta_ordenado = os.path.join(ruta_actual, "Ordenado")
if not os.path.exists(carpeta_ordenado):
    os.mkdir(carpeta_ordenado)

# crear las subcarpetas dentro de Ordenado
for subfolder in categorias:
    carpeta_subfolder = os.path.join(carpeta_ordenado, subfolder)
    if not os.path.exists(carpeta_subfolder):
        os.mkdir(carpeta_subfolder)

def renombrar_si_existe(archivo, carpeta_destino):
    """
    Renombra el archivo con un nombre aleatorio si ya existe un archivo con ese nombre en la carpeta destino.
    """
    nombre_archivo = os.path.basename(archivo)
    nombre_base, extension = os.path.splitext(nombre_archivo)
    while True:
        nombre_aleatorio = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
        nuevo_nombre_archivo = nombre_aleatorio + extension
        ruta_nuevo_archivo = os.path.join(carpeta_destino, nuevo_nombre_archivo)
        if not os.path.exists(ruta_nuevo_archivo):
            shutil.move(archivo, ruta_nuevo_archivo)
            break

# obtener la lista de archivos en la carpeta actual y subcarpetas
lista_archivos = []
for root, dirs, files in os.walk(ruta_actual):
    for file in files:
        if file != "Ordenar TODO.exe": # excluir este archivo
            ruta_archivo = os.path.join(root, file)
            lista_archivos.append(ruta_archivo)
# ordenar los archivos en las carpetas correspondientes
for archivo in tqdm(lista_archivos):
    extension = os.path.splitext(archivo)[1]
    categoria_encontrada = False
    for subfolder, extensiones in categorias.items():
        if extension.lower() in extensiones:
            carpeta_subfolder = os.path.join(carpeta_ordenado, subfolder)
            destino = os.path.join(carpeta_subfolder, os.path.basename(archivo))
            if os.path.exists(destino):
                # Generar un nuevo nombre de archivo aleatorio
                nuevo_nombre = os.path.splitext(os.path.basename(archivo))[0] + "_" + secrets.token_hex(4) + extension
                destino = os.path.join(carpeta_subfolder, nuevo_nombre)
            shutil.move(archivo, destino)
            categoria_encontrada = True
            break
    if not categoria_encontrada:
        carpeta_subfolder = os.path.join(carpeta_ordenado, "No clasificado")
        destino = os.path.join(carpeta_subfolder, os.path.basename(archivo))
        if os.path.exists(destino):
            # Generar un nuevo nombre de archivo aleatorio
            nuevo_nombre = os.path.splitext(os.path.basename(archivo))[0] + "_" + secrets.token_hex(4) + extension
            destino = os.path.join(carpeta_subfolder, nuevo_nombre)
        shutil.move(archivo, destino)
# eliminar carpetas vacías dentro de la carpeta principal, excepto la carpeta Ordenado
for root, dirs, files in os.walk(ruta_actual, topdown=False):
    for dir in dirs:
        if dir != "Ordenado":
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

print("Presione cualquier tecla para salir...")
input()