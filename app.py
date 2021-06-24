"""
Made by:
- Giuliana Rasmussen do Valle Saes, RA: 0040961623024
- Humberto de Souza Reque Junior, RA: 0040961623023
"""

import cv2 as cv
import os
from handDetector import *
import random

cap = cv.VideoCapture(0, cv.CAP_DSHOW)

# folderPath = "JankenPo"
# myList = os.listdir(folderPath)
# print(myList)
# overlayList = []
# for imPath in myList:
#     image = cv.imread(f'{folderPath}/{imPath}')
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image)

# print(len(overlayList))

detector = handDetector(detectionCon=0.75)

fingertipIds = [4, 8, 12, 16, 20]


optHumanChoosen = optAIChoosen = False
optHuman = optAI = whoWon = ""

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)


    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[fingertipIds[0]][1] >= lmList[fingertipIds[0] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[fingertipIds[id]][2] <= lmList[fingertipIds[id] - 3][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        print(fingers)

        if (optHumanChoosen == False):
            if (fingers == [0, 1, 1, 0, 0] or fingers == [1, 1, 1, 0, 0]):
                optHuman = "Scissor"
                optHumanChoosen = True
            elif (fingers == [1, 1, 1, 1, 1]):
                optHuman = "Paper"
                optHumanChoosen = True
            elif (fingers == [0, 0, 0, 0, 0] or fingers == [1, 0, 0, 0, 0]):
                optHuman = "Rock"
                optHumanChoosen = True


        if (optHumanChoosen and not optAIChoosen):
            randomNumber = random.randint(1,3)

            if (randomNumber == 1):
                optAI = "Scissor"
                optAIChoosen = True
            if (randomNumber == 2):
                optAI = "Paper"
                optAIChoosen = True
            if (randomNumber == 3):
                optAI = "Rock"
                optAIChoosen = True
            
        print(optAI)

        totalFingers = fingers.count(1)
        # print(totalFingers)

        cv.rectangle(img, (20, 20), (160, 60), (0, 0, 0), cv.FILLED)
        cv.putText(img, "Human Choice", (20, 20), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        cv.putText(img, optHuman, (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        cv.rectangle(img, (420, 20), (620, 60), (125, 125, 125), cv.FILLED)
        cv.putText(img, "AI Choice", (420, 20), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        cv.putText(img, optAI, (420, 50), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        # cv.putText(img, str(totalFingers), (45, 375), cv.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

        if (optHumanChoosen and optAIChoosen):
            if(optHuman == "Scissor" and optAI == "Scissor"):
                whoWon = "It's a Tie"
            if(optHuman == "Scissor" and optAI == "Paper"):
                whoWon = "Human Wins"
            if(optHuman == "Scissor" and optAI == "Rock"):
                whoWon = "AI Wins"
            if(optHuman == "Paper" and optAI == "Scissor"):
                whoWon = "AI Wins"
            if(optHuman == "Paper" and optAI == "Paper"):
                whoWon = "It's a Tie"
            if(optHuman == "Paper" and optAI == "Rock"):
                whoWon = "Human Wins"
            if(optHuman == "Rock" and optAI == "Scissor"):
                whoWon = "Human Wins"
            if(optHuman == "Rock" and optAI == "Paper"):
                whoWon = "AI Wins"
            if(optHuman == "Rock" and optAI == "Rock"):
                whoWon = "It's a Tie"
        
        cv.putText(img, whoWon, (240, 240), cv.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 8)
    
    else:
        optHumanChoosen = optAIChoosen = False
        optHuman = optAI = whoWon = ""

    cv.imshow("Image", img)
    cv.waitKey(1)

# Define escape key
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()