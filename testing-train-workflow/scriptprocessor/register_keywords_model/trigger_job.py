from sagemaker.processing import ScriptProcessor
from dotenv import dotenv_values
import os

def main():
    training_env_vars = dotenv_values('projects/keywords/train/config/prod.env')
    training_env_vars['NEPTUNE_API_TOKEN'] = os.environ['NEPTUNE_API_TOKEN']
    # training_env_vars['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']
    # training_env_vars['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']

    print(training_env_vars)

    script_processor = ScriptProcessor(
        command=['python'],
        image_uri='063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train:seb-test',
        role='arn:aws:iam::063759612765:role/mesh-sagemaker-execution-role-dev',
        instance_count=1,
        instance_type='ml.t3.medium', # ("local", "local_gpu") for local mode
        #instance_type='local',
        env = training_env_vars
    )

    script_processor.run(code='/home/ec2-user/data/repositories/ml-mesh/projects/keywords/train/src/register_trained_model.py')

if __name__ == "__main__":
    main()