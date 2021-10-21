from datetime import datetime
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Threshold to decide whether to send the email or not
EXTREME_FEAR_LEVEL = 25
FEAR_LEVEL = 45
GREED_LEVEL = 55
EXTREME_GREED_LEVEL = 75

# Suggestions depending on the index
suggestion = {'EXTREME FEAR': "sell your house and buy this shit, seriously",
              'FEAR': "start buying by bartering some of your possessions, not all of them",
              'GREED': "start selling, things are getting hot",
              'EXTREME GREED': "sell all your coins before this bubble pops and a stallion jams his dick in your ass"}


def retrieve_mail_bot_credentials():
    with open('mail bot credentials.txt', 'r') as c:
        return c.read().splitlines()


def retrieve_mailing_list():
    with open('mailing list.txt', 'r') as c:
        return c.read().splitlines()


def send_alert_mail(msg_body):
    credentials = retrieve_mail_bot_credentials()
    recipients = retrieve_mailing_list()

    msg = MIMEMultipart()

    msg['From'] = credentials[0]  # retrieve from mail bot credentials
    msg['To'] = msg['To'] = ", ".join(recipients)
    msg['Subject'] = 'Fear & Greed Index Alert'

    msg.attach(MIMEText(msg_body, 'html'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(credentials[0], credentials[1])
    server.send_message(msg)
    server.close()


try:
    # Get Fear & Greed Index (alternative.me API)
    API = "https://api.alternative.me/fng/"
    response = requests.get(API)
    # json response sample:
    # {'name': '', 'data': [{'value': '', 'value_classification': '', 'timestamp': '', 'time_until_update': ''}],
    # 'metadata': {'error': ''}}
    index = int(response.json()['data'][0]['value'])

    # Get BTC price (Coinbase API)
    API = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    response = requests.get(API)
    # json response sample:
    # {"data":{"base":"","currency":"","amount":""}}
    price = float(response.json()['data']['amount'])

    # Threshold evaluation and message construction
    level = ""
    if index < EXTREME_FEAR_LEVEL:
        level = 'EXTREME FEAR'
    elif index < FEAR_LEVEL:
        level = 'FEAR'
    elif index > EXTREME_GREED_LEVEL:
        level = 'EXTREME GREED'
    elif index > GREED_LEVEL:
        level = 'GREED'
    else:
        exit(0)  # Index is in neutral range, no email has to be sent

    # Building the message
    message = f"""<html><head></head><body>The Fear & Greed Index is <b>{index}</b>, corresponding to <b>{level}</b
    >.<br> The price of BTC is <b>${price}</b>.<br> 
    My suggestion is to {suggestion[level]}.</body></html><br><br>
    Yours faithfully,<br>
    FeaGA Bot"""

    # Sending emails...
    send_alert_mail(message)
except Exception as e:
    with open('errorLog.txt', 'a') as f:
        f.write(str(datetime.now()) + ': ' + str(e) + '\n')
    exit(-1)
