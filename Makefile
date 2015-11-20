dev_server::
	python backend/__init__.py

server::
	uwsgi -H ~/.virtualenvs/HotelUrbano-desafiohu1 --ini uwsgi.ini

import_data::
	python backend/data.py

index::
	curl -XDELETE http://localhost:9200/desafiohu1; echo;
	curl -XPOST http://localhost:9200/desafiohu1 -d @mapping.json; echo
	curl -XPOST http://localhost:9200/_bulk --data-binary @data/beers.data; echo

