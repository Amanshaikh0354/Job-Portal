"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('admin_login',admin_login,name="admin_login"),
    path('user_login',user_login,name="user_login"),
    path('employee_login',employee_login,name="employee_login"),
    path('user_signup',user_signup,name="user_signup"),
    path('user_home', user_home, name="user_home"),
    path('employee_home', employee_home, name="employee_home"),
    path('employee_signup', employee_signup, name="employee_signup"),
    path('admin_home', admin_home, name="admin_home"),
    path('Logout', Logout, name="Logout"),
    path('view_users', view_users, name="view_users"),
    path('employee_pending', employee_pending, name="employee_pending"),
    path('delete_user/<int:pid>', delete_user, name="delete_user"),
    path('change_status/<int:pid>', change_status, name="change_status"),
    path('employee_accepted', employee_accepted, name="employee_accepted"),
    path('employee_rejected', employee_rejected, name="employee_rejected"),
    path('employee_all', employee_all, name="employee_all"),
    path('delete_employee/<int:pid>', delete_employee, name="delete_employee"),
    path('change_passwordadmin', change_passwordadmin, name="change_passwordadmin"),
    path('change_passworduser', change_passworduser, name="change_passworduser"),
    path('change_passwordemployee', change_passwordemployee, name="change_passwordemployee"),
    path('add_job', add_job, name="add_job"),
    path('job_list', job_list, name="job_list"),
    path('delete_job/<int:pid>', delete_job, name="delete_job"),
    path('edit_jobdetail/<int:pid>', edit_jobdetail, name="edit_jobdetail"),
    path('change_companylogo/<int:pid>', change_companylogo, name="change_companylogo"),
    path('latest_jobs', latest_jobs, name="latest_jobs"),
    path('user_latestjobs', user_latestjobs, name="user_latestjobs"),
    path('job_detail/<int:pid>', job_detail, name="job_detail"),
    path('applyforjob/<int:pid>', applyforjob, name="applyforjob"),
    path('applied_candidatelist', applied_candidatelist, name="applied_candidatelist"),
    path('contact', contact, name="contact"),
    path('about', about, name="about"),
    path('report', report, name="report"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
