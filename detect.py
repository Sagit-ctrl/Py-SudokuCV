import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np


name1 = 'test/' + 'test05' + '.png'

def check(train_data, train_label, source):
    label_rate = []
    for data in train_data:
        count = 0
        for i in range(30):
            for j in range(30):
                if  data[i][j] == source[i][j]:
                    count += 1
        label_rate.append(count)

    max = -1
    id = 0
    for i in range(len(label_rate)):
        if label_rate[i] >= max:
            max = label_rate[i]
            id = i

    return train_label[id]


img = 0
train_data = [] # dữ liệu training
train_label = [] # label của chúng

for num in range(1, 10, 1):
    for i in range(1, 11, 1):
        name = 'image/0' + str(num) + ' (' + str(i) + ').png'
        img = cv2.imread(name, 0)
        img = np.array(img)
        train_data.append(img)
        train_label.append(num)

img = cv2.imread(name1, 0)
img = cv2.GaussianBlur(img, (5, 5), 0)
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

cv2.imshow('Source', img)

horizal = img
vertical = img

scale_height = 20 #Scale này để càng cao thì số dòng dọc xác định sẽ càng nhiều
scale_long = 15

long = int(img.shape[1]/scale_long)
height = int(img.shape[0]/scale_height)

horizalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (long, 1))
horizal = cv2.erode(horizal, horizalStructure, (-1, -1))
horizal = cv2.dilate(horizal, horizalStructure, (-1, -1))

verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, height))
vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))

mask = vertical + horizal

cv2.imshow('Mask', mask)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

max = -1
table = []
x_max, y_max, w_max, h_max = 0, 0, 0, 0
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if cv2.contourArea(cnt) > max:
        x_max, y_max, w_max, h_max = x, y, w, h
        max = cv2.contourArea(cnt)
        table = img[y_max:y_max+h_max, x_max:x_max+w_max]

table = cv2.resize(table, (500, 500))
print(table.shape)
cv2.imshow('Table', table)

cropped_thresh_img = []
cropped_origin_img = []
countours_img = []

NUM_ROWS = 9
NUM_COLUMNS = 9
START_ROW = 0
for i in range(START_ROW, NUM_ROWS):
    for j in range(START_ROW, NUM_COLUMNS):
        thresh1 = img[y_max + round(i*h_max/NUM_ROWS):y_max + round((i+1)*h_max/NUM_ROWS), x_max + round(j*w_max/NUM_COLUMNS):x_max + round((j+1)*w_max/NUM_COLUMNS)]
        contours_thresh1, hierarchy_thresh1 = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        origin1 = img[y_max + round(i*h_max/NUM_ROWS):y_max + round((i+1)*h_max/NUM_ROWS), x_max + round(j*w_max/NUM_COLUMNS):x_max + round((j+1)*h_max/NUM_COLUMNS)]

        cropped_thresh_img.append(thresh1)
        cropped_origin_img.append(origin1)
        countours_img.append(contours_thresh1)

cropped_thresh_img1 = []
cropped_origin_img1 = []
countours_img1 = []

for i in range(START_ROW, NUM_ROWS):
    for j in range(START_ROW, NUM_COLUMNS):
        thresh1 = img[y_max + round(i*h_max/NUM_ROWS):y_max + round((i+1)*h_max/NUM_ROWS), x_max + round(j*w_max/NUM_COLUMNS):x_max + round((j+1)*w_max/NUM_COLUMNS)]
        contours_thresh1, hierarchy_thresh1 = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        origin1 = img[y_max + round(i*h_max/NUM_ROWS):y_max + round((i+1)*h_max/NUM_ROWS), x_max + round(j*w_max/NUM_COLUMNS):x_max + round((j+1)*w_max/NUM_COLUMNS)]

        cropped_thresh_img1.append(thresh1)
        cropped_origin_img1.append(origin1)
        countours_img1.append(contours_thresh1)

print(len(countours_img1))
# i = 7
# cv2.imshow('Answer' + str(i), cropped_origin_img1[i])

sources = []
position = []
for i, countour_img in enumerate(countours_img1):
    for cnt in countour_img:
        # if cv2.contourArea(cnt) > 00:
        x,y,w,h = cv2.boundingRect(cnt)
        if x > cropped_origin_img1[i].shape[1]*0.2 and x < cropped_origin_img1[i].shape[1]*0.9:
            source = cropped_origin_img1[i][y-1:y+29, x-5:x+25]
            source = cv2.threshold(source, 160, 255, cv2.THRESH_BINARY)[1]
            sources.append(source)
            position.append(i)

# for i in range(len(sources)):
#     cv2.imwrite(str(i) + '.png', sources[i])

for i in range(len(sources)):
    sources[i] = np.array(sources[i])

result = []
for i in range(len(sources)):
    a = check(train_data, train_label, sources[i])
    result.append(a)

board_test = ''
count1 = 0
for i in range(81):
    if position.count(i) != 0:
        board_test += str(result[count1])
        count1 += 1
    else:
        board_test += '0'

# cv2.waitKey()
