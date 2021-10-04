#!/bin/bash
export FLASK_APP=app:name

case "$1" in
    run)
        # run flask
        cd app
        python3 -m flask run
        ;;
    test)
        pytest app/tests.py
        ;;
    *)
        exec "$@"
        ;;
esac

