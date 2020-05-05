from celery.schedules import crontab
from celery.task import periodic_task


@periodic_task(
    run_every=(crontab(minute=15, hour=3)),
    name="task_inform_user",
    ignore_result=True
)
def task_inform_users_expires(**kwargs):
    """
    Inform users about expiration date
    """
    pass
