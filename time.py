import tkinter as tk
from time import strftime

# Función para actualizar la hora en la etiqueta
def update_time():
    time_string = strftime('%H:%M:%S %p')  # Formato de hora (24h:MM:SS AM/PM)
    label.config(text=time_string)
    label.after(1000, update_time)  # Actualiza la hora cada 1000 ms (1 segundo)

# Crear la ventana principal
root = tk.Tk()
root.title("Reloj")

# Configurar el tamaño y la posición de la ventana
root.geometry("250x100")  # Puedes ajustar el tamaño según prefieras

# Configurar el estilo de la fuente
font_style = ('calibri', 80, 'bold')

# Crear una etiqueta para mostrar la hora
label = tk.Label(root, font=font_style, background='black', foreground='white')

# Mostrar la etiqueta en la ventana
label.pack(anchor='center')

# Inicializar la actualización de la hora
update_time()

# Ejecutar el bucle principal de la aplicación
root.mainloop()
