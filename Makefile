setup::
	@pip install -r requirements.txt

dev_server::
	@python backend/__init__.py

server::
	@uwsgi -H ~/.virtualenvs/HotelUrbano-desafiohu1 --ini uwsgi.ini

import_data::
	@curl -XDELETE http://localhost:9200/desafiohu1; echo;
	@curl -XPOST http://localhost:9200/desafiohu1 -d @mappings.json; echo
	@mongo desafiohu1 --eval "db.dropDatabase()"
	@python backend/data.py

run_frontend::
	@cd frontend && python -m SimpleHTTPServer
