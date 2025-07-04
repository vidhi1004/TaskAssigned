from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import random
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import docx2txt
import pymupdf
from rest_framework import status


class CandidateRegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserRegisterationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": 400, "message": "something is wrong", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(100000, 999999)
        email = request.data['email']
        username = request.data['username']
        if Users.objects.filter(username=data['username']).exists():
            # raise serializers.ValidationError("username already exists")
            return Response({"status": 400, "message": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if Users.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("email already in use")
            return Response({"status": 400, "message": "email already exists"})
        send_mail(otp, email, username)
        token = AccessToken()
        validate = serializer.validated_data

        token['username'] = validate['username']
        token['email'] = validate['email']
        token['password'] = validate['password']
        token['first_name'] = validate['first_name']
        token['last_name'] = validate['last_name']
        token['phone_number'] = validate['phone_number']
        token['otp'] = otp

        return Response({"status": 200, "message": "OTP has been sent to you", "access_token": str(token), "error": serializer.errors}, status=status.HTTP_200_OK)


def send_mail(otp, email, username):
    context = {
        "username": username,
        "otp": otp
    }

    subject = "Your Mail Needs To be verified"
    message = render_to_string("email\email_verification.html", context)
    email_from = settings.EMAIL_HOST_USER
    email_to = [email]
    email = EmailMessage(subject=subject, body=message,
                         from_email=email_from, to=email_to)
    email.content_subtype = 'html'
    email.send()


class VerifyUser(APIView):
    def post(self, request):
        user_otp = request.data['otp']
        user_token = request.data['access_token']

        token = AccessToken(user_token)

        if str(token['otp']) == str(user_otp):
            Users.objects.create_user(
                username=token['username'],
                password=token['password'],
                email=token['email'],
                first_name=token['first_name'],
                last_name=token['last_name'],
                phone_number=token['phone_number'],
                is_active=True
            )
            return Response({"status": 200, "message": "user has been successfulyy created"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = Users.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({"status": 200, "refresh_token": str(refresh), "access_token": str(refresh.access_token)}, status=status.HTTP_202_ACCEPTED)
        return Response({"error": "something is"})


class JobManagementView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data
        serializer = JobManagementSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            match_candidates_for_job(job)
            return Response({"message": "job posted successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "something went wrong", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        job_obj = Job.objects.all()
        serializer = JobSerializer(job_obj, many=True)
        if serializer.is_valid():
            return Response({serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id):
        try:
            Job.objects.filter(id=id).delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)


class UploadResumeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        uploaded_file = request.FILES.get('resume')

        if not uploaded_file:
            return Response({"message": "no file uploaded"})

        ext = uploaded_file.name.split(".")[-1].lower()

        content = ''

        if ext == 'pdf':
            doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                content += page.get_text()
        elif ext == 'docx':
            content = docx2txt.process(uploaded_file)
        else:
            return Response({"message": "filetype not supported"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        skill = []
        all_skills = Skills.objects.all()
        resume_text = content.lower()
        for s in all_skills:
            if s.name.lower() in resume_text:
                skill.append(s)

        user = request.user
        user.resume_file = uploaded_file
        user.resume_content = content
        user.save()
        user.skills.set(skill)
        match_jobs_for_user(user)
        return Response({"message": "resume uploaded successfully and job matched"}, status=status.HTTP_200_OK)


class GetJobsView(APIView):
    def get(self, request):
        job_obj = Job.objects.all()
        serializers = JobSerializer(job_obj, many=True)
        return Response({"status": 200, "payload": serializers.data}, status=status.HTTP_200_OK)


class JobMatchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        job_match_obj = MatchedJob.objects.filter(candidate=user)
        serializers = JobMatchSerializer(job_match_obj, many=True)
        return Response({"payload": serializers.data}, status=status.HTTP_200_OK)


class CandidateProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class IsAdminCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"is_admin": user.is_staff or user.is_superuser})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def profile_all(request):
    users = Users.objects.filter(is_staff=False, is_superuser=False)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


class SkillsListView(APIView):
    def get(self, request):
        skills = Skills.objects.all()
        serializer = SkillsSerializer(skills, many=True)
        return Response(serializer.data)

class SkillsCreation(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminUser]
    def post(self ,request):
        serializer=SkillsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"skills added successfully."})
        return Response({"message":"skills not created,something went wrong"})

def job_list(request):
    return render(request, "parser_and_job_matcherapp\job_list.html")


def signup(request):
    return render(request, "parser_and_job_matcherapp\signup.html")


def login(request):
    return render(request, "parser_and_job_matcherapp\login.html")


def werify(request):
    return render(request, "parser_and_job_matcherapp\werify.html")


@permission_classes([IsAuthenticated])
def home(request):
    return render(request, "parser_and_job_matcherapp\home.html")


def profile(request):
    return render(request, "parser_and_job_matcherapp\profile.html")


def upload_resume(request):
    return render(request, "parser_and_job_matcherapp/upload_resume.html")


def welcome(request):
    return render(request, "parser_and_job_matcherapp/welcome.html")


@permission_classes([IsAdminUser])
def admin(request):
    return render(request, "parser_and_job_matcherapp\\admin_dashboard.html")


@permission_classes([IsAdminUser])
def admin_login(request):
    return render(request, "parser_and_job_matcherapp\\login_admin.html")


def match_jobs_for_user(user):
    user_skills = set(user.skills.all())
    for job in Job.objects.exclude(title="").filter(required_skills__isnull=False).distinct():
        required_skills = set(job.required_skills.all())
        matching_skills = user_skills.intersection(required_skills)

        if matching_skills:
            match_percentage = (len(matching_skills) /
                                len(required_skills)) * 100
            MatchedJob.objects.update_or_create(
                candidate=user,
                job=job,
                defaults={"match_percentage": match_percentage}
            )


def match_candidates_for_job(job):
    required_skills = set(job.required_skills.all())
    for user in Users.objects.exclude(resume_content__isnull=True).exclude(resume_content=""):
        user_skills = set(user.skills.all())
        matching_skills = user_skills.intersection(required_skills)

        if matching_skills:
            match_percentage = (len(matching_skills) /
                                len(required_skills)) * 100
            MatchedJob.objects.update_or_create(
                candidate=user,
                job=job,
                defaults={"match_percentage": match_percentage}
            )
