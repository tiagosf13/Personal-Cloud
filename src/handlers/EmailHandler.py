import smtplib, configparser
from pathlib import Path
from handlers.DatabaseHandler import get_current_dir
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to, subject, body):
    
    # Read the configuration file
    config_file = Path(get_current_dir(subdirectory="../credentials/conf.ini"))
    assert config_file.exists(), "conf.ini file not found"

    config = configparser.ConfigParser()
    config.read(config_file)

    # Create a MIMEText object to represent the email body
    msg = MIMEMultipart()
    msg['From'] = config["email"]["email"]
    msg['To'] = to
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server
    server = smtplib.SMTP_SSL(config["email"]["server"], 465)  # Replace with your email provider's SMTP server

    try:
        # Login to your email account
        server.login(config["email"]["email"], config["email"]["password"])

        # Send the email
        server.sendmail(config["email"]["email"], to, msg.as_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()

    # Return True to indicate the email was sent successfully
    return True