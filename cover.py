import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO

API_KEY = 'a26545d4dc7353ac0408c2d616f0c123'
USER = 'rattamayhorka'
CHECK_INTERVAL = 30000  # Intervalo de verificación en milisegundos (30 segundos)

def get_current_track(api_key, user):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.getrecenttracks',
        'user': user,
        'api_key': api_key,
        'format': 'json',
        'limit': 1
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if 'recenttracks' in data and 'track' in data['recenttracks']:
        track = data['recenttracks']['track'][0]
        artist = track['artist']['#text']
        album = track['album']['#text']
        title = track['name']
        album_art_url = track['image'][-1]['#text']  # Obtiene la URL de la portada (último tamaño disponible)
        
        return title, artist, album, album_art_url
    else:
        return None, None, None, None

def display_album_cover(image_url, root):
    if image_url:
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        # Obtener el tamaño de la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Obtener las dimensiones originales de la imagen
        img_width, img_height = img.size

        # Calcular la proporción de escala
        scale = min(screen_width / img_width, screen_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # Redimensionar la imagen manteniendo la proporción
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Crear una imagen en blanco para centrar la imagen redimensionada
        background = Image.new('RGB', (screen_width, screen_height), (0, 0, 0))
        background.paste(img, ((screen_width - new_width) // 2, (screen_height - new_height) // 2))

        # Convertir la imagen a un formato compatible con tkinter
        img_tk = ImageTk.PhotoImage(background)

        # Actualizar la imagen en el widget de la etiqueta
        label.config(image=img_tk)
        label.image = img_tk  # Guardar referencia de la imagen

def on_image_click(event):
    # Cierra la aplicación cuando se hace clic en la imagen
    root.quit()

def update_track_info():
    title, artist, album, album_art_url = get_current_track(API_KEY, USER)
    
    if title:
        print(f'Reproduciendo ahora: {title} - {artist}')
        print(f'Álbum: {album}')
        display_album_cover(album_art_url, root)
    else:
        print("No se pudo obtener la información de la canción.")
    
    # Volver a llamar a esta función después de CHECK_INTERVAL milisegundos
    root.after(CHECK_INTERVAL, update_track_info)

# Crear la ventana de tkinter
root = tk.Tk()
root.title("Album Cover")

# Configurar la ventana en modo pantalla completa
root.attributes('-fullscreen', True)

# Crear un widget de etiqueta vacío
label = tk.Label(root)
label.pack(fill=tk.BOTH, expand=True)

# Asignar la función on_image_click al evento de clic en la imagen
label.bind("<Button-1>", on_image_click)

# Llamar a la función por primera vez
update_track_info()

# Ejecutar la ventana
root.mainloop()
