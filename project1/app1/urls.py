from django.urls import path
from . import views

urlpatterns = [
   path('adminhome/', views.adminhome, name='adminhome'),
   path('course', views.course, name='course'),
   path('add_course', views.add_course, name='add_course'),
   path('stdsignup', views.stdsignup, name='stdsignup'),
   path('add_std', views.add_std, name='add_std'),
   path('show/', views.show, name='show'),
   path('edit/<int:student_id>/', views.edit, name='edit'),
   path('student/<int:student_id>/', views.delete, name='delete'),
   path('',views.homepage,name='homepage'),
   path('signuppage',views.signuppage,name='signuppage'),
   path('user_sign',views.user_sign,name='user_sign'),
   path('log',views.log,name='log'),
   path('teacherhome',views.teacherhome,name='teacherhome'),
   path('teacher_card/', views.teacher_card, name='teacher_card'),  
   path('logout_fun',views.logout_fun,name='logout_fun'),
   path('delete_teacher/<int:id>/', views.delete_teacher, name='delete_teacher'),
   path('manage_teachers/', views.manage_teachers, name='manage_teachers'),
   path('delete_logged_in_teacher/', views.delete_logged_in_teacher, name='delete_logged_in_teacher'),
   path('edit_teacher/<int:id>/', views.edit_teacher, name='edit_teacher'),


]
