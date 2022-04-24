
build-image:
	docker build -t tickets .

up: build-image	
	docker-compose up -d
