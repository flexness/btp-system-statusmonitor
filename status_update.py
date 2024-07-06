from celery import Celery
import requests
import sys
import os
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url']
    )
    print("check :", app.config)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_celery_app(flask_app):
    celery_app = make_celery(flask_app)
    return celery_app

from app.factory import create_app  # Import your Flask app factory

app = create_app()  # Create Flask app instance

app.config.update(
    broker_url='redis://localhost:6379',
    result_backend='redis://localhost:6379'
)
celery = create_celery_app(app)



@celery.task
def check_service_availability():
    logger.info("check service availability")
    from api.models import Service
    from database import Session
    session = Session()  # Use the session directly from the import
    try:
        logger.info("try")
        services = session.query(Service).all()  # Retrieve the list of services from your database
        for service in services:
            logger.info(f"service: {service}")
            try:
                response = requests.get(service.endpoint, timeout=5)
                service.status = 'up' if response.status_code == 200 else 'down'
            except requests.RequestException:
                service.status = 'down'
        session.commit()  # Update the status in your database
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()  # Ensure the session is removed properly

from celery.schedules import crontab

celery.conf.beat_schedule = {
    'check-services-every-5-minutes': {
        'task': 'status_update.check_service_availability',  # Use the module name here
        'schedule': crontab(minute='*/5')
    },
}
