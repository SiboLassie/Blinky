import datetime
import smtplib
import time
import sys
import os

#### 2  Everyone can see what's happening ####

emailList = ["alexabo4@ac.sce.ac.il"]
def send_Mails(emailList,time1):
    for mail in emailList:
        if '@' not in mail:
            return False
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("blinkysendmsg@gmail.com", "sukablyat123")

        message = 'Subject: {}\n\n{}'.format('new code commit! at', time1)
        s.sendmail("blinkysendmsg@gmail.com", mail1, message)
        s.quit()

send_Mails(emailList,time1)