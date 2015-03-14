
CUR_DIR = $(shell pwd)
DOCKER_IMAGE_PREFIX ?= link_bank_
DB_IMAGE = $(DOCKER_IMAGE_PREFIX)db
DB_NAME = $(DOCKER_IMAGE_PREFIX)db_run
MAIN_IMAGE = $(DOCKER_IMAGE_PREFIX)main
MAIN_NAME = $(DOCKER_IMAGE_PREFIX)main_run
DB_PORT ?= 5433
APP_PORT ?= 8000
export DOCKER_HOST ?= localhost


.PHONY:


runserver: syncdb
	docker run -v $(CUR_DIR):/opt/src --link=$(DB_NAME):db -t -i --rm --name=$(MAIN_NAME) -p $(APP_PORT):8000 $(MAIN_IMAGE) runserver 0.0.0.0:8000


build:
	docker rmi $(MAIN_IMAGE) || echo "Image $(MAIN_IMAGE) not found"
	docker stop $(MAIN_NAME) || echo "Container $(MAIN_NAME) not found"
	docker rm $(MAIN_NAME) || echo "Container $(MAIN_NAME) not found"
	docker build -t $(MAIN_IMAGE) .


syncdb: db_run build
	docker run -v $(CUR_DIR):/opt/src --link=$(DB_NAME):db -t -i --rm --name=$(MAIN_NAME) $(MAIN_IMAGE) syncdb --all


db_init:
	docker rmi $(DB_IMAGE) || echo "Image $(DB_IMAGE) not found"
	docker stop $(DB_NAME) || echo "Container $(DB_NAME) not found"
	docker rm $(DB_NAME) || echo "Container $(DB_NAME) not found"
	cat $(CUR_DIR)/Dockerfile-Postgresql | docker build --rm -t $(DB_IMAGE) -


db_run: db_init
	docker run -p $(DB_PORT):5432 -d  --name=$(DB_NAME) $(DB_IMAGE) && sleep 2
	docker exec $(DB_NAME) createuser -h127.0.0.1 -p5432 -Upostgres bookmarks -S
	docker exec $(DB_NAME) createdb -h127.0.0.1 -p5432 -Upostgres bookmarks -O bookmarks
