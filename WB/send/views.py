from django.shortcuts import render,redirect,HttpResponse
from time import sleep
from .forms import Option,Add_number,Add_csv,Add_Attachment
from .saved_contacts import send_to_saved
from .unsaved_contacts import whatsapp_login,send_to_unsaved,quits,send_attachment_to_unsavaed
import csv
from .models import Whatsapp_Numbers,Read_csv,Attachment
import os
from pathlib import Path
from django.contrib import messages
# Create your views here.

def welcome_view(request):
    whatsapp_login()
    return render(request,r"send\welcome.html")

def list_phone_number_view(request):
    obj=Whatsapp_Numbers.objects.all()
    return render(request,r"send\phone_numbers.html",{"numbers":obj})

def number_delete_view(request,id):
    obj=Whatsapp_Numbers.objects.get(pk=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('phone_number')
    context = {
        'number': obj
    }
    return render(request,'send/number_delete.html',context)

def send_view(request):
    if request.method=="POST":
        etext=Option(request.POST)
        text=request.POST.get("text")
        lst=Whatsapp_Numbers.objects.filter(user="sib").values_list("number")
        numbers=[]
        for number in lst:
            number=str(number)
            a=number[3:15]
            numbers.append(a)
        for number in numbers:
            send_to_unsaved(number,text,1)
            sleep(1)
        messages.success(request,"All messages sent.")
        return redirect("send")
    else:
        send=Option
        return render(request,r"send\send_message.html",{"form":send})

def send_attachment_view(request):
    if request.method=="POST":
        obj = Add_Attachment(request.POST,request.FILES)
        if obj.is_valid(): 
            obj.save()
            name=request.FILES['File']
            dir=Path(__file__).resolve().parent.parent
            address=f"{dir}\media\Attachments\{name}"
            lst=Whatsapp_Numbers.objects.filter(user="sib").values_list("number")
            numbers=[]
            for number in lst:
                number=str(number)
                a=number[3:15]
                numbers.append(a)
            for number in numbers:
                send_attachment_to_unsavaed(number,address)
                sleep(1)
            messages.success(request,"All attachment sent.")
            os.remove(address)
            return redirect("attachment")
        else:
            print("error")
            return redirect("attachment")
    else:
        attach=Add_Attachment
        return render(request,r"send\send_attachment.html",{"form":attach})

def add_one_view(request):
    if request.method == "POST":
        number=request.POST.get("Phone_No")
        auth="sib"
        if int(number[3])>5:
            new_entry=Whatsapp_Numbers(number=number,user=auth)
            new_entry.save()
            return redirect("send")
        else:
            messages.error(request,"invalid number")
            return redirect("one")
    else:
        num_form=Add_number
        return render(request , r"send\add_one.html" , {"form":num_form})

def add_csv_view(request):
    if request.method == "POST":
        ext = os.path.splitext(str(request.FILES['File']))[1]
        if ext != ".csv":
            messages.error(request,"Not a csv file.")
            print("error")
            return redirect("csv")
        else:
            obj = Add_csv(request.POST,request.FILES)
            print(obj.is_valid)
            if obj.is_valid(): 
                obj.save()
                name=request.FILES['File']
                address=f"media\Csv_file\{name}"
                lst,count=read_file(address)
                for number in lst:
                    whats_obj=Whatsapp_Numbers(number=number,user="sib")
                    whats_obj.save()
                os.remove(address)

                if count != 0:
                    messages.warning(request,"There are some invalid numbers.")
                return redirect("csv")
            else:
                messages.error(request,"Invalid File")
                return redirect("csv")
    else:
        csv_form=Add_csv
        return render(request,r"send\add_csv.html",{"form":csv_form})



def read_file(csv_f):
    with open(csv_f) as file:
        numbers = csv.reader(file)
        country_code="+91"
        next(numbers)
        lst=[]
        count=0
        for number in numbers:
            number=str(number)
            if len(number) == 14 and int(number[2])>5:
                a=country_code+str(number[2:12])
                lst.append(a)
            else:
                count=count+1
        return lst,count