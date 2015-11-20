dev_server::
	@python backend/__init__.py

server::
	@uwsgi -H ~/.virtualenvs/HotelUrbano-desafiohu1 --ini uwsgi.ini

import_data::
	@curl -XDELETE http://localhost:9200/desafiohu1; echo;
	@curl -XPOST http://localhost:9200/desafiohu1 -d @mappings.json; echo
	@python backend/data.py

