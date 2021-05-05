from zaba.celery import app as celery_app


@celery_app.task(name="accounts.sample_task")
def sample_task(value):
    print(value)


@celery_app.task(name="accounts.notification")
def send_email_from_contact_task(form):
    pass
