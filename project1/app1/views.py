from django.shortcuts import render, redirect
from .models import Course, Student, Teacher
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required


from .models import Teacher

def adminhome(request):
    teachers = Teacher.objects.all()
    return render(request, 'adminhome.html', {'teachers': teachers})


def course(request):
    return render(request,'course.html')
def add_course(request):
    if request.method == 'POST':
        cname = request.POST.get('course') 
        fee = request.POST.get('fee')       

        if cname and fee:  
            course = Course(coursename=cname, fees=fee)
            course.save()
            return redirect('course')  # Redirect after successful post

    return render(request, 'course.html')  # Handle GET request properly
    

    
def stdsignup(request):
    course = Course.objects.all()
    return render(request,'stdsignup.html',{'course':course})

def add_std(request):
    if request.method =='POST':
        name = request.POST['name']
        address = request.POST['address']
        age = request.POST['age']
        date = request.POST['date']
        course = request.POST['course']
        crse = Course.objects.get(id=course)
        std = Student(studentname=name,address=address,age=age,joiningdate=date,course=crse)
        std.save()
        return redirect('stdsignup')

def show(request):
    students = Student.objects.all()
    return render(request, 'show.html', {"students": students})


def delete(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
    except Student.DoesNotExist:
        pass  # Handle silently or add logging
    return redirect('show')

def edit(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect('show') 

    courses = Course.objects.all()

    if request.method == 'POST':
        student.studentname = request.POST.get('studentname')
        student.address = request.POST.get('address')
        student.age = request.POST.get('age')
        student.joiningdate = request.POST.get('joiningdate')
        course_id = request.POST.get('course')
        try:
            student.course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            pass  # Optional: handle error
        student.save()
        return redirect('show')

    return render(request, 'edit_student.html', {'student': student, 'courses': courses})

def homepage(request):
    return render(request,'homepage.html')
def signuppage(request):
    crs = Course.objects.all()
    return render(request,'signuppage.html',{'crs':crs})

def user_sign(request): 
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        username=request.POST['uname']
        addr=request.POST['add']
        ag=request.POST['age']
        email=request.POST['mail']
        ph=request.POST['phone']
        password=request.POST['pass']
        cpassword=request.POST['cpass']
        # im=request.FILES.get('img')
        cou=request.POST['c']
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'This username already exists')
                return redirect('signuppage')
            else:
                user=User.objects.create_user(first_name=first_name,
                                              last_name=last_name,
                                              username=username,
                                              password=password,
                                              email=email)
                user.save() 
                use=Course.objects.get(id=cou)
                u=User.objects.get(id=user.id)
                reg=Teacher(address=addr,age=ag,phone=ph,user=u,course=use)
                reg.save()
                return redirect('/')

        else:
            messages.info(request,'Password doesnot match')
            return redirect('signuppage')       
    else:
        return render(request,'homepage.html')
    
def log(request):
    if request.method == 'POST':
        username = request.POST.get('usname')
        password = request.POST.get('passd')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['user'] = user.username

            if user.is_staff:
                return redirect('adminhome')  
            else:
                messages.info(request, f'Welcome {user.username}')
                return redirect('teacherhome')  
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('homepage')
    return render(request, 'homepage.html')

@login_required(login_url='homepage')
def teacherhome(request):
    if 'user' in request.session:
        return render(request,'teacherhome.html')
    
def teacher_card(request):
    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'teacher_card.html', {'teacher': teacher})

def logout_fun(request):
    auth.logout(request)
    return redirect('homepage')

def delete_logged_in_teacher(request):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user=request.user).first()
        user = request.user

        if teacher:
            teacher.delete()
        user.delete()
        logout(request)
        return redirect('adminhome')

    return redirect('adminhome')

def manage_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'manage_teachers.html', {'teachers': teachers})


def delete_teacher(request, id):
 
    try:
        teacher = Teacher.objects.get(id=id)
        user = teacher.user

        teacher.delete()
        user.delete()

        return redirect('manage_teachers')
    except Teacher.DoesNotExist:
        return HttpResponseNotFound("Teacher not found.")

def edit_teacher(request, id):
    teacher = Teacher.objects.get(id=id)

    if request.method == 'POST':
        user = teacher.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.save()

        teacher.address = request.POST.get('address')
        teacher.age = request.POST.get('age')
        teacher.phone = request.POST.get('phone')

        course_id = request.POST.get('course')
        teacher.course = Course.objects.get(id=course_id)

        teacher.save()

        return redirect('teacher_card')

    courses = Course.objects.all()
    return render(request, 'edit_teacher.html', {'teacher': teacher, 'courses': courses})