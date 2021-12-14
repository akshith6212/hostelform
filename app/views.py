from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from accounts.models import Registerbook
from django.http import HttpResponse
from datetime import datetime
import pytz
import csv

# Create your views here.
def index(request):
  if request.user.is_superuser:
    return redirect('admin_view/')
  
  if(request.method == 'POST'):
    reason = request.POST['reason']
    print("reason is: ", reason)
    username = request.user.username
    user = User.objects.get(username=username)
    flag = user.student.flag
    if(flag == False):
      tz = pytz.timezone('Asia/Kolkata') 
      datetime_local = datetime.now(tz)
      d = Registerbook(exit_time = datetime_local, enter_time = datetime_local, user = user.student, reason = reason)
      d.save()
      return redirect('exit/')
    else:
      return redirect('exit/')
  else:
    try:
      username = request.user.username
      user = User.objects.get(username=username)
      if user is not None:
        print('Flag value is:' ,user.student.flag)
    except:
      pass
    return render(request, 'app/index.html')

def exit(request):
  if request.user.is_superuser:
    return redirect('admin_view/')
  if request.user.is_anonymous:
    return redirect('/')
  username = request.user.username
  user = User.objects.get(username=username)
  flag = user.student.flag
  unique_flag = False
  D = Registerbook.objects.filter(user = user.student)
  for d in D:
    if(d.exit_time == d.enter_time):
      unique_flag = True
      break
  if( (flag == False) and (unique_flag == True) ):
    user.student.flag = True
    user.student.save()
    tz = pytz.timezone('Asia/Kolkata') 
    datetime_local = datetime.now(tz)
    time_exited = datetime_local.strftime("Time: %H:%M, Date:%D")
    return render(request, 'app/exit.html', {'time_exited':time_exited})
  elif (unique_flag == False):
    msg = "You are trying to exit without reason. Action will be recorded."
    return render(request, 'app/exit.html', {'msg':msg})
  else:
    msg = "You have already went outside of the campus."
    return render(request, 'app/exit.html', {'msg':msg})

def enter(request):
  if request.user.is_superuser:
    return redirect('admin_view/')
  if request.user.is_anonymous:
    return redirect('/')
  username = request.user.username
  user = User.objects.get(username=username)
  flag = user.student.flag
  if(flag == True):
    user.student.flag = False
    user.student.save()
    tz = pytz.timezone('Asia/Kolkata') 
    datetime_local = datetime.now(tz)
    D = Registerbook.objects.filter(user = user.student)
    for d in D:
      if(d.exit_time == d.enter_time):
        d.enter_time = datetime_local
        d.save()
    time_entered = datetime_local.strftime("Time: %H:%M, Date:%D")
    return render(request, 'app/enter.html', {'time_entered':time_entered})
  else:
    msg = "You have already entered the campus."
    return render(request, 'app/enter.html', {'msg':msg})

def admin_view(request):
  if request.user.is_superuser:
    all_students = Registerbook.objects.all()
    students = []
    for s in all_students:
      if s.exit_time.strftime("%D") == datetime.now().strftime("%D"):
        local_tz = pytz.timezone('Asia/Kolkata')
        exit_time_s = s.exit_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        enter_time_s = s.enter_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        t = []
        t.append(exit_time_s.strftime("Time: %H:%M, Date:%D"))
        t.append(enter_time_s.strftime("Time: %H:%M, Date:%D"))
        t.append(s.user.user.username)
        students.append(t)
    return render(request, 'app/admin.html', {'students':students})
  else:
    return redirect('/')

def export(request):
  # Create the HttpResponse object with the appropriate CSV header.
  response = HttpResponse(content_type='text/csv')

  writer = csv.writer(response)
  writer.writerow(['Exit time', 'Enter time', 'Student name', 'Reason'])
  all_students = Registerbook.objects.all()
  for s in all_students:
    if s.exit_time.strftime("%D") == datetime.now().strftime("%D"):
      local_tz = pytz.timezone('Asia/Kolkata')
      exit_time_s = s.exit_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
      enter_time_s = s.enter_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
      writer.writerow([exit_time_s.strftime("Time: %H:%M, Date:%D"),
                       enter_time_s.strftime("Time: %H:%M, Date:%D"), 
                       s.user.user.username,
                       s.reason
                      ])

  response['Content-Disposition'] = 'attachment; filename="data.csv"'
  return response