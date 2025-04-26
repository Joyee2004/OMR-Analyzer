import cv2
import matplotlib.pyplot as plt
import io
import base64

def preprocess(img):

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    denoised = cv2.medianBlur(img, 3) #kernel 3 / 5 is used
    
    
    denoised = cv2.fastNlMeansDenoising(denoised, h=7, templateWindowSize=7, searchWindowSize=29)
    
   
    filtered = cv2.edgePreservingFilter(denoised, flags=1, sigma_s=60, sigma_r=0.4)
    
    
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
    if len(filtered.shape) == 3:
        filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    enhanced = clahe.apply(filtered)
    
    return enhanced



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

def draw_score(score, img):
    cv2.putText(img, f"Score: {score}%", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 1)
    return img

def generate_chart(num_correct, num_wrong, num_blank):
   
    labels = ['Correct', 'Wrong', 'Blank']
    values = [num_correct, num_wrong, num_blank]
    
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#4CAF50", "#F44336", "#FFC107"])
    ax.axis('equal') 
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    chart_b64 = base64.b64encode(buf.read()).decode('utf-8')
    return chart_b64

