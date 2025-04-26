# OMR Analyzer

OMR Analyzer is an image processing application that uses computer vision techniques to scan and evaluate Optical Mark Recognition (OMR) sheets. This project was developed as part of an image processing course project and leverages Streamlit for the user interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [GitHub (Virtual Environment with Python 3.11)](#github-installation)
  - [Using Docker](#docker-installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Methods Adopted](#methods-adopted)
- [License](#license)

## Features

- **Image Preprocessing:** Converts uploaded images to grayscale, denoises, removes salt and pepper noise, enhances the edges and enhances contrast via CLAHE.
- **Dynamic Thresholding:** Uses Otsu’s method and adaptive thresholding to accurately determine mark levels.
- **Answer Detection:** Splits the processed image into individual answer regions (boxes) to detect filled bubbles.
- **Result Visualization:** Annotates the image with color-coded marks and generates a detailed report with visualisations.
- **User-Friendly Interface:** Built with Streamlit for rapid prototyping and deployment.

## Installation

### GitHub Installation (Using Virtual Environment with Python 3.11)

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Joyee2004/OMR-Scanner.git
   cd OMR-Scanner
   ```

2. **Create a Virtual Environment:**  
   (Ensure you have Python 3.11 installed.)

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
     
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

Your browser should open the Streamlit app at [http://localhost:8501](http://localhost:8501).

### Docker Installation

1. **Ensure You Have Docker Installed:**  
   Follow [Docker's official installation instructions](https://docs.docker.com/get-docker/).

2. **Build the Docker Image:**

   ```bash
   docker build -t omr-scanner .
   ```

3. **Run the Docker Container:**

   ```bash
   docker run -p 8501:8501 omr-scanner
   ```

4. **Access the Application:**  
   Open your browser and navigate to [http://localhost:8501](http://localhost:8501).

## Usage

- **Upload Your OMR Sheet:** Use the file uploader in the "Process OMR" tab.
- **Upload Answer Key:** Provide your answer key as a text file.
- **Configure the Marking Scheme and Layout:** Adjust the parameters for rows, columns, and scoring criteria.
- **Process and View Results:** After submission, an annotated image, report, and visualizations will be displayed.

## Deployment

The app is deployed on [Streamlit Community Cloud](https://share.streamlit.io). You can view the live application at:

[https://omr-analyzer.streamlit.app/](https://omr-analyzer.streamlit.app/)

## Methods Adopted

- **Image Preprocessing:**  
  The `preprocess` method (in `helper.py`) converts images to grayscale, applies median blur for noise reduction, uses fast non-local means denoising, and enhances contrast with CLAHE. These steps standardize the input for robust OMR extraction.

- **Adaptive Thresholding and Box Splitting:**  
  In `engine.py`, adaptive thresholding is applied to the preprocessed image to handle varying lighting conditions. The thresholded image is then split into multiple boxes (one for each answer option) using the `split_boxes` function, allowing for accurate detection of filled bubbles.

- **Dynamic Answer Detection:**  
  The `detect_marked_answers` method in the `OMRScanner` class uses a dynamically calculated threshold (via Otsu’s method) to determine if a bubble is filled. The method computes confidence scores based on the density of non-zero pixels within each box.

- **Result Annotation and Reporting:**  
  The final image is annotated to indicate correct, incorrect, or blank responses with color-coded indicators. Textual reports in both graphical HTML and plain text formats provide a detailed breakdown of the scanning results.

## License

This project is open source and available under the [MIT License](LICENSE).
