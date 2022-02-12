import beepy
#import kakao_utils

def beepsound():
    beepy.beep(sound=7)

import cv2
import tensorflow.keras
import numpy as np

def preprocessing(frame):
    size = (224, 224)
    frame_resized = cv2.resize(frame,size,interpolation=cv2.INTER_AREA)

    frame_normalized = (frame_resized.astype(np.float32)/127.0-1)

    frame_reshaped = frame_normalized.reshape((1,224,224,3))

    return frame_reshaped
model_filename='keras_model.h5'
model = tensorflow.keras.models.load_model(model_filename)

capture = cv2.VideoCapture(0)

capture.set(cv2.CAP_PROP_FRAME_WIDTH,300)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,250)

sleep_cnt  =  1# 30 초간 "졸림" 상태를 확인하기  위한 변수
while  True:

    ret,frame = capture.read()
    if ret == True:
        print("read success!")

        frame_flipped = cv2.flip(frame,1)

        cv2.imshow("videoFrame", frame_flipped)

        if cv2.waitKey(200) >0:break

        preprocessed = preprocessing(frame_flipped)

        prediction=model.predict(preprocessed)


        if prediction[0,0] < prediction [0,1]:
            print("not wearing a mask")
            sleep_cnt += 1

            if sleep_cnt %  5 == 0:
                sleep_cnt = 1
                print('5 seconds without a mask')
                beepsound()
                #send_music_link()
                break
        else:
            print("wearing a mask")
            sleep_cnt = 1

capture.release()

cv2.destroyAllWindows()