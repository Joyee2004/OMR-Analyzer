from engine import OMRScanner
import cv2

if __name__ == "__main__":
    image_path = "img2.png"
    answer_key = [4, 4, 2, 3, 4, 2, 4, 1, 1, 2, 1, 3, 1, 4, 3]
    marked_key = [2, 4, 0, 2, 1, 3, 0, 0, 3, 0, 3, 4, 3, 3, 2]
    rows, cols = 15,4
    
    scanner = OMRScanner(image_path, answer_key, rows, cols)
    final_img, score, report = scanner.process()
    accuracy_score = 0
    for i in range(0,10):
        if (report['marked_answers'][i] == marked_key[i]):
            accuracy_score+=1
        elif (marked_key[i] == 0):
            accuracy_score+=1


 
    print(scanner.generate_text_report())
    print(accuracy_score)
    
    cv2.imwrite("res.png",final_img)
    cv2.imshow("OMR Result", final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()