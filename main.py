import cv2
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Function to capture video from webcam for 5 seconds and save as MP4
def capture_video(filename='doorbell_video.mp4', duration=5):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = time.time()

    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Function to send an email with the video attachment
def send_email_with_attachment(sender_email, receiver_email, password, subject, body, filename):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(filename)}')
            msg.attach(part)

        # Connect to the server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f'Email sent to {receiver_email} with video attachment.')

    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Main function to capture video and send it via email
def main():
    video_filename = 'doorbell_video.mp4'

    # Capture video for 5 seconds
    capture_video(video_filename, 5)

    # Email details
    sender_email = "piyushrajput285@gmail.com"
    receiver_email = "thesoupboyom@gmail.com"
    password = "mjxs fvnu ykeg sqtx"  # Use a more secure method for storing passwords
    subject = "Doorbell Camera Video"
    body = "Here is the recorded video from your doorbell camera."

    # Send the email with the video attachment
    send_email_with_attachment(sender_email, receiver_email, password, subject, body, video_filename)

if __name__ == "__main__":
    main()