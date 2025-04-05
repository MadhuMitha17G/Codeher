import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

def mail_credentials(text, no, image_path):
    # Email details
    sender_email = "creativebean21@gmail.com"  # Replace with your Gmail
    sender_password = "gwpy labk byhy sjyv"  # Replace with your Gmail App Password
    receiver_email = "swethamangai.r@gmail.com"  # Replace with recipient's email
    subject = "Abusive Message Report - Reg"

    # Plain text version of the email body
    plain_body = f"""
Dear Recipient,

We are writing to report an incident of cyberbullying that has been detected. Below are the details:

Extracted Text from Screenshot:
"""
    if text:
        plain_body += "\n".join(text.splitlines())  # Join lines with newline
    else:
        plain_body += "Couldn't extract text"

    plain_body += f"""


Phone Number Detected:
{no if no else "Not found"}

The screenshot is attached for your reference.

Please review the content and take appropriate action to address this matter.

Sincerely,
Cyberbullying Detection Team
"""

    # HTML version of the email body with a neat, professional template and inline image
    
    html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8d7da; padding: 10px; border-radius: 5px; text-align: center; }}
        .content {{ margin-top: 20px; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #777; text-align: center; }}
        .highlight {{ font-weight: bold; color: #d9534f; }}
        img {{ max-width: 100%; height: auto; margin-top: 10px; border: 1px solid #ccc; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Cyberbullying Incident Report</h2>
        </div>
        <div class="content">
            <p>Dear Recipient,</p>
            <p>We are writing to report an incident of cyberbullying that has been detected. Below are the details:</p>
            <p><strong>Extracted Text from Screenshot:</strong></p>
            <blockquote style="background-color: #f9f9f9; padding: 10px; border-left: 4px solid #ccc;">
                {text}
            </blockquote>
            <p><strong>Phone Number Detected:</strong></p>
            <p class="highlight">{no if no else "Not found"}</p>
            <p><strong>Screenshot:</strong></p>
            <img src={image_path} alt="Attached Screenshot">
            <p>Please review the content and take appropriate action to address this matter.</p>
        </div>
        <div class="footer">
            <p>Sincerely,<br>Cyberbullying Detection Team</p>
        </div>
    </div>
</body>
</html>
"""

    # Create the email message with both plain text and HTML versions
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach plain text and HTML versions
    msg.attach(MIMEText(plain_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    # Attach the image file and link it with a Content-ID
    try:
        with open(image_path, 'rb') as img_file:
            mime_image = MIMEImage(img_file.read())
            mime_image.add_header('Content-ID', '<screenshot>')
            mime_image.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
            msg.attach(mime_image)
    except FileNotFoundError:
        print(f"Warning: Image file {image_path} not found. Sending email without attachment.")

    # Connect to Gmail's SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server and port
        server.starttls()  # Enable TLS (security)
        server.login(sender_email, sender_password)  # Login to your email

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server.quit()  # Close the connection

# Example usage (for testing)
if __name__ == "__main__":
    sample_text = "This is a sample abusive message extracted from a screenshot."
    sample_no = "12345 67890"  # Example phone number
    mail_credentials(sample_text, sample_no, 'ss3.jpeg')