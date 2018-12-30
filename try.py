import smtplib

def send_email(subject, msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login('viral.cloudvm@gmail.com','Vikeee@!')
    message = 'Subject: {}\n\n{}'.format(subject,msg)
    server.sendmail('viral.cloudvm@gmail.com','viral.sangani2011@gmail.com',message)
    server.quit()
    print("Done")

send_email('`1st mail','SEND')
