from sagemaker.estimator import Estimator
import os
from datetime import datetime as dt
import click

@click.command()
@click.option(
    '--image-name',
    default='063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train',
    help="Image name of contaienr to be run on sagemaker. Defaults to `063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train`."
)
@click.option(
    '--image-tag',
    default='seb-test',
    help="Image tag of container to be run on sagemaker. Defaults to `seb-test`."
)
@click.option(
    '--instance-type',
    default='ml.m4.xlarge',
    help="Select 'local'/'local_gpu' for testing. Defaults to 'ml.m4.xlarge'."
)
@click.option(
    '--sagemaker-role',
    default='arn:aws:iam::063759612765:role/mesh-sagemaker-execution-role-dev',
    help="The role passed to the sagemaker service to execute the given job. Defaults to 'arn:aws:iam::063759612765:role/mesh-sagemaker-execution-role-dev'."
)
def trigger_sagemaker_train(image_name, image_tag, instance_type, sagemaker_role):

    estimator = Estimator(
        image_uri=f'{image_name}:{image_tag}',
        base_job_name="register-keywords-model",
        role=sagemaker_role,
        instance_count=1,
        instance_type=instance_type,
        environment = {'NEPTUNE_API_TOKEN': os.environ['NEPTUNE_API_TOKEN']},
        container_log_level=10
    )

    estimator.fit(job_name=dt.now().strftime('%Y-%m-%d--%H-%M-%S'))

if __name__ == "__main__":
    trigger_sagemaker_train()
