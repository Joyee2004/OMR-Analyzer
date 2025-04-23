import cv2

def preprocess(img): 
    img1 =  cv2.fastNlMeansDenoising(img, h=10, templateWindowSize=11,searchWindowSize=35)
    return cv2.bilateralFilter(img1,9,75,75)


def split_boxes(img, rows, cols):
    boxes = []
    h, w = img.shape
    row_height = h // rows
    col_width = w // cols
    for r in range(rows):
        for c in range(cols):
            box = img[r*row_height:(r+1)*row_height, c*col_width:(c+1)*col_width]
            boxes.append(box)
    return boxes

def draw_answers(img, marked, grading, answer_key, rows, cols):
    secW = int(img.shape[1] / cols)
    secH = int(img.shape[0] / rows)
    for i in range(rows):
        color = (0, 255, 0) if grading[i] == 1 else (0, 0, 255)
        cv2.circle(img, (int((marked[i]*secW)+secW/2), int((i*secH)+secH/2)), 12,color, cv2.FILLED)
        cv2.circle(img, (int((answer_key[i]*secW)+secW/2), int((i*secH)+secH/2)),12,(255, 0, 0), 2)
    return img

def draw_score(score, img):
    cv2.putText(img, f"Score: {score}%", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    return img
