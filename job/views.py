from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.shortcuts import redirect, get_object_or_404
# Create your views here.

def index(request):
    return render(request,'index.html')

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'admin_login.html',d)

def user_login(request):
    error = ""
    if request.method == "POST":
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(username=uname, password=pwd)
        if user:
            login(request, user)
            error = "no"
        else:
            error = "yes"
    return render(request, 'user_login.html', {'error': error})

def employee_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)

        if user is not None:
            try:
                user1 = Employee.objects.get(user=user)
                if user1.type == "employee":
                    if user1.status.lower() != "pending":
                        login(request, user)
                        error = "no"
                    else:
                        error = "not" 
                else:
                    error = "y"
            except Employee.DoesNotExist:
                error = "y"  
        else:
            error = "y"  

    return render(request, 'employee_login.html', {'error': error})

def employee_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        company = request.POST['company']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Employee.objects.create(user=user, mobile=con, image=i, gender=gen,company=company, type="employee",status="pending")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request,'employee_signup.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        student.user.first_name = f
        student.user.last_name = l
        student.mobile = con
        student.gender = gen
        try:
            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            student.image = i
            student.save()
            error = "no"
        except:
            pass

    d = {'student': student, 'error': error}
    return render(request,'user_home.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    ecount = Employee.objects.all().count()
    scount = StudentUser.objects.all().count()
    d = {'ecount':ecount,'scount':scount}
    return render(request,'admin_home.html',d)

def employee_home(request):
    if not request.user.is_authenticated:
        return redirect('employee_login')
    user = request.user
    employee = Employee.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        employee.user.first_name = f
        employee.user.last_name = l
        employee.mobile = con
        employee.gender = gen
        try:
            employee.save()
            employee.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            employee.image = i
            employee.save()
            error = "no"
        except:
            pass

    d= {'employee':employee,'error':error}
    return render(request,'employee_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def user_signup(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            StudentUser.objects.create(user=user,mobile=con,image=i,gender=gen,type="student")
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request, 'user_signup.html',d)

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data':data}
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def delete_employee(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    employee = User.objects.get(id=pid)
    employee.delete()
    return redirect('employee_all')

def employee_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Employee.objects.filter(status='pending')
    d = {'data':data}
    return render(request,'employee_pending.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    employee = Employee.objects.get(id=pid)
    if request.method=="POST":
        s = request.POST['status']
        employee.status=s
        try:
            employee.save()
            error="no"
        except:
            error="yes"
    d = {'employee':employee,'error':error}
    return render(request,'change_status.html',d)

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passwordadmin.html',d)

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passworduser.html',d)

def change_passwordemployee(request):
    if not request.user.is_authenticated:
        return redirect('employee_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passwordemployee.html',d)

def employee_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Employee.objects.filter(status='Accept')
    d = {'data':data}
    return render(request,'employee_accepted.html',d)

def employee_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Employee.objects.filter(status='Reject')
    d = {'data':data}
    return render(request,'employee_rejected.html',d)

def employee_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Employee.objects.all()
    d = {'data':data}
    return render(request,'employee_all.html',d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('employee_login')
    error=""
    if request.method=='POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        l = request.FILES['logo']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        user = request.user
        employee = Employee.objects.get(user=user)
        try:
            Job.objects.create(employee=employee,start_date=sd,end_date=ed,title=jt,salary=sal,image=l,description=des,experience=exp,location=loc,skills=skills,creationdate=date.today())
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'add_job.html',d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('employee_login')
    user = request.user
    employee = Employee.objects.get(user=user)
    job = Job.objects.filter(employee=employee)
    d={'job':job}
    return render(request,'job_list.html',d)

def delete_job(request,pid):
    job = get_object_or_404(Job, pk=pid)
    job.delete()  # or update status if you're not actually deleting
    return redirect('job_list') 
    
def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('employee_login')
    error=""
    job = Job.objects.get(id=pid)
    if request.method=='POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']

        job.title = jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = skills
        job.description = des
        try:
            job.save()
            error="no"
        except:
            error="yes"
        if sd:
            try:
                job.start_date = sd
                job.save()
            except:
                pass
        else:
            pass
        if ed:
            try:
                job.end_date = ed
                job.save()
            except:
                pass
        else:
            pass
    d = {'error':error,'job':job}
    return render(request,'edit_jobdetail.html',d)

def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('employee_login')
    error=""
    job = Job.objects.get(id=pid)
    if request.method=='POST':
        cl = request.FILES['logo']
        job.image = cl
        try:
            job.save()
            error="no"
        except:
            error="yes"
    d = {'error':error,'job':job}
    return render(request,'change_companylogo.html',d)

def latest_jobs(request):
    job = Job.objects.all().order_by('-start_date')
    d = {'job':job}
    return render(request,'latest_jobs.html',d)

def user_latestjobs(request):
    job = Job.objects.all().order_by('-start_date')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)
    d = {'job':job,'li':li}
    return render(request,'user_latestjobs.html',d)

def job_detail(request,pid):
    job = Job.objects.get(id=pid)
    d = {'job':job}
    return render(request,'job_detail.html',d)

def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()
    if job.end_date < date1:
        error = "close"
    elif job.start_date > date1:
        error = "notopen"
    else:
        if request.method == 'POST':
            r = request.FILES['resume']
            Apply.objects.create(job=job,student=student,resume=r,applydate=date.today())
            error="done"
    d = {'error':error}
    return render(request,'applyforjob.html',d)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('employee_login')
    data = Apply.objects.all()
    d = {'data':data}
    return render(request,'applied_candidatelist.html',d)

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def report(request):
    jobs = Job.objects.all()  # Querying all jobs
    users = User.objects.all()  # Querying all users
    employees = Employee.objects.all()  # Querying all employees
    
    context = {
        'jobs': jobs,
        'users': users,
        'employees': employees,
    }
    
    return render(request, 'report.html', context)