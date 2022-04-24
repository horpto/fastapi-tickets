
build-image:
	DOCKER_BUILDKIT=1 docker build -t tickets .

up: build-image	
	docker-compose up -d tickets-api

logs:
	docker logs --tail 10 -f tickets-api

exec:
	docker exec -it tickets-api bash
