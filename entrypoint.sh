#!/bin/bash
export FLASK_APP='app:create_app()'

case "$1" in
    run)
        # run flask
        cd app
        python3 -m gunicorn "$FLASK_APP" -b :"$PORT" --access-logfile=- --access-logformat "{'remote_ip':'%(h)s','request_id':'%({X-Request-Id}i)s','response_code':'%(s)s','request_method':'%(m)s','request_path':'%(U)s','request_querystring':'%(q)s','request_timetaken':'%(D)s','response_length':'%(B)s'}"
        ;;
    test)
        pytest app/tests.py
        ;;
    faker)
        python3 app/faker.py --host "$FAKER_TARGET"
        ;;
    *)
        exec "$@"
        ;;
esac

