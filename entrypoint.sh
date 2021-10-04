#!/bin/bash
export FLASK_APP='app:create_app()'

case "$1" in
    run)
        # run flask
        cd app
        python3 -m gunicorn "$FLASK_APP" -b :"$PORT"
        ;;
    test)
        pytest app/tests.py
        ;;
    *)
        exec "$@"
        ;;
esac

