import streamlit as st
import cv2
import numpy as np
import base64
from engine import OMRScanner
from helper import generate_chart  
from PIL import Image
import io



def decode_uploaded_image(uploaded_file):
   
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img

def file_to_text(uploaded_file):
    
    return uploaded_file.read().decode("utf-8")

def process_omr(image, answer_text, rows, cols, marks_per_correct, penalty_per_wrong):
 
    temp_image_path = "temp_image.png"
    cv2.imwrite(temp_image_path, image)
    try:
        answer_key = [int(x) for x in answer_text.replace(",", " ").split()]
    except Exception as e:
        st.error("Error parsing answer key. Check sample file format.")
        return None, None
    scanner = OMRScanner(temp_image_path, answer_key, int(rows), int(cols))
    try:
        final_img, score, report_data = scanner.process()
    except Exception as e:
        st.error(f"Error during OMR processing: {e}")
        return None, None
    
    valid = [i for i, m in enumerate(report_data['marked_answers']) if m != -1]
    num_correct = sum(1 for i in valid if report_data['marked_answers'][i] == answer_key[i])
    num_wrong = len(valid) - num_correct
    num_blank = len(report_data['blank_answers'])
    final_score = (num_correct * marks_per_correct) + (num_wrong * penalty_per_wrong)
    report_html = f"""
    <div style="background-color: #f7f7f7; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 12px #aaa; margin-bottom: 20px;">
      <h2 style="color: #2c3e50; text-align: center;">OMR Scanning Report</h2>
      <hr>
      <p><strong>Total Questions:</strong> {int(rows)}</p>
      <p><strong>Answered:</strong> {int(rows)-num_blank}</p>
      <p><strong>Blank:</strong> {num_blank}</p>
      <p><strong>Raw Score (of answered):</strong> {score}%</p>
      <p><strong>Final Score (with marking scheme):</strong> {final_score}</p>
      <p><strong>Correct:</strong> {num_correct}</p>
      <p><strong>Wrong:</strong> {num_wrong}</p>
      <hr>
      <pre style="background-color: #ecf0f1; padding: 10px; border-radius: 5px;">{scanner.generate_text_report()}</pre>
    </div>
    """
    chart_b64 = generate_chart(num_correct, num_wrong, num_blank)
    return final_img, (report_html, scanner.generate_text_report(), chart_b64)

def main():
    st.title("OMR Analyzer")
    
    
    svg_url = "https://www.svgrepo.com/show/476481/study.svg"
    st.markdown(f"""<div style="text-align: center;">
        <img src="{svg_url}" width="150"/>
    </div>""", unsafe_allow_html=True)
    
    # Inject CSS for background image and center form styling
    st.markdown("""
        <style>
        body {
            background-image: url("https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm0zNDctYmFpZmVybm4tMDcuanBn");
            background-size: cover;
            background-repeat: no-repeat;
        }
        .center-form {
            background: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: auto;
        }
        </style>
        """, unsafe_allow_html=True)
    
    tabs = st.tabs(["Home", "Process OMR", "About"])
    

    with tabs[0]:
        st.header("About OMR Scanner")
        st.write("""
            This application uses computer vision and image processing concepts to scan and process OMR (Optical Mark Recognition) sheets. 
            You can upload your own images and answer key to process your OMR and generate detailed report and data visualisations.
        """)
        

    with tabs[1]:
        st.header("Process Your Own OMR")
        with st.container():
            st.markdown('<div class="center-form">', unsafe_allow_html=True)
            with st.form(key="omr_form"):
                image_file = st.file_uploader("Upload OMR Image", type=["png", "jpg", "jpeg"])
                answer_file = st.file_uploader("Upload Answer Key (txt)", type=["txt"])
                st.markdown("### Marking Scheme")
                marks_per_correct = st.number_input("Marks per Correct Answer", value=4.0)
                penalty_per_wrong = st.number_input("Penalty per Wrong Answer", value=-1.0)
                st.markdown("### Layout Options")
                rows = st.number_input("Number of Questions (Rows)", value=20, step=1)
                cols = st.number_input("Number of Options (Cols)", value=4, step=1)
                submit_button = st.form_submit_button("Process OMR")
            st.markdown('</div>', unsafe_allow_html=True)
            
        if submit_button:
            if image_file is None or answer_file is None:
                st.error("Please upload both an image and an answer key file.")
            else:
                image = decode_uploaded_image(image_file)
                temp_image_path = "temp_image.png"
                cv2.imwrite(temp_image_path, image)
                answer_text = file_to_text(answer_file)
                final_img, result = process_omr(image, answer_text, rows, cols, marks_per_correct, penalty_per_wrong)
                if final_img is not None:
                    report_html, report_text, chart_b64 = result
                    st.subheader("Report")
                    st.markdown(report_html, unsafe_allow_html=True)
                    st.subheader("Annotated Image")
                    final_img_rgb = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
                    st.image(final_img_rgb, channels="RGB")
                    chart_bytes = base64.b64decode(chart_b64)
                    chart_img = Image.open(io.BytesIO(chart_bytes))
                    st.subheader("Score Visualization")
                    st.image(chart_img, caption="Score Distribution", use_column_width=True)
                    st.download_button(
                        label="Download Report",
                        data=report_text,
                        file_name="omr_report.txt",
                        mime="text/plain"
                    )
    

    with tabs[2]:
        st.header("About")
        st.markdown("""
            **OMR Analyzer**  
            This application uses computer vision to process Optical Mark Recognition (OMR) sheets.  
            It uses a custom engine for detecting marked answers along with score calculation and visualization.  
            \n\n
            
        """)
        
if __name__ == '__main__':
    main()