from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from conf import EMAIL, PASSWORD

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

 
s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(EMAIL, PASSWORD)

names, emails = get_contacts('contacts.txt')
message_template = read_template('email.txt')

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

for name, email in zip(names, emails):
    msg = MIMEMultipart()  

    message = message_template.substitute(PERSON_NAME=name.title())

    msg['From']=EMAIL
    msg['To']=email
    msg['Subject']="This is TEST"

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    
    del msg