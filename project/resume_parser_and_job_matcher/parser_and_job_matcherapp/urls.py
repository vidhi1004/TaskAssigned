from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("",views.welcome,name="welcome"),
    path("api/register/",CandidateRegistrationView.as_view()),
    path("api/verify/",VerifyUser.as_view()),
    path("api/login/",LoginView.as_view()),
    path("api/job/",JobManagementView.as_view()),
    path("api/resume/",UploadResumeView.as_view()),
    path("api/job_view/",GetJobsView.as_view()),
    path("api/job_match/",JobMatchView.as_view()),
    path("job_list/",views.job_list , name="job_list"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login,name="login"),
    path("verify/",views.werify,name="werify"),
    path("api/profile/",CandidateProfileView.as_view()),
    path("home/",views.home,name="home"),
    path("profile/",views.profile,name="profile"),
    path("upload-resume/",views.upload_resume,name="upload_resume"),
    path("profile_all/",views.profile_all,name="profile_all"),
    path("admin1/",views.admin,name="admin"),
    path("admin_login/",views.admin_login,name="admin_login"),
    path("is_admin/",IsAdminCheckView.as_view()),
    path("api/job/<int:id>/", JobManagementView.as_view()),
    path("api/skills/", SkillsListView.as_view()),
    path("api/skills_creation",SkillsCreation.as_view()),

]