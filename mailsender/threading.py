import threading
from django.core.mail import EmailMessage
from coderz.settings import EMAIL_HOST_USER
from mailsender.models import History,User

class SendMail(threading.Thread):
    def __init__(self,args):
        super().__init__(target=self.send,args=args)
    
    def send(self,data,files,trans_id):
        # print("working",data)
        user=User.objects.get(code=data['secret-code'])         
        history=History(uid=user.uid,transaction_id=trans_id)
        history.save()

        email=EmailMessage(
                from_email=EMAIL_HOST_USER,
                to=[data['to-email']],
                subject=data['subject'],
                body=data['body'],
            )
        for doc in files:
            email.attach(doc.name,doc.read(),doc.content_type)

        try:
            email.send()
            history.status=True
            history.save()
        
        except:
            email.to=[user.email]
            email.send()

        # print("mail send..")
