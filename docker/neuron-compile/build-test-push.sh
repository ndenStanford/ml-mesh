COMPILE_NEURON_AWS_ECR='mock-repo'
GIT_COMMIT_HASH_SHORT=$(git rev-parse --short HEAD)


# build & tag
docker build \
    -f ./orchestration/docker/images/compile-neuron/compile-neuron-Dockerfile \
    -t $COMPILE_NEURON_AWS_ECR:$GIT_COMMIT_HASH_SHORT \
    --target test \
    ./orchestration/docker/images/compile-neuron

# run tests
export OUTPUT_DIR=/home/ec2-user/repositories/ml-serve-app/build_utils/docker/torch-neuron/test_artifacts
mkdir $OUTPUT_DIR
touch $OUTPUT_DIR/test

docker run \
    -e AWS_ACCESS_KEY_ID=$(aws configure get default.aws_access_key_id) \
    -e AWS_SECRET_ACCESS_KEY=$(aws configure get default.aws_secret_access_key) \
    --mount type=bind,source=$OUTPUT_DIR,target='/output' \
    $COMPILE_NEURON_AWS_ECR:$GIT_COMMIT_HASH_SHORT \
    pytest test.py

# authenticate docker with ecr
aws ecr get-login-password --region us-east-1 \
    | docker login --username AWS --password-stdin 484375727565.dkr.ecr.us-east-1.amazonaws.com

# push
docker push $COMPILE_NEURON_AWS_ECR:$GIT_COMMIT_HASH_SHORT