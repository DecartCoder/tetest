import smtplib
import email.message

def send_email(text):
    msg = email.message.Message()
    msg['Subject'] = 'New Order'
    msg['From'] = 'zakazfullpull@gmail.com'
    msg['To'] = 'fullandpull2020@gmail.com'
    password = "zakazfullpull123"
    msg.add_header('Content-Type', 'text/plain')
    msg.set_payload(str(text).replace('*', ''))
    #Server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))