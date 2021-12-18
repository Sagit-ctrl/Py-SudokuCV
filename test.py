import cv2

video = cv2.VideoCapture(0)
while True:
    check, frame = video.read()
    # frame = cv2.GaussianBlur(frame, (5, 5), 0)
    _, frame = cv2.threshold(frame, 170, 255, cv2.THRESH_BINARY)

    cv2.imshow("Capturing",frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

showPic = cv2.imwrite("filename.jpg",frame)
print(showPic)

video.release()
cv2.destroyAllWindows()