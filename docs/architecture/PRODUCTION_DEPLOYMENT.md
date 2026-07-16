# Production Deployment

## Validate

```bash
python scripts/validate_production.py
```

## Initialize database

```bash
python scripts/migrate_database.py
```

## Start

```bash
python scripts/start_production.py
```

## Docker

```bash
cp .env.production.example .env.production
docker compose -f docker-compose.production.yml up --build
```
