frontend-test:
	docker compose -f docker-compose.test.yml run --rm frontend-test npm run test:unit

frontend-test-e2e: 
	docker compose -f docker-compseo.test.yml run --rm frontend-test npm run test:e2e

backend-test:
	docker compose -f docker-compose.test.yml run --rm backend-test pytest