import cv2
import numpy as np
import math
import imageio



def display(img, frame_name="OpenCV Image"):
    height, width = img.shape[0:2]
    new_width = 700
    new_height = int(new_width * (height / width))
    img = cv2.resize(img, (new_width, new_height))
    cv2.imshow(frame_name, img)
    cv2.waitKey(0)


def open_img(file_path):
    if file_path.lower().split('.')[-1] in ['heic', 'heif']:
        heif_file = imageio.imread(file_path)
        img = cv2.cvtColor(heif_file, cv2.COLOR_RGB2BGR)
        height, width = img.shape[:2]
        new_width = width // 3
        new_height = height // 3
        img = cv2.resize(img, (new_width, new_height))
        return img
    else:
        img = cv2.imread(file_path)
    return img


class Blank:
    def __init__(self, file_path):
        self.file_path = file_path
        self.img = open_img(file_path)
        self.centers = self.getting_boxes()
        self.ratio = 0.74
        self.ver_ratio = None
        self.hor_ratio = None
        self.id = None
        self.var = None
        self.answers = {str(i): '' for i in range(1, 41)}

    def getting_boxes(self):
        raw_centers = []
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 85, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        i = 0
        min_area = 1000
        max_area = 100000

        for contour in contours:

            area = cv2.contourArea(contour)
            if i == 0:
                i = 1
                continue

            approx = cv2.approxPolyDP(
                contour, 0.05 * cv2.arcLength(contour, False), True)

            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])

            if len(approx) == 4 and min_area < area < max_area:
                x, y, w, h = cv2.boundingRect(contour)
                ratio = float(w) / h
                if 0.5 <= ratio <= 2:
                    # cv2.drawContours(self.img, [contour], 0, (0, 0, 255), 2)
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    raw_centers.append([[cx, cy], area])
                    # cv2.circle(self.img, (cx, cy), 7, (255, 255, 255), -1)

        # display(self.img)

        centers = self.find_closest_values(raw_centers)
        centers = self.sort_coordinates(self.get_distances(centers))

        return centers

    @staticmethod
    def sort_coordinates(points):
        center = np.mean([item[0] for item in points], axis=0)
        sorted_points = sorted(points, key=lambda point: np.arctan2(point[0][1] - center[1], point[0][0] - center[0]))

        mark = 0
        min_diff = 10 ** 10
        for i in range(len(sorted_points)):
            if min_diff > sum(sorted_points[i][1]):
                mark = i
                min_diff = sum(sorted_points[i][1])

        new_points = []
        for i in range(len(sorted_points)):
            point = (i + mark + 2) % len(sorted_points)
            if point != mark:
                new_points.append(sorted_points[point])
        return [point[0] for point in new_points]

    @staticmethod
    def get_distances(cen):
        out_boxs = []
        for box in cen:
            dstn = []
            for other_box in cen:
                dstn.append(
                    round(
                        math.hypot(abs(other_box[0] - box[0]), abs(other_box[1] - box[1]))))
            out_boxs.append([box, sorted(dstn, reverse=True)])
        return sorted(out_boxs, key=lambda item: sum(item[1]), reverse=True)

    @staticmethod
    def find_closest_values(cen):
        sorted_lst = sorted(
            cen,
            key=lambda item: sum([abs(item[1] - i[1]) for i in cen]))
        return [i[0] for i in sorted_lst[:5]]

    def get_perspective(self):
        img = self.img
        cen = self.centers
        row, col = img.shape[:2]
        pts1 = np.float32(cen)

        ratio = self.ratio
        cardH = math.sqrt(
            (pts1[2][0] - pts1[1][0]) * (pts1[2][0] - pts1[1][0]) + (pts1[2][1] - pts1[1][1]) * (
                    pts1[2][1] - pts1[1][1]))
        cardW = ratio * cardH
        pts2 = np.float32(
            [[pts1[0][0], pts1[0][1]], [pts1[0][0] + cardW, pts1[0][1]], [pts1[0][0] + cardW, pts1[0][1] + cardH],
             [pts1[0][0], pts1[0][1] + cardH]])

        M = cv2.getPerspectiveTransform(pts1, pts2)

        if cen[0][1] > cen[-2][1]:
            offsetSize = row
        elif cen[0][0] > cen[-2][0]:
            offsetSize = abs(cen[0][0] - cen[-2][0])
        else:
            offsetSize = 500

        transformed = np.zeros((int(cardW + offsetSize), int(cardH + offsetSize)), dtype=np.uint8)
        dst = cv2.warpPerspective(img, M, transformed.shape)

        self.img = dst

        self.centers = self.getting_boxes()
        self.get_ratio()
        self.img = self.img[
                   self.centers[0][1] - round(67 * self.ver_ratio): self.centers[-2][1] + round(
                       54 * self.ver_ratio),
                   self.centers[0][0] - round(68 * self.hor_ratio): self.centers[1][0] + round(
                       68 * self.hor_ratio)]

        return self.img

    def get_ratio(self):
        self.hor_ratio = abs(self.centers[0][0] - self.centers[1][0]) / 915
        self.ver_ratio = abs(self.centers[0][1] - self.centers[-1][1]) / 1234

    def check_line(self, image, first_check, count, inter, addition=0):
        pixels = []
        result = ''
        y = round(first_check[1] * self.ver_ratio)
        for checkbox in range(count):
            x = round((first_check[0] * self.hor_ratio) + (inter * self.ver_ratio) * checkbox)
            pixel = image[y, x]
            pixels.append(pixel)
        avg = sum(pixels,) / len(pixels)
        for i, pixel in enumerate(pixels):
            if pixel / avg < 0.8 and pixel < 70 or pixel < 30 or pixel / avg < 0.5:
                result += str(i+addition)
        return result

    def check_data(self):
        self.get_perspective()
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray, alpha=0.5, beta=70)
        gray = cv2.equalizeHist(gray)
        # _, img = cv2.threshold(self.img, 112, 200, cv2.THRESH_BINARY)
        img = cv2.GaussianBlur(gray, (17, 17), 0)

        # display(img)

        blank_id0 = self.check_line(img, [243, 195], 10, 45, 0)
        blank_id1 = self.check_line(img, [243, 255], 10, 45, 0)
        self.id = blank_id0 + blank_id1
        self.var = self.check_line(img, [243, 315], 10, 45, 1)

        start = 0
        for i in range(1, 11):
            answer = self.check_line(img, [126, 442 + 35 * (i - 1)], 5, 40, 1)
            correction = self.check_line(img, [335, 440 + 35 * (i - 1)], 5, 40, 1)
            if correction == '':
                self.answers[f'{start + i}'] = answer
            else:
                self.answers[f'{start + i}'] = correction

        start = 10
        for i in range(1, 11):
            answer = self.check_line(img, [128, 861 + 35 * (i - 1)], 5, 40, 1)
            correction = self.check_line(img, [335, 861 + 35 * (i - 1)], 5, 40, 1)
            if correction == '':
                self.answers[f'{start + i}'] = answer
            else:
                self.answers[f'{start + i}'] = correction

        start = 20
        for i in range(1, 11):
            answer = self.check_line(img, [609, 441 + 35 * (i - 1)], 5, 40, 1)
            correction = self.check_line(img, [818, 441 + 35 * (i - 1)], 5, 40, 1)
            if correction == '':
                self.answers[f'{start + i}'] = answer
            else:
                self.answers[f'{start + i}'] = correction

        start = 30
        for i in range(1, 11):
            answer = self.check_line(img, [606, 858 + 35 * (i - 1)], 5, 40, 1)
            correction = self.check_line(img, [815, 858 + 35 * (i - 1)], 5, 40, 1)
            if correction == '':
                self.answers[f'{start + i}'] = answer
            else:
                self.answers[f'{start + i}'] = correction

        return self


def checker(file):
    try:
        blank = Blank(file)
        blank.check_data()
    except:
        return 'invalid'
    return blank


if __name__ == "__main__":
    blank = checker('images/test.jpg')

    print(f'ID: {blank.id}')
    print(f'Variant: {blank.var}')
    for row in range(5):
        for answer in list(blank.answers.items())[8 * row:8 * (row + 1)]:
            print(f'Ответ {answer[0] if int(answer[0]) > 9 else f'0{answer[0]}'}: {answer[1]}', end='  ||  ')
        print()
