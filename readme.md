# flask webap for sap btp statusmonitor *wip*
- flask for backend/api
- dash for frontend/display
- JWT, Login/User management
- flowbite/tailwind 
- optional: htmx, brwoser-sync, db-alternative, sqlite


## install
- `pip install -r requirements.txt`
- `npm i` for tailwind/flowbite (if not using flowbite/tailwind CDNs)
- rename `.env.example` & setup env vars
- `python run.py`

## develop locally
- `npm i browser-sync`

## develop in bas
- tbc


## sap tech overview
- tbc

## cf cli @ btp deployment
- `cf create-service xsuaa application my-xsuaa -c xs-security.json`
- `cf create-service hana hdi-shared my-hana`
- `cf push` 
