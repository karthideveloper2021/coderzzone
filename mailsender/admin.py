from django.contrib import admin
from mailsender.models import User,History

# Register your models here.

class UserModelView(admin.ModelAdmin):
    list_display=('uid','name',)

class HistoryModelView(admin.ModelAdmin):
    titles=('uid','transaction_id','status','activity')
    list_display=titles[:1]+titles[2:]
    readonly_fields=titles

admin.site.register(User,UserModelView)
admin.site.register(History,HistoryModelView)