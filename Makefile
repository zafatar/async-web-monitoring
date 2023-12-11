#!/usr/bin/env make

.DEFAULT_GOAL: help

PROJECT_NAME=web-monitoring

DOCKER?=docker

DOCKER_COMPOSE?=docker-compose -p $(PROJECT_NAME)

SERVICE?=webmonitor

SHELL_COMMAND_WITHOUT_DEPS?=$(DOCKER_COMPOSE) run --rm -T --no-deps $(SERVICE) bash -c

.PHONY: help
help: ## List all Python Makefile targets
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

##
## webmonitoring containers 📦
## -----------------
##
.PHONY: build
build: ## Build webmonitor container
	$(DOCKER_COMPOSE) build --no-cache $(SERVICE)

.PHONY: run
run:  ## Run webmonitor container along with database
	$(DOCKER_COMPOSE) up --build $(SERVICE) -d

.PHONY: stop
stop:  ## Stop and remove the running containers
	$(DOCKER_COMPOSE) down

.PHONY: clear
clear:  ## Clear volumes and stop containers
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
	docker image prune -af --filter label=web-monitoring/$(SERVICE)

.PHONY: logs
logs:  ## Show logs for webmonitor container
	$(DOCKER_COMPOSE) logs -f $(SERVICE)

.PHONY: list
list: ## List all running containers
	$(DOCKER) ps

##
## Links and stats 📊
## -----------------
##
.PHONY: stats
stats: ## Show stats for the first 100 links
	@if [ "$(shell docker inspect -f '{{.State.Running}}' web-monitoring-webmonitor)" = "true" ]; then \
		$(DOCKER) exec -it web-monitoring-$(SERVICE) python src/cli.py --offset 0 --limit 100; \
	else \
		echo "Container is not running"; \
	fi

##
## webmonitoring tests 🧪
## -----------------
##
.PHONY: test
test:  ## Run tests
	$(DOCKER_COMPOSE) run --rm $(SERVICE) pytest -v

##
## Python Code Analysis 🔎
## --------------------
##
.PHONY: format
format: ## Format code
	$(SHELL_COMMAND_WITHOUT_DEPS) "isort tests src && black ."

.PHONY: style
style: ## Check lint, code styling rules
	$(SHELL_COMMAND_WITHOUT_DEPS) "flake8 tests src && isort tests src -c && black --check ."
