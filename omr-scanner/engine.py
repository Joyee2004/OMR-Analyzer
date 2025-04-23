import cv2
import numpy as np
from helper import split_boxes, draw_answers, draw_score, preprocess

class OMRScanner:
    def __init__(self, image_path, answer_key, rows, cols):
        self.image_path = image_path
        self.answer_key = answer_key
        self.rows = rows
        self.cols = cols
        self.img = cv2.imread(image_path)
        self.img = cv2.resize(self.img, (600, 600)) if self.img is not None else None
        self.report = {
            'marked_answers': [],
            'correct_answers': answer_key.copy(),
            'is_correct': [],
            'score': 0
        }

    def process(self):
        if self.img is None:
            raise ValueError("Image not loaded properly")
        
        img_copy = self.img.copy()
        img_pre = preprocess(img_copy)
        
       
        thresh = cv2.threshold(cv2.cvtColor(img_pre, cv2.COLOR_BGR2GRAY), 100, 255, cv2.THRESH_BINARY_INV)[1]
        
        
        boxes = split_boxes(thresh, self.rows, self.cols)
        pixel_vals = np.array([cv2.countNonZero(box) for box in boxes]).reshape((self.rows, self.cols))
        
       
        marked = np.argmax(pixel_vals, axis=1)
        grading = (marked == self.answer_key).astype(int)
        score = int((np.sum(grading) / self.rows) * 100)
        
        
        self.report = {
            'marked_answers': marked.tolist(),
            'correct_answers': self.answer_key,
            'is_correct': grading.tolist(),
            'score': score
        }
        
       
        result_img = draw_answers(self.img.copy(), marked, grading, self.answer_key, self.rows, self.cols)
        final = draw_score(score, result_img)
        
        return final, score, self.report

    def generate_text_report(self):
        report = f"OMR Evaluation Report\n{'='*30}\n"
        report += f"Total Questions: {self.rows}\n"
        report += f"Score: {self.report['score']}%\n\n"
        
        report += "Item\tMarked\tCorrect\tStatus\n"
        report += "-"*30 + "\n"
        
        for i in range(self.rows):
            status = "CORRECT" if self.report['is_correct'][i] else "INCORRECT"
            report += f"{i}\t{self.report['marked_answers'][i]+1}\t{self.report['correct_answers'][i]}\t{status}\n"
        
        return report