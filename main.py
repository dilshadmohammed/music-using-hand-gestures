import cv2
import time
import pygame
import HandTrackingModule as htm

# initialize pygame mixer
pygame.mixer.init()
pygame.mixer.set_num_channels(25)

# define list of sound files
sound_files = ['soundfiles/sitar1.wav', 'soundfiles/sitar2.wav', 'soundfiles/sitar3.wav',
               'soundfiles/sitar4.wav', 'soundfiles/sitar5.wav', 'soundfiles/sitar0.wav']

sound_files1 = ['soundfiles/piano-Gnew.wav', 'soundfiles/piano-A.wav', 'soundfiles/piano-B.wav',
                'soundfiles/piano-C.wav', 'soundfiles/piano-D.wav', 'soundfiles/piano-Fnew.wav']

# create  empty lists for the sound objects
sounds = []
sounds1 = []

# loop over the sound files and create Pygame sound objects for each file
for file in sound_files:  # sitar
    sound = pygame.mixer.Sound(file)
    sounds.append(sound)
for file in sound_files1:  # piano
    sound = pygame.mixer.Sound(file)
    sounds1.append(sound)

# width and height of camera
wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

previousTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
        # Checking left or right hand
        if lmList[1][1] < lmList[0][1]:
            # Thumb
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)

        # check if hand is in right or left side of the screen
        # If hand is in left sitar else piano
        if lmList[0][1] < 640:
            sounds[totalFingers - 1].play()
            time.sleep(0.15)

            cv2.rectangle(img, (10, hCam - 117), (85, hCam - 17), (13, 221, 224), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (23, hCam - 42), cv2.FONT_HERSHEY_PLAIN, 5, (235, 189, 23), 12)

        else:
            sounds1[totalFingers - 1].play()
            time.sleep(0.1)

            cv2.rectangle(img, (1185, hCam - 117), (1270, hCam - 17), (13, 221, 224), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (1198, hCam - 42), cv2.FONT_HERSHEY_PLAIN, 5, (235, 189, 23), 12)

    # calculating fps
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, f'FPS: {int(fps)}', (wCam - 77, 23), cv2.FONT_HERSHEY_PLAIN, 1, (156, 2, 245), 1)
    cv2.imshow("Image", img)

    # Wait for a key press and check if the 'q' key was pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the resources
cap.release()
cv2.destroyAllWindows()
