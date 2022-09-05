from django.shortcuts import render,redirect
from mailsender.models import User
from mailsender.threading import SendMail
from mailsender.models import History
from django.core.mail import EmailMessage
from coderz.settings import EMAIL_HOST_USER
import uuid

# Create your views here.
def home(request):
    context={}
    if request.method=='POST':
        # print(request.POST)
        data=request.POST
        files=request.FILES.getlist('attachments')
        # print(files)

        user_code=User.objects.filter(code=data['secret-code'])
        
        if user_code.exists():
            trans_id=uuid.uuid4()
            # SendMail(args=(data,files,trans_id)).start()
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
            
            context['success_message']="Mail has been sent to {} successfully with Transaction id: {}".format(data['to-email'],trans_id)
        else:
            context['error_message']="Sorry, your are not authorized to use this service"
    
    return render(request,'mailsender_home.html',context)

