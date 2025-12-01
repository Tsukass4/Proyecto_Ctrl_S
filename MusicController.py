import pyautogui
import time

class MusicController:
    """
    Clase para controlar la aplicación de música simulando pulsaciones de teclas multimedia.
    Se utiliza pyautogui para la simulación de teclas.
    """
    def __init__(self):
        # Mapeo de comandos a teclas multimedia
        self.commands = {
            "play_pause": "playpause",
            "next_track": "nexttrack",
            "prev_track": "prevtrack",
            "volume_up": "volumeup",
            "volume_down": "volumedown"
        }
        self.last_command_time = time.time()
        self.cooldown = 0.5  # Cooldown de 0.5 segundos para evitar comandos duplicados

    def execute_command(self, command_name):
        """
        Ejecuta un comando de música si el tiempo de espera (cooldown) ha pasado.
        """
        current_time = time.time()
        if current_time - self.last_command_time < self.cooldown:
            # print(f"Comando '{command_name}' omitido por cooldown.")
            return False

        if command_name in self.commands:
            key = self.commands[command_name]
            pyautogui.press(key)
            self.last_command_time = current_time
            # print(f"Comando ejecutado: {command_name} ({key})")
            return True
        else:
            # print(f"Comando desconocido: {command_name}")
            return False

