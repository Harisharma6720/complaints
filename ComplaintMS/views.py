from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
import reportlab
from .utils import send_status_change_notification
from django.db.models import Count, Q
from .models import Profile,Complaint

from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
##from .forms import UserRegisterForm,ProfileUpdateForm,UserProfileform,ComplaintForm,UserProfileUpdateform,statusupdate
from .utils import send_complaint_notification

from .forms import UserRegisterForm, ProfileUpdateForm, UserProfileForm, ComplaintForm, UserProfileUpdateForm, StatusUpdateForm




""""from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ComplaintForm
from .models import Complaint"""
from django.shortcuts import render
def login_view(request):
    return render(request, 'signinpublic')

def login_view(request):
    return render(request, 'signinstaff')

def signin_public(request):
    # view logic here
    return render(request, 'signinpublic.html')

def signin_staff(request):
    # view logic here
    return render(request, 'signinstaff.html')


"""def add_complaint(request):
    #...
    return render(request, 'complaints/add_complaint.html')






def add_complaint(request):
    if request.user.is_authenticated:
        return redirect('complaint_form')
    else:
        return redirect('login')

@login_required
def complaint_form(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'complaint_form.html', {'form': form})"""




from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from datetime import datetime




def login_redirect(request):
    # Your view function code here
    print("I have come here in the code.")
    print("this is the staff user login",request.user.profile.type_user)
    # return redirect('counter')
    if request.user.profile.type_user=='staff':
        print("this is the user type",request.user.profile.type_user)
        return redirect('counter')
    else:
        return redirect('dashboard')
   
def signinstaff_redirect(request):
    # Your view function code here
    print("I have come here in the code.")
    # return redirect('dashboard')
    return redirect('counter')
    
   
#page loading.
def index(request):
    return render(request,"ComplaintMS/home.html")

def aboutus(request):
    return render(request,"ComplaintMS/aboutus.html")

def signinpublic(request):
    return render(request,"ComplaintMS/signinpublic.html")

def signinstaff(request):
    return render(request,"ComplaintMS/signinstaff.html")

def loginpublic(request):
    return render(request,"ComplaintMS/loginpublic.html")

def loginstaff(request):
    return render(request,"ComplaintMS/loginstaff.html")

def login(request):
    return render(request,"ComplaintMS/login.html")

def signin(request):
    return render(request,"ComplaintMS/signin.html")

#get the count of all the submitted complaints,solved,unsolved.
def counter(request):
        total=Complaint.objects.all().count()
        unsolved=Complaint.objects.all().exclude(status='1').count()
        solved=Complaint.objects.all().exclude(Q(status='3') | Q(status='2')).count()
        dataset=Complaint.objects.values('Type_of_complaint').annotate(total=Count('status'),solved=Count('status', filter=Q(status='1')),
                  notsolved=Count('status', filter=Q(status='3')),inprogress=Count('status',filter=Q(status='2'))).order_by('Type_of_complaint')
        args={'total':total,'unsolved':unsolved,'solved':solved,'dataset':dataset,}
        return render(request,"ComplaintMS/counter.html",args)

#changepassword for grievancemember.
def change_password_g(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request,messages.SUCCESS, f'Your password was successfully updated!')
            return redirect('change_password_g')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComplaintMS/change_password_g.html', {
        'form': form
    })
    return render(request,"ComplaintMS/change_password_g.html")
#registration page.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form=UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid() :
            
            new_user=form.save()
            profile=profile_form.save(commit=False)
            if profile.user_id is None:
                profile.user_id=new_user.id
            profile.save()
            messages.add_message(request,messages.SUCCESS, f' Registered Successfully ')
            return redirect('/signinpublic/')
    else:
        form = UserRegisterForm()
        profile_form=UserProfileForm()

    context={'form': form,'profile_form':profile_form }
    return render(request, 'ComplaintMS/signinpublic.html',context )



"""def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            address = form.cleaned_data.get('address')
            Profile.objects.create(user=user, address=address)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})"""



#login based on user.
def loginpublic_redirect(request):
    if request.user.profile.type_user=='user':
        print("this is the user type",request.user.profile.type_user)
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/counter/')
    
@login_required
def dashboard(request):

 if request.user.profile.type_user=='public':
    if request.method == 'POST':
        p_form=ProfileUpdateForm(request.POST,instance=request.user)
        profile_update_form=UserProfileUpdateForm(request.POST,instance=request.user.profile)
        if p_form.is_valid() and profile_update_form.is_valid():
                user=p_form.save()
                profile=profile_update_form.save(commit=False)
                profile.user=user
                profile.save()
                messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
                return render(request,'ComplaintMS/dashboard.html',)
    else:
        p_form=ProfileUpdateForm(instance=request.user)
        profile_update_form=UserProfileUpdateForm(instance=request.user.profile)
    context={
        'p_form':p_form,
        'profile_update_form':profile_update_form
        }
    return render(request, 'ComplaintMS/dashboard.html',context)
 
