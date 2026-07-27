# ==========================
# Variables
# ==========================

COMPOSE=docker compose

# ==========================
# Docker
# ==========================

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d --build

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

# ==========================
# Containers
# ==========================

backend:
	$(COMPOSE) exec backend bash

mysql:
	$(COMPOSE) exec mysql mysql -u$$MYSQL_USER -p$$MYSQL_PASSWORD $$MYSQL_DATABASE

# ==========================
# Alembic
# ==========================

migrate:
	$(COMPOSE) exec backend alembic upgrade head

revision:
	$(COMPOSE) exec backend alembic revision --autogenerate -m "$(MSG)"

history:
	$(COMPOSE) exec backend alembic history

current:
	$(COMPOSE) exec backend alembic current

# ==========================
# Development
# ==========================

install:
	$(COMPOSE) exec backend pip install -r requirements.txt

format:
	$(COMPOSE) exec backend ruff format .

lint:
	$(COMPOSE) exec backend ruff check .

check:
	$(MAKE) lint
	$(MAKE) format

# ==========================
# Cleanup
# ==========================

clean:
	$(COMPOSE) down -v
	docker system prune -f

# ==========================
# Rebuild
# ==========================

rebuild:
	$(COMPOSE) down -v
	$(COMPOSE) up -d --build

# ==========================
# Backend Logs
# ==========================

backend-logs:
	$(COMPOSE) logs -f backend