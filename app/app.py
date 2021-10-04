#!/usr/bin/env python
"""
Application to store and retrieve a date of birth.
"""
from datetime import datetime, date

from flask import Flask, request, jsonify, request
from pydantic import BaseModel, validator
from spectree import SpecTree, Response
from flask_injector import FlaskInjector


from converters import OnlyLettersConverter
from models import Date, Message, User
from dependencies import configure
from storage import Storage
from message import MessageService


def create_app(*, dependencies_injector=None, config=None):
    app = Flask(__name__)
    app.url_map.converters["onlyletters"] = OnlyLettersConverter
    api = SpecTree("flask")

    if config is not None:
        app.config.update(config)

    if dependencies_injector is None:
        dependencies_injector = configure

    @app.route("/hello/<onlyletters:username>", methods=["PUT"])
    @api.validate(json=Date, resp=Response(HTTP_200=None), tags=["api"])
    def hello_store(username: str, storage: Storage):
        """
        Store a user date of birth.
        """
        user = User(username=username, date_of_birth=request.context.json)
        storage.save(user)
        return ("", 204)

    @app.route("/hello/<onlyletters:username>", methods=["GET"])
    @api.validate(resp=Response(HTTP_200=Message), tags=["api"])
    def hello_retrieve(username: str, storage: Storage):
        """
        Return information about the users birthday.
        """
        message_service = MessageService()
        user = storage.get(username)
        return jsonify(message=message_service.get_message(user))

    @app.route("/health", methods=["GET"])
    @api.validate(resp=Response(HTTP_200=None), tags=["health"])
    def health():
        """
        Health check endpoint.
        """
        return ("", 200)

    # Initialize Flask-Injector. This needs to be run *after* you attached all
    # views, handlers, context processors and template globals.
    FlaskInjector(app=app, modules=[dependencies_injector])
    api.register(app)
    return app
