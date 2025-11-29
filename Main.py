import cv2
import time
from GestureRecognizer import GestureRecognizer
from MusicController import MusicController

# --- Configuración ---
WINDOW_NAME = "Control de Musica por Gestos"
COOLDOWN_STATIC_GESTURE = 2.0 # Cooldown para gestos estáticos (segundos) - Aumentado a 2.0s para evitar comandos accidentales

# --- Inicialización ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

recognizer = GestureRecognizer()
controller = MusicController()

# Variables para el control de gestos
last_static_command_time = time.time()

print("Sistema de Control de Música por Gestos iniciado. Presiona 'q' para salir.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignorando frame vacío de la cámara.")
        continue

    # Voltear la imagen horizontalmente para una vista de espejo más intuitiva
    image = cv2.flip(image, 1)
    
    # Convertir a RGB para MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Procesar el frame y obtener el comando de gesto estático
    image_processed, static_gesture = recognizer.process_frame(image_rgb)
    
    # Convertir de vuelta a BGR para mostrar con OpenCV
    image_processed = cv2.cvtColor(image_processed, cv2.COLOR_RGB2BGR)

    # --- Lógica de Control de Gestos Estáticos ---
    current_time = time.time()
    
    if static_gesture and (current_time - last_static_command_time > COOLDOWN_STATIC_GESTURE):
        command_map = {
            "open_hand": "play_pause", # Mano Abierta -> Play/Pause
            "fist": "play_pause",      # Puño Cerrado -> Play/Pause
            "peace": "volume_down",    # Paz -> Bajar Volumen
            "rock": "volume_up",       # Rock -> Subir Volumen
            "point_right": "next_track", # Apuntar Derecha -> Siguiente Canción
            "point_left": "prev_track"  # Apuntar Izquierda -> Canción Anterior
        }
        
        command = command_map.get(static_gesture)
        
        if static_gesture == "open_hand":
            command = "play_pause" 
            
        elif static_gesture == "fist":
            command = "play_pause"
            
        elif static_gesture == "peace":
            command = "volume_down"
            
        elif static_gesture == "rock":
            command = "volume_up"
            
        elif static_gesture == "point_right":
            command = "next_track"
            
        elif static_gesture == "point_left":
            command = "prev_track"
            
        if command:
            if controller.execute_command(command):
                last_static_command_time = current_time
                print(f"Comando de Gesto Estático Ejecutado: {static_gesture} -> {command}")
                cv2.putText(image_processed, f"COMANDO: {command.upper()}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # --- Lógica de Control de Gestos Dinámicos (Swipe) ---
    # NOTA: La lógica de swipe dinámico ha sido reemplazada por los gestos estáticos de "point_right" y "point_left".
    # Se mantiene la estructura para evitar errores, pero la lógica de swipe se omite.
    pass

    # Mostrar el frame
    cv2.putText(image_processed, f"Gesto: {static_gesture if static_gesture else 'N/A'}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow(WINDOW_NAME, image_processed)

    # Salir con 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
print("Sistema de Control de Música por Gestos finalizado.")
