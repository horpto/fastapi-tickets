
build-image:
	docker build -t tickets .

up: build-image	
	docker-compose up -d

exec:
	docker exec -it tickets-api bash
