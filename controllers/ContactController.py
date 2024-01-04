import smtplib
from email.message import EmailMessage
from fastapi import HTTPException, status
import csv

def handleSendMail(data):
    print(data)
    email_address = "huyphan1232002@gmail.com"
    email_password = "aiftrjdztgmstvxs"
    msg = EmailMessage()
    msg['Subject'] = data.title
    msg['From'] = email_address
    msg['To'] = data.email
    msg.set_content(
       f"""\
    Name : {data.name}
    Email : {data.email}
    Message : {data.content}    
    """,
    )
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
    return {
        "success":True,
        "message":"Gửi liên hệ thành công !"
    }
