import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO

# Reemplaza con tu propia API key de Last.fm
API_KEY = 'a26545d4dc7353ac0408c2d616f0c123'
USER = 'rattamayhorka'

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

def display_album_cover(image_url):
    if image_url:
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        # Crear la ventana de tkinter
        root = tk.Tk()
        root.title("Album Cover")

        # Redimensionar la imagen si es necesario
        img.thumbnail((500, 500))  # Cambia este tamaño si es necesario

        # Convertir la imagen a un formato compatible con tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Crear un widget de etiqueta y poner la imagen en él
        label = tk.Label(root, image=img_tk)
        label.pack()

        # Ejecutar la ventana
        root.mainloop()
    else:
        print("No se encontró la portada del álbum.")

def main():
    title, artist, album, album_art_url = get_current_track(API_KEY, USER)

    if title:
        print(f'Reproduciendo ahora: {title} - {artist}')
        print(f'Álbum: {album}')
        display_album_cover(album_art_url)
    else:
        print("No se pudo obtener la información de la canción.")

if __name__ == '__main__':
    main()
