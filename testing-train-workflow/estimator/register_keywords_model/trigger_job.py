from sagemaker.estimator import Estimator
import os
from datetime import datetime as dt
import click

@click.command()
@click.option(
    '--instance-type',
    default='ml.m4.xlarge',
    help="Select 'local'/'local_gpu' for testing. Defaults to 'ml.m4.xlarge'."
)
def trigger_sagemaker_train(instance_type):

    estimator = Estimator(
        image_uri='063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train:seb-test-sagemaker',
        base_job_name="register-keywords-model",
        role='arn:aws:iam::063759612765:role/mesh-sagemaker-execution-role-dev',
        instance_count=1,
        instance_type=instance_type,
        environment = {'NEPTUNE_API_TOKEN': os.environ['NEPTUNE_API_TOKEN']}
    )

    estimator.fit(job_name=dt.now().strftime('%Y-%m-%d--%H-%M-%S'))

if __name__ == "__main__":
    trigger_sagemaker_train()
