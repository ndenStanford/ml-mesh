source .env

# In the corresponding folder
docker-compose -f docker-compose.dev.yaml build python-base
docker-compose -f docker-compose.dev.yaml build fastapi-serve
# ------
make apps.start/prompt COMPONENT=backend ENVIRONMENT=dev

make projects.build/summarization COMPONENT=serve
make projects.test/summarization COMPONENT=serve