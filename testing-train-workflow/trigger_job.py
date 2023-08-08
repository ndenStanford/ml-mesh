from sagemaker.processing import ScriptProcessor

script_processor = ScriptProcessor(command=['python3'],
                image_uri='063759612765.dkr.ecr.us-east-1.amazonaws.com/python-base:seb-test',
                role='arn:aws:iam::063759612765:role/mesh-sagemaker-executor-role-dev',
                instance_count=1,
                instance_type='ml.m5.large')

script_processor.run(code='/home/ec2-user/data/repositories/ml-mesh/testing-train-workflow/preprocessing.py')
