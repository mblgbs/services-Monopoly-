# services-Monopoly-

API FastAPI pour exposer des offres de services mock (EDF, eau, CPAM, box/TV)
et les convertir en cartes Monopoly.

## Prerequis

- Python 3.10+

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer l'API

```bash
uvicorn app.main:app --reload
```

L'API est disponible sur `http://127.0.0.1:8000`.

## Endpoints

- `GET /health`
- `GET /services`
- `GET /services?provider=edf`
- `GET /services/{provider}`
- `GET /services/{provider}/{offer_id}`
- `GET /monopoly/cards`
- `GET /monopoly/cards?provider=cpam`

## Exemples curl

```bash
curl http://127.0.0.1:8000/services
curl http://127.0.0.1:8000/services/edf
curl http://127.0.0.1:8000/monopoly/cards?provider=box_tv
```

## Structure

- `app/main.py`: routes FastAPI
- `app/schemas.py`: schemas Pydantic
- `app/data/*.json`: jeux de donnees mock
- `app/services/catalog.py`: acces au catalogue
- `app/services/monopoly_adapter.py`: mapping vers cartes Monopoly
- `tests/`: tests pytest
