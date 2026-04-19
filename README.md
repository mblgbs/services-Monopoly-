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
- `GET /ecosystem` — decouverte des URLs des microservices (lecture des variables d'environnement ; aucun appel reseau sortant)
- `GET /services`
- `GET /services?provider=edf`
- `GET /services/{provider}`
- `GET /services/{provider}/{offer_id}`
- `GET /monopoly/cards`
- `GET /monopoly/cards?provider=cpam`

## Decouverte des services (`/ecosystem`)

Pour configurer des clients HTTP (scripts, UI) sans dupliquer les ports : appelez cette API une fois et utilisez les `base_url` retournees.

```bash
curl http://127.0.0.1:8004/ecosystem
```

Les URLs par defaut correspondent au runbook ci-dessous. Vous pouvez les surcharger via `.env` (voir [`.env.example`](.env.example)) : `FRANCECONNECT_BASE_URL`, `BANK_API_BASE_URL`, `DECLARATION_API_BASE_URL`, `SERVICES_MONOPOLY_BASE_URL` (ou `APP_BASE_URL` pour cette API), `WEB_MONOPOLY_BASE_URL`, `SNCF_CONNECT_BASE_URL`, `STRIPE_MONOPOLY_BASE_URL`, `AIRBNB_MONOPOLY_BASE_URL`, `SAVE_SERVICE_BASE_URL`.

Documentation des autres depots : [FranceConnect-Monopoly/README.md](../FranceConnect-Monopoly/README.md), [compte-de-Banque-Monopoly-/README.md](../compte-de-Banque-Monopoly-/README.md), [D-claration-Monopoly-/README.md](../D-claration-Monopoly-/README.md), [Web-monopoly-/README.md](../Web-monopoly-/README.md), [sncf-connect-Monopoly/README.md](../sncf-connect-Monopoly/README.md), [stripe-Monopoly/README.md](../stripe-Monopoly/README.md), [airbnb-monopoly-/README.md](../airbnb-monopoly-/README.md).

## Exemples curl

```bash
curl http://127.0.0.1:8004/services
curl http://127.0.0.1:8004/services/edf
curl http://127.0.0.1:8004/monopoly/cards?provider=box_tv
curl http://127.0.0.1:8004/ecosystem
```

## Convention de ports locale (multi-services)

- `Web-monopoly-`: `PORT=3000`
- `FranceConnect-Monopoly`: `PORT=8001`
- `compte-de-Banque-Monopoly-`: `PORT=8002`
- `D-claration-Monopoly-`: `PORT=8003`
- `services-Monopoly-`: `PORT=8004`
- `sncf-connect-Monopoly`: `PORT=8005`
- `stripe-Monopoly`: `PORT=8006`
- `airbnb-monopoly-`: port `3001` recommande en local si le Web Monopoly utilise deja `3000`
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
- `app/ecosystem.py`: construction du payload `GET /ecosystem`
- `app/schemas.py`: schemas Pydantic
- `app/data/*.json`: jeux de donnees mock
- `app/services/catalog.py`: acces au catalogue
- `app/services/monopoly_adapter.py`: mapping vers cartes Monopoly
- `tests/`: tests pytest
