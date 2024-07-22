from django.contrib import admin
from .models import Profile,Complaint

class CAdmin(admin.ModelAdmin):
    list_display = ('user','Subject','Type_of_complaint','Description','Time','status','longitude','latitude','image')

admin.site.register(Profile)
admin.site.register(Complaint,CAdmin)
#admin.site.register(Grievance)


