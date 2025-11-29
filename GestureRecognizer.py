import mediapipe as mp
import numpy as np

class GestureRecognizer:
    """
    Clase para la detección de manos y el reconocimiento de gestos estáticos
    utilizando MediaPipe Hands.
    """
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def process_frame(self, image):
        """
        Procesa un frame de video para detectar manos y reconocer gestos.
        Retorna el frame con las anotaciones y el comando de gesto reconocido.
        """
        image_rgb = image
        results = self.hands.process(image_rgb)
        gesture_command = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                gesture_command = self._recognize_static_gesture(hand_landmarks)
                
        return image, gesture_command

    def _recognize_static_gesture(self, hand_landmarks):
        landmarks = hand_landmarks.landmark
        
        def is_finger_up(tip_id, pip_id):
            return landmarks[tip_id].y < landmarks[pip_id].y

        # Estado de los dedos (True si está levantado)
        thumb_up = landmarks[4].y < landmarks[3].y and landmarks[4].y < landmarks[2].y
        index_up = is_finger_up(8, 6)
        middle_up = is_finger_up(12, 10)
        ring_up = is_finger_up(16, 14)
        pinky_up = is_finger_up(20, 18)

        # Gesto: Mano Abierta (Play)
        if index_up and middle_up and ring_up and pinky_up:
            return "open_hand"

        # Gesto: Puño Cerrado (Pause)
        if not index_up and not middle_up and not ring_up and not pinky_up:
            return "fist"

        # Gesto: Paz (Volume Down)
        if index_up and middle_up and not ring_up and not pinky_up:
            return "peace"

        # Gesto: Rock (Volume Up)
        if index_up and pinky_up and not middle_up and not ring_up:
            return "rock"

        # Gesto: Apuntar (Derecha/Izquierda) - Pulgar e Índice levantados
        # Este gesto es un puño con pulgar e índice extendidos.
        if thumb_up and index_up and not middle_up and not ring_up and not pinky_up:
            # Compara la posición X de la punta del índice con la base de la mano
            if landmarks[8].x > landmarks[5].x:
                return "point_right"
            else:
                return "point_left"

        return None
