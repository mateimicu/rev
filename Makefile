VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
IMAGE_NAME = matei10/rev
IMAGE_TAG = local

run_local: $(VENV)/bin/activate
				cd app/ && FLASK_APP='app:create_app()' ../$(PYTHON) -m flask run

test_local: $(VENV)/bin/activate
				pytest app/tests.py


$(VENV)/bin/activate: requirements.txt
				python3 -m virtualenv $(VENV)
				$(PIP) install -r requirements.txt


test_docker: build_docker
				docker run $(IMAGE_NAME):$(IMAGE_TAG) test

run_docker: build_docker
				docker run -ti -p 3000:3000 $(IMAGE_NAME):$(IMAGE_TAG)

build_docker:
				docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

clean:
				rm -rf __pycache__
				rm -rf $(VENV)
