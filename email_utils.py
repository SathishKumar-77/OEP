import smtplib

# Function to send emails
def send_email(subject, body, recipient_email, sender_email="onlineexamportal49@gmail.com", app_password="mfqd xgdy dplj alaw"):
    smtp_server = "smtp.gmail.com"
    port = 587  # For TLS

    try:
        # Establish connection to the SMTP server
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, app_password)  # Login with the sender's credentials

        # Compose the email
        message = f"Subject: {subject}\n\n{body}"

        # Send the email
        server.sendmail(sender_email, recipient_email, message)
        print("Email sent successfully!")
        return True  # Indicate success
    except Exception as e:
        print(f"Error while sending email: {e}")
        return False  # Indicate failure
    finally:
        server.quit()  # Close the connection


        
