import cv2
import numpy as np
import math
from PIL import Image


def getting_file(file_name: str):
    return cv2.imread(file_name)


def getting_boxes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 50, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    centers = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        min_area = 2000
        max_area = 15000
        x1, y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and area > min_area and area < max_area:
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = float(w) / h
            if ratio >= 0.8 and ratio <= 1.2:
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append([cX, cY])
    if len(centers) == 3:
        return centers
    else:
        print('С изображением что-то не так!')
        exit(0)


def getting_distances(boxes):
    boxesWithDistances = []
    for box in range(3):
        dstn = []
        for other_box in range(3):
            dstn.append(
                int(math.hypot(abs(boxes[other_box][0] - boxes[box][0]), abs(boxes[other_box][1] - boxes[box][1]))))
        boxesWithDistances.append([boxes[box], dstn])
    return boxesWithDistances


def getting_rates(boxes):
    main_box = boxes[0]
    right_box = boxes[1]
    bottom_box = boxes[2]
    ratioX = abs(main_box[0][0] - right_box[0][0]) / 915
    ratioY = abs(main_box[0][1] - bottom_box[0][1]) / 1350
    return ratioX, ratioY


def get_angle(distances):
    if distances[0][0][0] - distances[2][0][0] != 0:
        y_line = distances[0][0][1] - distances[2][0][1]
        x_line = distances[0][0][0] - distances[2][0][0]
        rad = np.arctan(x_line / y_line)
        return abs(math.degrees(rad) - 90)
    else:
        return 0


def blankdata(image):
    centers = getting_boxes(image)
    distances = getting_distances(centers)
    distances = sorted(distances, key=lambda box: sum(box[1]))
    sorted_distances = sorted(distances, key=lambda box: math.hypot(box[0][0], box[0][1]))
    return {
        'centers': centers,
        'sorted_distances': sorted_distances
    }


def getting_blank(file_name):
    image = getting_file(file_name)
    blank = blankdata(image)
    radians = get_angle(blank['sorted_distances'])
    if radians != 0:
        image = Image.fromarray(image)
        image = image.rotate(radians, expand=True)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    blank = blankdata(image)
    rateX, rateY = getting_rates(blank['sorted_distances'])
    img = image[
          blank['sorted_distances'][0][0][1] - int(68 * rateY): blank['sorted_distances'][2][0][1] + int(68 * rateY),
          blank['sorted_distances'][0][0][0] - int(68 * rateX): blank['sorted_distances'][1][0][0] + int(68 * rateX)]
    return img, rateX, rateY


def check_line(image, firstChB, count, inter, rX, rY, addition=0):
    result = ''
    for checkbox in range(count):
        pixel = image[int(firstChB[1] * rY), int((firstChB[0] + inter * checkbox) * rX)]
        # cv2.circle(image, (int((firstChB[0] + inter * checkbox)* rX), int(firstChB[1] * rY)), 7, (0, 0, 0), -1)
        if pixel < 100:
            result += str(checkbox + addition)
    # cv2.imshow('test', image)
    # cv2.waitKey(0)
    return result


def check_blank(img, rateX, rateY):
    result = {
        'blank_id': 0,
        'var': 0,
        'answers': {},
    }
    img = cv2.GaussianBlur(img, (17, 17), 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blank_id0 = check_line(img, [243, 195], 10, 45, rateX, rateY, 0)
    blank_id1 = check_line(img, [243, 255], 10, 45, rateX, rateY, 0)
    result['blank_id'] = blank_id0 + blank_id1
    var = check_line(img, [243, 315], 10, 45, rateX, rateY, 0)
    result['var'] = var

    start = 0
    for i in range(1, 11):
        answer = check_line(img, [126, 438 + 35 * (i - 1)], 5, 40, rateX, rateY, 1)
        correstion = check_line(img, [335, 438 + 35 * (i - 1)], 5, 40, rateX, rateY, 1)
        if correstion == '':
            result['answers'][f'{start + i}'] = answer
        else:
            result['answers'][f'{start + i}'] = correstion

    start = 10
    for i in range(1, 11):
        answer = check_line(img, [126, 860 + 35 * (i - 1)], 5, 40, rateX, rateY, 1)
        correstion = check_line(img, [335, 860 + 35 * (i - 1)], 5, 40, rateX, rateY, 1)
        if correstion == '':
            result['answers'][f'{start + i}'] = answer
        else:
            result['answers'][f'{start + i}'] = correstion

    start = 20
    for i in range(1, 11):
        answer = check_line(img, [608, 438 + 35 * (i - 1)], 5, 40, rateX, rateY, 1)
        correstion = check_line(img, [817, 438 + 35 * (i - 1)], 5, 40, rateX, rateY, 1)
        if correstion == '':
            result['answers'][f'{start + i}'] = answer
        else:
            result['answers'][f'{start + i}'] = correstion

    start = 30
    for i in range(1, 11):
        answer = check_line(img, [608, 860 + 35 * (i - 1)], 5, 40, rateX, rateY, 1)
        correstion = check_line(img, [817, 860 + 35 * (i - 1)], 5, 40, rateX, rateY, 1)
        if correstion == '':
            result['answers'][f'{start + i}'] = answer
        else:
            result['answers'][f'{start + i}'] = correstion
    return result


def checker(file):
    img, rX, rY = getting_blank(file)
    print(rX, rY)
    results = check_blank(img, rX, rY)
    return results, Image.fromarray(img)


if __name__ == '__main__':
    print(checker(input()))
