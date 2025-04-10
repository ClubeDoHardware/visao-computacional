from pyfirmata import Arduino, SERVO
import time

board = Arduino('COM3')

pin = 9  # Define o pino do servo

board.digital[pin].mode = SERVO  # Configura o pino como servo

def rotateServo(pino, angle):
    board.digital[pino].write(angle)
    time.sleep(3)  # Espera 5 segundos entre os movimentos

# Loop infinito alternando entre 0° e 180°
while True:
    rotateServo(pin, 0)
    rotateServo(pin, 180)
