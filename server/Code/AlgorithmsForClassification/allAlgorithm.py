# import numpy as np
import numpy as np


def nose_classification(points_nose):
    np.array(points_nose)
    x = points_nose[:9]
    y = points_nose[9:]
    dy = y[6] - y[0]
    dx = x[8] - x[4]
    if dy < 140:
        return "קטן"
    elif dx > 90:
        return "רחב"
    else:
        return "ארוך"


def eye_classification(points_eye):
    np.array(points_eye)
    x = points_eye[:12]
    y = points_eye[12:]
    dy = (y[4]+y[5]-y[1]-y[2])/2
    dx = x[3]-x[0]
    if dy > 23:
        return "גדולות"
    elif dx > 70:
        return "מוארכות"
    else:
        return "קטנות"


def mouth_classification(points_mouth):
    np.array(points_mouth)
    x = points_mouth[:20]
    y = points_mouth[20:]
    top = y[14] - y[3]
    bottom = y[9] - y[18]
    dx = max(x)-min(x)
    if dx < 150:
        return "קטן"
    elif top > 10 and bottom > 30:
        return "עבה"
    else:
        return "בינוני"


# arr = [140, 182, 223, 249, 279,	317, 354, 316, 278,	246, 218, 177,	151, 222, 249.1, 279.1,	341, 277, 246.1, 219, 339, 328,	325, 332, 328.1, 335, 347, 383,	401, 404, 399, 380,	342, 342.1,	347.1, 345,	349, 372, 376, 371]
# s = mouth_classification(arr)
# print(s)
# arr = [108, 134, 166, 190, 164, 133, 296, 323, 352, 372, 352, 323, 146, 128, 128, 150, 153, 153, 156, 135, 137, 154, 161, 160]
# s = eye_classification(arr)
# print(s)
