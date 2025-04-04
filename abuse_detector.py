import cv2
import pytesseract
import joblib
import re
from send_email import mail_credentials

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the trained model and vectorizer
model = joblib.load('abuse_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image at {image_path}")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    return text

def is_text_abusive(text):
    text_counts = vectorizer.transform([text])
    prediction = model.predict(text_counts)
    return prediction[0] in [0, 1]

def extract_ten_digit_number(s):
    """
    Extracts the first standalone 10-digit number from a string (5 digits, space, 5 digits).
    
    Args:
        s (str): The input string to search.
    
    Returns:
        str: The first 10-digit number found, or None if no match exists.
    """
    pattern = r"\b\d{5} \d{5}\b"
    match = re.search(pattern, s)
    return match.group() if match else None

def main():
    image_path = 'ss3.jpeg'  # Update to your file
    try:
        text = extract_text_from_image(image_path)
        no = extract_ten_digit_number(text)
        print("Extracted Text:", text)
        if is_text_abusive(text):
            print("Result: This screenshot contains abusive content.")
            print(f"Phone Number: {no if no else 'Not detected'}")
            mail_credentials(text, no, image_path)  # Pass image_path to email function
        else:
            print("Result: No abusive content detected.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()