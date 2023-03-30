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

detector = htm.handDetector(detectionCon=0.75)

left_hand_tipIds = [4, 8, 12, 16, 20]
right_hand_tipIds = [4, 8, 12, 16, 20]

# loop over the sound files and create Pygame sound objects for each file
for file in sound_files:  # sitar
    sound = pygame.mixer.Sound(file)
    sounds.append(sound)
for file in sound_files1:  # piano
    sound = pygame.mixer.Sound(file)
    sounds1.append(sound)

# Import necessary libraries
from flask import Flask, render_template, Response, url_for

# Initialize the Flask app
app = Flask(__name__)

from flask import Flask, render_template
import cv2

wCam, hCam = 1280, 720
camera = cv2.VideoCapture(0)
camera.set(3, wCam)
camera.set(4, hCam)
detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]


def gen_frames():
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame, 1)

        frame = detector.findHands(frame)
        lmList_left = detector.findPosition(frame, draw=False, handNo=0)
        lmList_right = detector.findPosition(frame, draw=False, handNo=-1)
        if lmList_right == lmList_left:
            lmListCommon = lmList_right

        if len(lmList_left) != 0 and lmList_left != lmList_right:
            fingers = []
            # Checking left or right hand
            if lmList_left[1][1] < lmList_left[0][1]:
                # Thumb
                if lmList_left[tipIds[0]][1] < lmList_left[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                # Thumb
                if lmList_left[tipIds[0]][1] > lmList_left[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList_left[tipIds[id]][2] < lmList_left[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # print(fingers)
            totalFingers = fingers.count(1)

            sounds[totalFingers - 1].play()
            time.sleep(0.01)
            #cv2.circle(frame, (1228, hCam - 60), 38, (188, 241, 288), cv2.FILLED)
            #cv2.putText(frame, str(totalFingers), (1203, hCam - 33), cv2.FONT_HERSHEY_PLAIN, 5, (62, 78, 240), 12)



        if len(lmList_right) != 0 and lmList_left != lmList_right:
            fingers = []
            # Checking left or right hand
            if lmList_right[1][1] < lmList_right[0][1]:
                # Thumb
                if lmList_right[tipIds[0]][1] < lmList_right[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                # Thumb
                if lmList_right[tipIds[0]][1] > lmList_right[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList_right[tipIds[id]][2] < lmList_right[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # print(fingers)
            totalFingers = fingers.count(1)
            sounds1[totalFingers - 1].play()
            time.sleep(0.01)
            #cv2.circle(frame, (55, hCam - 60), 38, (188, 241, 288), cv2.FILLED)
            #cv2.putText(frame, str(totalFingers), (30, hCam - 33), cv2.FONT_HERSHEY_PLAIN, 5, (62, 78, 240), 12)

        if len(lmListCommon) != 0:
            fingers = []
            # Checking left or right hand
            if lmListCommon[1][1] < lmListCommon[0][1]:
                # Thumb
                if lmListCommon[tipIds[0]][1] < lmListCommon[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                # Thumb
                if lmListCommon[tipIds[0]][1] > lmListCommon[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmListCommon[tipIds[id]][2] < lmListCommon[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # print(fingers)
            totalFingers = fingers.count(1)

            # check if hand is in right or left side of the screen
            # If hand is in left sitar else piano
            if lmListCommon[0][1] < 640:
                sounds[totalFingers - 1].play()
                # cv2.circle(frame, (55, hCam - 60), 38, (188, 241, 288), cv2.FILLED)
                # cv2.putText(frame, str(totalFingers), (30, hCam - 33), cv2.FONT_HERSHEY_PLAIN, 5, (62, 78, 240), 12)
                time.sleep(0.01)



            else:
                sounds1[totalFingers - 1].play()
                # cv2.circle(frame, (1228, hCam - 60), 38, (188, 241, 288), cv2.FILLED)
                # cv2.putText(frame, str(totalFingers), (1203, hCam - 33), cv2.FONT_HERSHEY_PLAIN, 5, (62, 78, 240), 12)
                time.sleep(0.01)


        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
