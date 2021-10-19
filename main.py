import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Threshold to decide whether to send the email or not
EXTREME_FEAR_LEVEL = 25
FEAR_LEVEL = 45
GREED_LEVEL = 55
EXTREME_GREED_LEVEL = 75


def retrieve_mail_bot_credentials():
    bot_email = ""
    bot_password = ""
    return [bot_email, bot_password]


def retrieve_mailing_list():
    recipients = ["", ""]
    return recipients


def send_alert_mail(msg_body):
    credentials = retrieve_mail_bot_credentials()
    recipients = retrieve_mailing_list()

    msg = MIMEMultipart()

    msg['From'] = ""  # retrieve from mail bot credentials
    msg['To'] = msg['To'] = ", ".join(recipients)
    msg['Subject'] = 'Fear & Greed Index Alert'

    msg.attach(MIMEText(msg_body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(credentials[0], credentials[1])
    server.send_message(msg)
    server.close()


try:
    # API Call (alternative.me)
    API = "https://api.alternative.me/fng/"
    response = requests.get(API)
    # json response sample:
    # {'name': '', 'data': [{'value': '', 'value_classification': '', 'timestamp': '', 'time_until_update': ''}],
    # 'metadata': {'error': ''}}
    index = response.json()['data'][0]['value']

    # Get BTC price (Coinbase)
    API = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    response = requests.get(API)
    # json response sample:
    # {"data":{"base":"","currency":"","amount":""}}
    price = response.json()['data']['amount']
except Exception as e:
    with open('errorLog.txt', 'a') as f:
        f.write(e + '\n')
    exit(-1)
exit(0)
# Threshold evaluation and message construction
message = ""  # TODO
if index < EXTREME_FEAR_LEVEL:
    send_alert_mail(index)
elif index < FEAR_LEVEL:
    send_alert_mail(index)
elif index > EXTREME_GREED_LEVEL:
    send_alert_mail(index)
elif index > GREED_LEVEL:
    send_alert_mail(index)
else:
    exit(0)  # Index is in neutral range, no email has to be sent

# Sending emails...
send_alert_mail(message)
