include .env

.PHONY: all

build:
	docker build -t chatbotx .

run:
	export $(cat .env | xargs)
	docker stop chatbotx || true && docker rm chatbotx || true
	docker run --name chatbotx --rm -e OPENAI_API_KEY=${OPENAI_API_KEY} -p 3000:3000 chatbotx

logs:
	docker logs -f chatbotx

push:
	docker tag chatbotx:latest ${DOCKER_USER}/chatbotx:${DOCKER_TAG}
	docker push ${DOCKER_USER}/chatbotx:${DOCKER_TAG}