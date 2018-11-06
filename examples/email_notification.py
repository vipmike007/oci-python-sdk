import smtplib
from email.mime.text import MIMEText

class Email:
    def __init__(self):
        self.mailto_list=["mike.cao@oracle.com"]
        self.mail_host="smtp.126.com"
        self.mail_user="vipmike007"
        self.sender = "Mike Cao"
        self.mail_pass="oracleS1"
        self.mail_postfix="126.com"
######################
    def send_mail(self,sub,content):
        '''
        to_list:
        sub:
        content:
        send_mail("aaa@126.com","sub","content")
        '''
        to_list = self.mailto_list
        me=self.sender+"<"+self.mail_user+"@"+self.mail_postfix+">"
        msg = MIMEText(content)
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            s = smtplib.SMTP()
            s.connect(self.mail_host)
            s.login(self.mail_user,self.mail_pass)
            s.sendmail(me, to_list, msg.as_string())
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False
def test():    
    emailclient = Email()
    if emailclient.send_mail("subject","content"):
        print "send succcessfully"
    else:
        print "send failed"
if __name__ == '__main__':
    test()
