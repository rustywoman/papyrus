# Include Common Configuration
# ---
include .env

# Variables
# ---
PROJECT_NAME = papyrus
API_CONF = .env
PEP8_CONF = .pep8.conf
TS=`date +%Y%m%d%H%M%S`
TEST_DIR = ./.test/
TEST_OK_PDF_FILE_NAME = template_1
TEST_NG_PDF_FILE_NAME = template_2

# Init. - Install Python Modules
# ---
init:
	mkdir ${TEST_DIR}
	pip install -r requirements.txt

# Init. - Check File Exsistence in .gitignore
# ---
check:
	if [ -f $(API_CONF) ];then echo "\n    OK : [ $(API_CONF) ] exists.\n";else echo "\n    NG : [ $(API_CONF) ] not exists...\n"; exit 1;fi
	if [ -f $(PEP8_CONF) ];then echo "\n    OK : [ $(PEP8_CONF) ] exists.\n";else echo "\n    NG : [ $(PEP8_CONF) ] not exists...\n"; exit 1;fi

# Dev. - Lint
# ---
lint:
	pycodestyle *.py --config=$(PEP8_CONF) --verbose --show-source --count

# Dev. - Start API Server by CLI
# ---
cli:
	flask run

# Dev. - Build API Server by Docker Container
# ---
docker-build:
	docker build -t ${PROJECT_NAME}:latest .

# Dev. - Start API Server by Docker Container
# ---
docker-run:
	docker run --env-file $(API_CONF) -p 3020:3020 -it ${PROJECT_NAME}:latest

check-ok-1:
	curl -o $(TEST_DIR)$(TEST_OK_PDF_FILE_NAME)_default.pdf -w '\n' -i \
			--request POST \
			--url http://localhost:$(API_DEFAULT_PORT)/pdf \
			--header 'Accept:application/json' \
			--header 'Content-Type:application/json' \
			--data '{"name":"check-ok-default","ledger":[{"date": "2099/12/01", "id": 666666, "name": "りんご", "price": 1200, "status": "done"},{"date": "2099/12/02", "id": 777777, "name": "みかん", "price": 3400, "status": "close"},{"date": "2099/12/03", "id": 888888, "name": "ぶどう", "price": 5600, "status": "call"},{"date": "2099/12/04", "id": 999999, "name": "びわ", "price": 7800, "status": "warning"}]}'

check-ok-2:
	curl -o $(TEST_DIR)$(TEST_OK_PDF_FILE_NAME)_none_item.pdf -w '\n' -i \
			--request POST \
			--url http://localhost:$(API_DEFAULT_PORT)/pdf \
			--header 'Accept:application/json' \
			--header 'Content-Type:application/json' \
			--data '{"name":"check-ok-none-item","ledger":[]}'

check-ng-1:
	curl -o $(TEST_DIR)$(TEST_NG_PDF_FILE_NAME)_invalid_parameter.pdf -w '\n' -i \
			--request POST \
			--url http://localhost:$(API_DEFAULT_PORT)/pdf \
			--header 'Accept:application/json' \
			--header 'Content-Type:application/json' \
			--data '{"na": "HOGEHOGE"}'

check-ng-2:
	curl -o $(TEST_DIR)$(TEST_NG_PDF_FILE_NAME)_wrong_parameter.pdf -w '\n' -i \
			--request POST \
			--url http://localhost:$(API_DEFAULT_PORT)/pdf \
			--header 'Accept:application/json' \
			--header 'Content-Type:application/json' \
			--data '{"name":"check-ng-wrong-parameter","ledger":[{"date": "2099/12/01", "id": 666666, "namex": "りんご", "pricey": 1200, "status": "done", "hoge": "fugafuga"}]}'

check-ng-3:
	curl -o $(TEST_DIR)$(TEST_NG_PDF_FILE_NAME)_none_parameter.pdf -w '\n' -i \
			--request POST \
			--url http://localhost:$(API_DEFAULT_PORT)/pdf
