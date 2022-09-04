from django.shortcuts import render,redirect
from mailsender.models import User
from mailsender.threading import SendMail
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
            SendMail(args=(data,files,trans_id)).start()
            context['success_message']="Mail has been sent to {} successfully with Transaction id: {}".format(data['to-email'],trans_id)
        else:
            context['error_message']="Sorry, your are not authorized to use this service"
    
    return render(request,'mailsender_home.html',context)

