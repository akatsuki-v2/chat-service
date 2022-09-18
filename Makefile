#!/usr/bin/make

REPO_DIR = ..

build: # build all containers
	# @docker build -t user-gateway-service:latest $(REPO_DIR)/user-gateway-service
	@docker build -t chat-service:latest $(REPO_DIR)/chat-service

clone: # clone all containers
	# @if [ ! -d $(REPO_DIR)/user-gateway-service ]; then git clone git@github.com:akatsuki-v2/user-gateway-service.git $(REPO_DIR)/user-gateway-service; fi
	@if [ ! -d $(REPO_DIR)/chat-service ]; then git clone git@github.com:akatsuki-v2/chat-service.git $(REPO_DIR)/chat-service; fi

pull: # pull all containers
	# cd $(REPO_DIR)/user-gateway-service && git pull
	cd $(REPO_DIR)/chat-service && git pull

run-bg: # run all containers in the background
	@docker-compose up -d \
		chat-service \
		postgres
		# user-gateway-service \
		# redis \
		# rabbitmq \
		# elasticsearch \

run: # run all containers in the foreground
	@docker-compose up \
		chat-service \
		postgres
		# user-gateway-service \
		# redis \
		# rabbitmq \
		# elasticsearch \

logs: # attach to the containers live to view their logs
	@docker-compose logs -f

test: # run the tests
	@docker-compose exec chat-service /scripts/run-tests.sh

test-dbg: # run the tests in debug mode
	@docker-compose exec chat-service /scripts/run-tests.sh --dbg
