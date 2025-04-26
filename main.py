from engine import OMRScanner
import cv2

if __name__ == "__main__":
    image_path = "../Images/img3.png"
    answer_key = [3, 3, 1, 2, 3, 1, 3, 0, 0, 1, 0, 2, 0, 3, 2, 1 , 0, 1, 2, 3]
    marked_key = [2, 2, 3, 1, 1, 0, 2, 3, 2, 2, 4, 4, 1, 1, 3, 4, 0, 0, 1, 3]
    rows, cols = 20,4
    
    scanner = OMRScanner(image_path, answer_key, rows, cols)
    final_img, score, report = scanner.process()
    accuracy_score = 0
    # for i in range(0,rows):
    #     if (report['marked_answers'][i] == marked_key[i]):
    #         accuracy_score+=1
    #     elif (marked_key[i] == 0):
    #         accuracy_score+=1


 
    print(scanner.generate_text_report())
    print(accuracy_score)
    
    cv2.imwrite("res.png",final_img)
    cv2.imshow("OMR Result", final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()