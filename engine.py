import cv2
import numpy as np
from helper import split_boxes,  draw_score, preprocess

class OMRScanner:
    def __init__(self, image_path, answer_key, rows, cols):
        self.image_path = image_path
        self.answer_key = answer_key 
        self.rows = rows
        self.cols = cols
        
        
        self.img = cv2.imread(image_path)
        if self.img is None:
            raise ValueError(f"Failed to load image at: {image_path}")
        self.img = cv2.resize(self.img, (450, 650))
        
        self.report = {
            'marked_answers': [],
            'correct_answers': answer_key.copy(),
            'is_correct': [],
            'confidence_scores': [],
            'score': 0,
            'blank_answers': []
        }
#OTSU
    def calculate_dynamic_threshold(self, pixel_vals):
        
        all_values = pixel_vals.flatten()
        
        ret, _ = cv2.threshold((all_values * 255).astype(np.uint8), 0, 255, 
                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return ret / 255.0

    def detect_marked_answers(self, pixel_vals):
        
        threshold = self.calculate_dynamic_threshold(pixel_vals)
        marked_answers = []
        confidence_scores = []
        
        for row in pixel_vals:
            max_val = np.max(row)
            if max_val > threshold:
                marked = np.argmax(row)
                confidence = max_val
            else:
                marked = -1 
                confidence = 0
                
            marked_answers.append(marked)
            confidence_scores.append(confidence)
        
        return marked_answers, confidence_scores

    def draw_results(self, img, marked):
       
        secW = int(img.shape[1] / self.cols)
        secH = int(img.shape[0] / self.rows)
        
        for i in range(self.rows):
            if marked[i] == -1:  
                cv2.putText(img, "?", 
            (int((self.cols//2 * secW) + secW//2), int((i*secH) + secH//2)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            else:
               # correct answer -> green
                # incorrect answer -> red
                is_correct = marked[i] == self.answer_key[i]
                color = (0, 255, 0) if is_correct else (0, 0, 255)
                cv2.circle(img, 
                          (int((marked[i]*secW) + secW//2), int((i*secH) + secH//2)), 
                          8, color, cv2.FILLED)
            
           # expected answer -> blue 
            cv2.circle(img, 
                (int((self.answer_key[i]*secW) + secW//2), int((i*secH) + secH//2)),
                8, (255, 0, 0), 2)
            
        return img

    def process(self):
        if self.img is None:
            raise ValueError("Image not loaded properly")
    
        img_pre = preprocess(self.img.copy())
        
        if len(img_pre.shape) == 3:
            img_pre = cv2.cvtColor(img_pre, cv2.COLOR_BGR2GRAY)
        
        
        thresh = cv2.adaptiveThreshold(
            img_pre, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 31, 7
        )
        
       
        boxes = split_boxes(thresh, self.rows, self.cols)
        pixel_vals = np.array([cv2.countNonZero(box)/box.size for box in boxes])
        pixel_vals = pixel_vals.reshape((self.rows, self.cols))
        
        
        marked_answers, confidence_scores = self.detect_marked_answers(pixel_vals)
        
      
        valid_answers = [i for i, m in enumerate(marked_answers) if m != -1]
        if valid_answers:
            correct = sum(1 for i in valid_answers if marked_answers[i] == self.answer_key[i])
            score = int((correct / len(valid_answers)) * 100)
        else:
            score = 0
        
        
        self.report = {
            'marked_answers': marked_answers,
            'correct_answers': self.answer_key,
            'is_correct': [m == ak if m != -1 else None for m, ak in zip(marked_answers, self.answer_key)],
            'confidence_scores': confidence_scores,
            'score': score,
            'blank_answers': [i for i, m in enumerate(marked_answers) if m == -1],
            'threshold': self.calculate_dynamic_threshold(pixel_vals)
        }
        
      
        result_img = self.draw_results(self.img.copy(), marked_answers)
        final_img = draw_score(score, result_img)
        
        return final_img, score, self.report

    def generate_text_report(self):
        report = [
            f"OMR Evaluation Report",
            "="*40,
            f"Total Questions: {self.rows}",
            f"Answered: {self.rows - len(self.report['blank_answers'])}",
            f"Blank: {len(self.report['blank_answers'])}",
            f"Score (of answered): {self.report['score']}%",
            f"Detection Threshold: {self.report['threshold']:.2f}",
            "",
            "Item\tMarked\tCorrect\tStatus",
            "-"*40
        ]
        
        for i in range(self.rows):
            if i in self.report['blank_answers']:
                marked = "BLANK"
                status = "BLANK"
            else:
                marked = chr(65 + self.report['marked_answers'][i])  # A, B, C
                status = "CORRECT" if self.report['is_correct'][i] else "INCORRECT"
            
            correct = chr(65 + self.report['correct_answers'][i])
            report.append(f"{i+1}\t{marked}\t{correct}\t{status}")
        
        return "\n".join(report)