#change password for user.

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request,messages.SUCCESS, f'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComplaintMS/change_password.html', {
        'form': form
    })


#complaints handling and submission section.
@login_required
def complaints(request):
  
    if request.method == 'POST':
           
        
        complaint_form=ComplaintForm(request.POST, request.FILES)
        if complaint_form.is_valid():
                    
               instance=complaint_form.save(commit=False)
               instance.user=request.user
               
        #        mail=request.user.email
        #        print(mail)
        #        send_mail('Hi Complaint has been Received', 'Thank you for letting us know of your concern, Have a Cookie while we explore into this matter.  Dont Reply to this mail', 'testerpython13@gmail.com', [mail],fail_silently=False)
               
               instance.save()
               send_complaint_notification(instance)               
               messages.add_message(request,messages.SUCCESS, f'Your complaint has been registered!')
               return render(request,'ComplaintMS/comptotal.html',)
        else:
                messages.add_message(request, messages.ERROR, 'Please correct the errors below.')

    else:
        
        complaint_form=ComplaintForm(request.POST)
    context={'complaint_form':complaint_form,}
    return render(request,'ComplaintMS/comptotal.html',context)
        

@login_required
def list(request):
    c = Complaint.objects.filter(user=request.user).exclude(status='1')
    result = Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    
    # Pagination for 'c'
    paginator_c = Paginator(c, 10)  # Show 10 complaints per page
    page_number_c = request.GET.get('page_c')
    page_obj_c = paginator_c.get_page(page_number_c)

    # Pagination for 'result'
    paginator_result = Paginator(result, 10)  # Show 10 complaints per page
    page_number_result = request.GET.get('page_result')
    page_obj_result = paginator_result.get_page(page_number_result)
    
    args = {
        'page_obj_c': page_obj_c,
        'page_obj_result': page_obj_result,
    }
    return render(request, 'ComplaintMS/Complaints.html', args)

@login_required
def slist(request):
    result=Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    #c=Complaint.objects.all()
    args={'result':result}
    return render(request,'ComplaintMS/solvedcomplaint.html',args)

