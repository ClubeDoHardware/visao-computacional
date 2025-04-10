import cv2  
import mediapipe as mp  
import servo_braco3d as mao  #Módulo para mão robótica

# Vídeo da webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Tamanho da resolução do vídeo
cap.set(3, 640)  #Largura
cap.set(4, 480)  #Altura

#Detector de mãos do MediaPipe
hands = mp.solutions.hands
Hands = hands.Hands(max_num_hands=1)  #Detectar no máximo 1 mão

#Desenha as linhas entre os pontos da mão
mpDwaw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()  #Captura um frame
    frameRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #Converte para RGB
    results = Hands.process(frameRGB) 
    handPoints = results.multi_hand_landmarks  #Obtém os pontos das mãos detectadas
    h, w, _ = img.shape  #Obtém altura e largura da imagem
    pontos = []  #Armazena coordenadas dos pontos da mão

    if handPoints:
        for points in handPoints:
            #Desenha os pontos e conexões
            mpDwaw.draw_landmarks(img, points, hands.HAND_CONNECTIONS)

            #Percorre os pontos
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)  #Converte coordenadas normalizadas para pixels
                # cv2.putText(img, str(id), (cx, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.circle(img, (cx, cy), 4, (255, 0, 0), -1)  #Desenha um círculo nos pontos
                pontos.append((cx, cy))  #Adiciona o ponto à lista

            if pontos:
                #Calcula as distâncias entre os dedos
                distPolegar = abs(pontos[17][0] - pontos[4][0])
                distIndicador = pontos[5][1] - pontos[8][1]
                distMedio = pontos[9][1] - pontos[12][1]
                distAnelar = pontos[13][1] - pontos[16][1]
                distMinimo = pontos[17][1] - pontos[20][1]

                # Comandos para abrir ou fechar os dedos do braço robótico
                if distPolegar < 80:
                    mao.abrir_fechar(10, 0)  
                else:
                    mao.abrir_fechar(10, 1) 

                if distIndicador >= 1:
                    mao.abrir_fechar(9, 1)  
                else:
                    mao.abrir_fechar(9, 0) 

                if distMedio >= 1:
                    mao.abrir_fechar(8, 1) 
                else:
                    mao.abrir_fechar(8, 0) 
                if distAnelar >= 1:
                    mao.abrir_fechar(7, 1)  
                else:
                    mao.abrir_fechar(7, 0)  

                if distMinimo >= 1:
                    mao.abrir_fechar(6, 1)  
                else:
                    mao.abrir_fechar(6, 0)  

    #Exibe a imagem com os pontos e conexões desenhados
    cv2.imshow('Imagem', img)

    #Encerra com a tecla Q
    cv2.waitKey(1)
