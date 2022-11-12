from django.http import JsonResponse
from django.shortcuts import render,redirect
from mailsender.models import User
from mailsender.models import History
from django.core.mail import EmailMessage
from coderz.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.template.loader import render_to_string,get_template
import uuid


class Message:
    def __init__(self,type,content):
        self.type=type
        self.content=content

    def getJson(self):
        return {
            'type':self.type,
            'content':self.content
        }

# Create your views here.
def home(request):

    return render(request,'mailsender_home.html')

def send(request):
    if request.method=='POST':
        data=request.POST
        files=request.FILES.getlist('attachments')
        user_code=User.objects.filter(code=data['secret-code'])
        if user_code.exists():
            
            trans_id=uuid.uuid4()
            user=User.objects.get(code=data['secret-code'])         
            history=History(uid=user.uid,transaction_id=trans_id)
            history.save()

            # content=render_to_string("email_format.html",
            #                 {'name':data['name'],'body':data['body']})
            content=get_template("email_format.html").render({'name':data['name'],'body':data['body']})
                            
            email=EmailMessage(
                    from_email="Coderzzone <{}>".format(EMAIL_HOST_USER),
                    to=[data['to-email']],
                    subject=data['subject'],
                    body=content,
                
                )
            email.content_subtype="html"
            for doc in files:
                email.attach(doc.name,doc.read(),doc.content_type)

            try:
                email.send()
                history.status=True
                history.save()
                message=Message("success","Mail has been sent to {} successfully with Transaction id: {}".format(data['to-email'],trans_id))
            
            except:
                
                email.to=[user.email]
                email.send()
                message=Message("warning",
                    "Failed to send the mail...")
        else:
            message=Message("warning","Sorry, your are not authorized to use this service")
        return JsonResponse(message.getJson())
    else:
        return redirect('mailsender:home')
