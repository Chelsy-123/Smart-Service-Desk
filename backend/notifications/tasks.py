from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from notifications.models import NotificationLog

@shared_task(bind=True, max_retries=3)
def send_notification_async(self, log_id):
    log = None
    try:
        log = NotificationLog.objects.select_related(
            "event", "channel"
        ).get(id=log_id)

        template = log.event.notificationtemplate_set.filter(
            channel=log.channel,
            is_active=True
        ).first()

        if not template:
            raise Exception("No template found")

        subject = (
            template.subject_template.format(**log.payload)
            if template.subject_template
            else "Notification"
        )
        body = template.body_template.format(**log.payload)

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[log.recipient_address],
            fail_silently=False
        )

        log.status = "SENT"
        log.sent_at = timezone.now()
        log.save()

    except Exception as exc:
        if log:
            log.status = "FAILED"
            log.error_message = str(exc)
            log.save()

        raise self.retry(exc=exc, countdown=10)
