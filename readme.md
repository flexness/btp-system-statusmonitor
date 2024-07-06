# flask webap for sap btp statusmonitor *wip*
- flask for backend/api
- bootstrap + bootstrap-tables + boostrap-icons
- dash for charts/graphs 
- JWT, Login/User management
- optional: htmx, brwoser-sync, db-alternative, sqlite
- swagger for api doc/test


## install
- `pip install -r requirements.txt`
- `python run.py`
- rename `.env.example`
- adjust `Config.py` and `.env`
- adjust `manifest.yml` 
- adjust `'schedule': crontab(minute='*/5')` in `status_update.py`
- `celery -A status_update.celery beat --loglevel=info`
- `celery -A status_update.celery worker -P solo --loglevel=info -E`

## develop locally
- `npm i browser-sync`

## develop in bas
- tbc

## models
- Service/services incl. self-dependencies / association-table
- Tag/tags incl. service-dependencies / association-table


## sap tech overview
- tbc

## cf cli @ btp deployment
- `cf create-service xsuaa application my-xsuaa -c xs-security.json`
- `cf create-service hana hdi-shared my-hana`
- `cf push` 

## crit notes
- @ bootstrap table `data-side-pagination="server"` very dangerous (no more refresh, no more pagination, no more filter by search, ..)
- @ bootstrap table data-url e.g. `data-url="http://127.0.0.1:3000/api/services/"` table rows get auto-rendered!



## status update worker
celery and redis for updating status of service with worker/task (celery) and msg-broker/queue (redis)
- `celery -A status_update.celery beat --loglevel=info`
- `celery -A status_update.celery worker --loglevel=info -E`
- `celery -A status_update.celery worker -P solo --loglevel=info -E`