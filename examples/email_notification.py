import smtplib
import oci
from email.mime.text import MIMEText

class Email:
    def __init__(self):
        self.mailto_list=["mike.cao@oracle.com"]
        #self.mail_host="smtp.126.com"
        self.mail_host="smtp.gmail.com"
        self.mail_user="vipmike007@gmail.com"
        self.sender = "Mike Cao"
        config = oci.config.from_file()
        self.mail_pass = config["email_password"]
        self.mail_postfix="gmail.com.com"
        self.mailcc_list=[]
######################
    def send_mail(self,sub,content):
        '''
        to_list:
        sub:
        content:
        send_mail("aaa@gmail.com","sub","content")
        '''
        to_list = self.mailto_list
        cc_list = self.mailcc_list
        me = "Mike Cao <mike.cao@oracle.com>"
        msg = MIMEText(content)
        msg['Subject'] = sub
        msg['From'] = me
        if len(to_list) !=0 :
            msg['To'] = ";".join(to_list)
        if len(cc_list) !=0:
            msg['Cc'] = ";".join(cc_list)
        try:
            s = smtplib.SMTP("smtp.gmail.com", 587)
            #s.set_debuglevel(1)
            s.ehlo()
            s.starttls()
            #s.connect(self.mail_host)
            s.login(self.mail_user,self.mail_pass)
            s.sendmail(me, to_list, msg.as_string())
            #s.sendmail(me, msg.as_string())
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
