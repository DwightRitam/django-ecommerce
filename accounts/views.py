from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.http import HttpResponseRedirect
from accounts.models import Profile

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required




def send_email(request,user_email,first_name):
    
    subject = 'Welcome to Filmotrend, where fashion trends are always in style.'
    message = f'Hi {first_name}, Find your new favorite fashion trends at Filmotrend. See the pdf for more information about us'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
     # Attach a file to the email
    file_path = f"{settings.BASE_DIR}/filmy.pdf"
    
    # print("email has been sent")


    email = EmailMessage(subject, message, email_from, recipient_list)
    
    email.attach_file(file_path)
    
    email.send()
    

    return redirect('/')



def login_page(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user_obj=User.objects.filter(username=email)
        
        if not user_obj.exists():
            messages.error(request,'Invalid Username')
            return redirect('/login')
        
        if not user_obj[0].profile.is_email_verified:
            messages.error(request,'Account not verified')
            return redirect('/login')
            
        
        user=authenticate(username=email, password=password)
        
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login')
        
        else:
            login(request,user)
            return redirect('/')
    return render(request, 'login.html')

def signin_page(request):
    flag=False
    if request.method == 'POST':
       
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        
        if user_obj.exists() and flag==False:
            messages.warning(request, "Email already exists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()
        # messages.warning(request, "A OTP has been sent to your email address")
        flag=True
        print(user_obj.profile.email_token)
        return redirect(f'email_verification/{user_obj.profile.email_token}')
        
    # if request.user.is_authenticated:
    #     # return redirect('/'
    #     print(request.user)
    # else:
    return render(request, 'sign.html')

def logout_page(request):
    logout(request)
    return redirect('/')   


def email_verification(request,email_token):
    user = Profile.objects.get(email_token= email_token)
    # print(user.user)
    curr_user=user.user
    # print(curr_user.first_name)
    # print(type(curr_user))
    if request.method == 'POST':
         email_Otp=request.POST.get('email_Otp')  
        #  print(email_Otp)
         if(user.email_Otp==email_Otp):
              user.is_email_verified = True
              user.save()
              send_email(request,curr_user.username,curr_user.first_name)
              login(request,curr_user)
              return redirect('/')
         else:
            messages.error(request,'Invalid Otp')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context={
        "curr_user":curr_user
    }
    return render(request, 'email_verification.html',context)    
                 
             
         
    
