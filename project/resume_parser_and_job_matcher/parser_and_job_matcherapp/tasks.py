from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from parser_and_job_matcherapp.models import Users, MatchedJob

@shared_task
def send_weekly_job_match_emails():
    users = Users.objects.filter(is_active=True).exclude(resume_content__isnull=True).exclude(resume_content="")

    for user in users:
        matched_jobs = MatchedJob.objects.filter(candidate=user)

        if matched_jobs.exists():
            subject = "Your Weekly Job Matches from JobMatcher"
            context = {
                "user": user,
                "matched_jobs": matched_jobs
            }

            message = render_to_string("email\job_match_email.html", context)
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.content_subtype = 'html'
            email.send()
    