build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

ps:
	docker compose ps

log:
	docker compose logs chatbot

tail:
	docker compose logs -f chatbot

shell:
	docker compose exec chatbot sh

test:
	docker compose exec chatbot pytest tests --asyncio-mode=strict