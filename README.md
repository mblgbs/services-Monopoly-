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
uvicorn app.main:app --reload --host 127.0.0.1 --port 8004
```

L'API est disponible sur `http://127.0.0.1:8004`.

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
curl http://127.0.0.1:8004/services
curl http://127.0.0.1:8004/services/edf
curl http://127.0.0.1:8004/monopoly/cards?provider=box_tv
```

## Convention de ports locale (multi-services)

- `Web-monopoly-`: `PORT=3000`
- `FranceConnect-Monopoly`: `PORT=8001`
- `compte-de-Banque-Monopoly-`: `PORT=8002`
- `D-claration-Monopoly-`: `PORT=8003`
- `services-Monopoly-`: `PORT=8004`
- `Save service` (si utilise): `PORT=8010`

## Runbook de demarrage (Windows PowerShell)

1) Lancer FranceConnect (`8001`):

```powershell
cd "H:\Mon Drive\FranceConnect-Monopoly"
copy .env.example .env
$env:APP_BASE_URL="http://127.0.0.1:8001"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

2) Lancer la banque (`8002`):

```powershell
cd "H:\Mon Drive\compte-de-Banque-Monopoly-"
$env:PORT="8002"
$env:FRANCECONNECT_BASE_URL="http://127.0.0.1:8001"
python api.py
```

3) Lancer Declaration (`8003`):

```powershell
cd "H:\Mon Drive\D-claration-Monopoly-"
$env:PORT="8003"
$env:FRANCECONNECT_BASE_URL="http://127.0.0.1:8001"
$env:BANK_API_BASE_URL="http://127.0.0.1:8002"
python api.py
```

4) Lancer Services (`8004`):

```powershell
cd "H:\Mon Drive\services-Monopoly-"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8004
```

5) Lancer Web (`3000`):

```powershell
cd "H:\Mon Drive\Web-monopoly-"
$env:PORT="3000"
$env:FRANCECONNECT_BASE_URL="http://127.0.0.1:8001"
$env:BANK_API_BASE_URL="http://127.0.0.1:8002"
npm install
npm start
```

## Structure

- `app/main.py`: routes FastAPI
- `app/schemas.py`: schemas Pydantic
- `app/data/*.json`: jeux de donnees mock
- `app/services/catalog.py`: acces au catalogue
- `app/services/monopoly_adapter.py`: mapping vers cartes Monopoly
- `tests/`: tests pytest
