VENV=.venv
PYTHON =$(VENV)/bin/python3
PIP=$(VENV)/bin/pip3
IMAGE_NAME=matei10/rev
IMAGE_TAG=local
PORT=5000

run_local: $(VENV)/bin/activate
				cd app/ && ../$(PYTHON) -m gunicorn 'app:create_app()' -b :$(PORT) --access-logfile=- --access-logformat "{'remote_ip':'%(h)s','request_id':'%({X-Request-Id}i)s','response_code':'%(s)s','request_method':'%(m)s','request_path':'%(U)s','request_querystring':'%(q)s','request_timetaken':'%(D)s','response_length':'%(B)s'}"

test_local: $(VENV)/bin/activate
				$(PYTHON) -m pytest app/tests.py

$(VENV)/bin/activate: requirements.txt
				python3 -m virtualenv $(VENV)
				$(PIP) install -r requirements.txt

test_docker: build_docker
				docker run $(IMAGE_NAME):$(IMAGE_TAG) test

type_checking: $(VENV)/bin/activate
				$(PYTHON) -m mypy app

run_docker: build_docker
				docker run -ti -p $(PORT):$(PORT) $(IMAGE_NAME):$(IMAGE_TAG)

build_docker:
				docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

publish_docker: build_docker
				docker push $(IMAGE_NAME):$(IMAGE_TAG)

faker_local: $(VENV)/bin/activate
				$(PYTHON) app/faker.py --host=http://0.0.0.0:5000

helm_deploy: publish_docker
				kubectl create ns rev-live --dry-run=client -o yaml | kubectl apply -f -
				helm repo add bitnami https://charts.bitnami.com/bitnami
				helm repo update
				helm dependency update chart
				helm upgrade rev-live \
				--debug \
				--install \
				--namespace=rev-live \
				--atomic \
				--cleanup-on-fail \
				-f chart/values.yaml \
				--set image.repository=$(IMAGE_NAME) \
				--set image.tag=$(IMAGE_TAG) chart
				# If the image has the same name and tag and
				# we already have pods running it will not
				# get pulled again
				kubectl rollout restart deployment -n rev-live rev-live
				kubectl rollout restart deployment -n rev-live rev-live-faker

clean:
				rm -rf __pycache__
				rm -rf $(VENV)
				helm uninstall rev-live
