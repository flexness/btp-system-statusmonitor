# flask app for statusmonitor *wip*
- flask for backend/api
- bootstrap + bootstrap-tables + boostrap-icons
- celery & redis for updating status in bg
- swagger/flask_restx for swagger-api doc/test
- sqlite for non-prod env
- optional: htmx, brwoser-sync, db-alternative
- later: 
    - JWT, Login/User management
    - dash for charts/graphs


## install
- `pip install -r requirements.txt`
- `python run.py`
- rename `.env.example`
- adjust `Config.py` and `.env`
- adjust `manifest.yml` 
- service-status-update worker (celery+redis):
    - adjust `'schedule': crontab(minute='*/5')` in `status_update.py`
    - start worker `celery -A status_update.celery worker -P solo --loglevel=info -E`
    - start beat for worker `celery -A status_update.celery beat --loglevel=info`

## develop locally
- optional: `npm i browser-sync`

## models
- Service/services incl. self-dependencies / association-table
- Tag/tags incl. service-dependencies / association-table

## sap/btp context
- packages: `hdbcli`, `cfenv`, `sap-xssec`

### btp deployment tbc
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