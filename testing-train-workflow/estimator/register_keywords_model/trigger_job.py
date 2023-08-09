from sagemaker.estimator import Estimator
from dotenv import dotenv_values
import os
from datetime import datetime as dt

def main():
    training_env_vars = dotenv_values('projects/keywords/train/config/prod.env')
    training_env_vars['NEPTUNE_API_TOKEN'] = os.environ['NEPTUNE_API_TOKEN']

    print(training_env_vars)

    estimator = Estimator(
        entry_point="register_trained_model.py",
        source_dir="ml-mesh/testing-train-workflow/estimator/register_keywords_model",
        image_uri='063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train:seb-test',
        base_job_name="register-keywords-model",
        role='arn:aws:iam::063759612765:role/mesh-sagemaker-execution-role-dev',
        instance_count=1,
        #instance_type='ml.m4.xlarge', # ("local", "local_gpu") for local mode
        instance_type='local',
        environment = training_env_vars
    )

    estimator.fit(job_name=dt.now().strftime('%Y-%m-%d--%H-%M-%S'))

if __name__ == "__main__":
    main()