import cv2
import numpy as np
import os

# Make sure that when recording we will save a new file
# and also when taking a picture
dirPath = os.getcwd()
vidFlag, i = 1, 1
while (vidFlag):
    if (os.path.isfile(dirPath + '\output_' + str(i) + '.avi')):
        i = i + 1
    else:
        vidFlag = 0
fileNameVid = "output_" + str(i) + ".avi"
picFlag, j = 1, 1
while (picFlag):
    if (os.path.isfile(dirPath + '\pic_' + str(j) + '.png')):
        j = j + 1
    else:
        picFlag = 0
fileNamePic = "pic_" + str(j) + ".png"

recordingFlag = -1  # enter recording mode
savingFlag = -1  # creating a video file

min_YCrCb = np.array([40, 140, 77], np.uint8)
max_YCrCb = np.array([150, 170, 127], np.uint8)

cap = cv2.VideoCapture(0)

while (cap.isOpened()):
    ret, frame = cap.read()  # Capture frame-by-frame
    if ret is True:
        key = cv2.waitKey(1) & 0xff
        frame = cv2.flip(frame, 1)

        imageYCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
        imageYCrCb = cv2.GaussianBlur(imageYCrCb, (3, 3), 0)
        skinMask = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)
        skinYCrCb = cv2.bitwise_and(frame, frame, mask=skinMask)
        skinYCrCb[:, :, :] = skinYCrCb[:, :, :] * [1, 255, 1]
        skinYCrCb = cv2.bitwise_or(frame, skinYCrCb)

        # Display the resulting frame
        cv2.imshow('frame', skinYCrCb)

        if key == ord('s'):  # press 's' to Save
            if savingFlag == -1:
                savingFlag = 1
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(fileNameVid, fourcc, 20.0, (640, 480))
            recordingFlag = recordingFlag * -1
        if recordingFlag == 1:
            out.write(skinYCrCb)

        if key == ord('d'):  # press 'd' to take a photo
            cv2.imwrite(fileNamePic, skinYCrCb)

        if key == ord('p'):  # press 'p' to Pause
            while True:
                key2 = cv2.waitKey(1) or 0xff
                cv2.imshow('frame', skinYCrCb)
                if key2 == ord('p'):
                    break

        if key == ord('q'):  # press 'q' to Exit
            break

# When done, release the capture
if savingFlag == 1:
    out.release()
cap.release()
cv2.destroyAllWindows()
