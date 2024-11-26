from celery.signals import task_prerun, task_postrun, after_task_publish
from src.generated.tables import Generated
from src.prompt.constants import CeleryStatusTypes

from dyntastic.exceptions import DoesNotExist

from onclusiveml.core.logging import get_default_logger
logger = get_default_logger(__name__)

@after_task_publish.connect
def update_generated_on_publish(sender=None, headers=None, body=None, **kwargs):
    """Update Generated object when the task is published."""
    task_id = headers['id']
    logger.info(f"===================Updating status for task with ID {task_id} to {CeleryStatusTypes.PENDING}")
    try:
        generated = Generated.get(task_id)
        generated.status = CeleryStatusTypes.PENDING
        generated.save()
        logger.info(f"****************************Updated status for task with ID {task_id} to {CeleryStatusTypes.PENDING}")
    except:
        logger.error(f"Cannot update status for task with ID {task_id}")


@task_prerun.connect
def update_generated_on_start(task_id=None, task=None, **kwargs):
    """Update Generated object when the task starts."""
    logger.info(f"======================Updating status for task with ID {task_id} to {CeleryStatusTypes.STARTED}")
    try:
        generated = Generated.get(task_id)
        generated.status = CeleryStatusTypes.STARTED
        generated.save()
        logger.info(f"**************************Updated status for task with ID {task_id} to {CeleryStatusTypes.STARTED}")
    except:
        logger.error(f"Cannot update status for task with ID {task_id}")


@task_postrun.connect
def update_generated_on_complete(task_id=None, task=None, state=None, retval=None, **kwargs):
    """Update Generated object when the task completes."""
    logger.info(f"===============Updating status for task with ID {task_id} to {CeleryStatusTypes.SUCCESS}")
    try:
        generated = Generated.get(task_id)
        if state == 'SUCCESS':
            generated.status = CeleryStatusTypes.SUCCESSFUL
            generated.generation = retval  # Assuming the task returns the generated text
        elif state == 'FAILURE':
            generated.status = CeleryStatusTypes.FAILED
            generated.error = str(retval)  # Assuming `retval` contains error info
        generated.save()
        logger.info(f"****************Updated status for task with ID {task_id} to {CeleryStatusTypes.SUCCESS}")
    except:
        logger.error(f"Cannot update status for task with ID {task_id}")
