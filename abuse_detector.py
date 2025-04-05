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
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image at {image_path}")
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_image)
        if not text.strip():  # Check if extracted text is empty or just whitespace
            return None
        return text
    except Exception as e:
        print(f"Error during text extraction: {e}")
        return None

def is_text_abusive(text):
    if text is None:
        return False  # Cannot classify if no text
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

def main(image_path):
    try:
        text = extract_text_from_image(image_path)
        if text is None:
            print("Couldn't extract text from the image (possibly blurry or empty).")
            return "Couldn't extract text from the image (possibly blurry or empty)."

        no = extract_ten_digit_number(text)
        print("Extracted Text:", text)
        if is_text_abusive(text):
            print("Result: This screenshot contains abusive content.")
            print(f"Phone Number: {no if no else 'Not detected'}")
            mail_credentials(text, no, image_path)  # Pass image_path to email function
            return "Abusive content detected"
        else:
            print("Result: No abusive content detected.")
            return "No abusive content detected"
    except Exception as e:
        print(f"Error in main function: {e}")
        return f"Error processing image: {e}"
    try:
        text = extract_text_from_image(image_path)
        no = extract_ten_digit_number(text)
        print("Extracted Text:", text)
        if is_text_abusive(text):
            print("Result: This screenshot contains abusive content.")
            print(f"Phone Number: {no if no else 'Not detected'}")
            mail_credentials(text, no, image_path)  # Pass image_path to email function
            return "Abusive content detected. This report will be sent for review."
        else:
            print("Result: No abusive content detected.")
            return "No strong indicators of abuse were found in the text."
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example for standalone testing:
    # main("test_screenshot.png")
    non_abusive_text = "This is a friendly message."
    is_abusive = is_text_abusive(non_abusive_text)
    print(f"'{non_abusive_text}' is abusive: {is_abusive}")