@login_required
def allcomplaints(request):
      
        
        c=Complaint.objects.all().exclude(status='1')
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_complaint__icontains=drop))
        if comp:
                c=c.filter(Q(Type_of_complaint__icontains=comp)|Q(Description__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                uid=request.POST.get('uid')
                print(uid)
                project = Complaint.objects.get(id=cid)
                
                forms=StatusUpdateForm(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        mail = User.objects.filter(id=uid)
                        for i in mail:
                                m=i.email
                       
                
                        print(m)
                        # send_mail('Hi, Complaint has been Resolved ', 'Thanks for letting us know of your concern, Hope we have solved your issue. Dont Reply to this mail', 'testerpython13@gmail.com', [m],fail_silently=False)
                        obj.save()
                        send_status_change_notification(obj)
                        messages.add_message(request,messages.SUCCESS, f'The complaint has been updated!')
                        return HttpResponseRedirect(reverse('allcomplaints'))
                else:
                        return render(request,'ComplaintMS/AllComplaints.html')
                 #testing

        else:
                forms=StatusUpdateForm()
        #c=Complaint.objects.all().exclude(status='1')
           
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'ComplaintMS/allcomplaints.html',args)

@login_required
def solved(request):
        
        cid=request.POST.get('cid2')
        c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_complaint__icontains=drop))
        if comp:
               
                c=c.filter(Q(Type_of_complaint__icontains=comp)|Q(Description__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                print(cid)
                project = Complaint.objects.get(id=cid)
                forms=StatusUpdateForm(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        obj.save()
                        send_status_change_notification(obj)
                        messages.add_message(request,messages.SUCCESS, f'The complaint has been updated!')
                        return HttpResponseRedirect(reverse('solved'))
                else:
                        return render(request,'ComplaintMS/solved.html')
                 #testing
        else:
                forms=StatusUpdateForm()
        #c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'ComplaintMS/solved.html',args)

#allcomplaints pdf viewer.
def pdf_viewer(request):
    detail_string={}
    #detailname={}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Complaint_id.pdf'
    p = canvas.Canvas(response,pagesize=A4)
    
    cid=request.POST.get('cid')
    uid=request.POST.get('uid')
    
    details = Complaint.objects.filter(id=cid).values('Description')
    name = Complaint.objects.filter(id=cid).values('user_id')
    '''Branch = Complaint.objects.filter(id=cid).values('Branch')'''
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_complaint')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')
    #date_format1 = "%Y-%m-%d %H:%M:%S.%f%z"
   
    
    for val in details:
            detail_string=("{}".format(val['Description']))
    for val in name:
           detailname=("User: {}".format(val['user_id']))
    '''for val in Branch:
            detailbranch=("Branch: {}".format(val['Branch']))'''
    for val in Subject:
            detailsubject=("Subject: {}".format(val['Subject']))
    for val in Type:
            detailtype=("{}".format(val['Type_of_complaint']))
            
    for val in Issuedate:
            ptime=("{}".format(val['Time']))
            detailtime=("Time of Issue/ Time of Solved: {}".format(val['Time']))
    #detail_string = u", ".join(("Desc={}".format(val['Description'])) for val in details) 
    date_format = "%Y-%m-%d"
    a = datetime.strptime(str(datetime.now().date()), date_format)
    b = datetime.strptime(str(ptime), date_format)
    delta = a - b
    print(b)
    print(a)
    print (delta.days )       
    if detailtype=='1':
            detailtype="Type of Complaint: Fire"
    if detailtype=='3':
            detailtype="Type of Complaint: Road"
    if detailtype=='2':
            detailtype="Type of Complaint: Garbage"
    if detailtype=='4':
            detailtype="Type of Complaint: Transportation"
    if detailtype=='5':
            detailtype="Type of Complaint: Other"

    p.drawString(25, 770,"Report:")
    p.drawString(30, 750,detailname)
    ''' p.drawString(30, 730,detailbranch)'''
    p.drawString(30, 710,detailtype)
    p.drawString(30, 690,detailtime)
    p.drawString(30, 670,detailsubject)
    p.drawString(30, 650,"Description:")
    p.drawString(30, 630,detail_string)

    p.showPage()
    p.save()
    return response

#complaints pdf view.
@login_required
def pdf_view(request):
    detail_string={}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=complaint_id.pdf'
    
    p = canvas.Canvas(response,pagesize=A4)
    cid=request.POST.get('cid')
    #print(cid)
    details = Complaint.objects.filter(id=cid).values('Description')
    name = User.objects.filter(username=request.user.username).values('username')
    #Branch = Complaint.objects.filter(id=cid).values('Branch')
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_complaint')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')


    for val in details:
            detail_string=("{}".format(val['Description']))
    for val in name:
            detailname=("User: {}".format(val['username']))
    ##for val in Branch:
      ##      detailbranch=("Branch: {}".format(val['Branch']))
    for val in Subject:
            detailsubject=("Subject: {}".format(val['Subject']))
    for val in Type:
            detailtype=("{}".format(val['Type_of_complaint']))
            
    for val in Issuedate:
            detailtime=("Time of Issue: {}".format(val['Time']))
    detail_string = u", ".join(("Desc={}".format(val['Description'])) for val in details) 

    if detailtype=='1':
            detailtype="Type of Complaint: Fire"
    if detailtype=='3':
            detailtype="Type of Complaint: Road"
    if detailtype=='2':
            detailtype="Type of Complaint: Garbage"
    if detailtype=='4':
            detailtype="Type of Complaint: Transportation"
    if detailtype=='5':
            detailtype="Type of Complaint: Other"

    p.drawString(25, 770,"Report:")
    p.drawString(30, 750,detailname)
    #p.drawString(30, 730,detailbranch)
    p.drawString(30, 710,detailtype)
    p.drawString(30, 690,detailtime)
    p.drawString(30, 670,detailsubject)
    p.drawString(30, 650,"Description:")
    p.drawString(30, 630,detail_string)

    p.showPage()
    p.save()
    return response
'''
def complaint_details(request):
    complaint_id = request.GET.get('id')
    complaint = get_object_or_404(Complaint, id=complaint_id)
    data = {
        'user': complaint.user.username,
        'subject': complaint.Subject,
        'type': complaint.get_Type_of_complaint }
    

    
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ComplaintForm
from .models import Complaint

def send_complaint_registered_email(staff_email, staff_name, user_name, complaint_details):

    subject = 'New Complaint Registered'
    message = render_to_string('emails/complaint_registered.html', {
        'staff_name': staff_name,
        'user_name': user_name,
        'complaint_details': complaint_details,
    })
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [staff_email], html_message=message)
def register_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            
            # Send email notification to staff
            staff_email = 'harisharma00456@gmail.com'  # Replace with actual staff email
            staff_name = 't'  # Replace with actual staff name
            user_name = request.user.username
            complaint_details = complaint.description  # Adjust as needed
            
            send_complaint_registered_email(staff_email, staff_name, user_name, complaint_details)
            
            return redirect('complaint_success')  # Redirect to a success page
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/register_complaint.html', {'form': form})

# views.py

def send_complaint_updated_email(user_email, user_name, complaint_details):
    subject = 'Complaint Updated'
    message = render_to_string('emails/complaint_updated.html', {
        'user_name': user_name,
        'complaint_details': complaint_details,
    })
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email], html_message=message)

def update_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            
            # Send email notification to public user
            user_email = complaint.user.email
            user_name = complaint.user.username
            complaint_details = complaint.description  # Adjust as needed
            
            send_complaint_updated_email(user_email, user_name, complaint_details)
            
            return redirect('complaint_detail', complaint_id=complaint.id)  # Redirect to the complaint detail page
    else:
        form = ComplaintForm(instance=complaint)
    
    return render(request, 'complaints/update_complaint.html', {'form': form})
'''


def some_view_function(request):
    from .forms import UserProfileform
    # ...
    # Your view code here
    # ...

             

