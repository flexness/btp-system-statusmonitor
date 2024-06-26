# btp python webapp boilerplate *wip*
- flask for backend/api
- dash for frontend/display
- JWT, Login/User management
- optional: tailwind, htmx, brwoser-sync, db-alternative, sqlited

## install
- `npm i` for tailwind
- `pip install -r requirements.txt`
- rename `.env.example` & setup env vars
- `python run.py`
- `npm i`

## develop locally
- `npm i browser-sync`

## develop in bas
- tbc

## core/goal
- using sap/fiori/ecosystem presets "only"
- minimal example routes
- user auth using btp/ias
- role based Access for routes/content
- access btp services
- access on premise services/data
- monitor/status/ping route
- 

## optional for later
- single-route-file-management
- 

## sap tech overview
- tbc

## cf cli @ btp deployment
- `cf create-service xsuaa application my-xsuaa -c xs-security.json`
- `cf create-service hana hdi-shared my-hana`
- `cf push` 
