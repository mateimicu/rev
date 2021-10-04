#!/usr/bin/env python3

from datetime import date, timedelta, datetime
import string
import random
import json


from injector import singleton
import pytest
import fakeredis

from app import create_app
import storage
import message
from models import Date, User
import message


@pytest.fixture
def client_and_server():
    server = fakeredis.FakeServer()

    def mock_dependencies_injector(binder):
        binder.bind(
            storage.Storage,
            to=storage.FakeRedisStorage(host="dummy", server=server),
            scope=singleton,
        )

    app = create_app(
        dependencies_injector=mock_dependencies_injector, config={"TESTING": True}
    )

    with app.test_client() as client:
        yield (client, server)


@pytest.fixture
def today_date():
    return date.today()


@pytest.fixture
def yesterday_date(today_date):
    return today_date - timedelta(days=1)


@pytest.fixture
def tomorrow_date(today_date):
    return today_date + timedelta(days=1)


@pytest.fixture
def today(today_date):
    return str(today_date)


@pytest.fixture
def yesterday(yesterday_date):
    return str(yesterday_date)


@pytest.fixture
def tomorrow(tomorrow_date):
    return str(tomorrow_date)


@pytest.fixture
def good_username():
    return "".join(random.sample(string.ascii_letters, random.randint(1, 25)))


@pytest.fixture
def bad_username(good_username):
    return good_username + "1"


def test_wrong_username_put(client_and_server, bad_username, yesterday):
    client, _ = client_and_server
    response = client.put("/hello/" + bad_username, data={"dateOfBirth": yesterday})
    assert response.status_code == 404, response.data


def test_date_in_past(client_and_server, good_username, yesterday):
    client, _ = client_and_server
    response = client.put("/hello/" + good_username, data={"dateOfBirth": yesterday})
    assert response.status_code == 204, response.data


def test_date_in_the_future(client_and_server, good_username, tomorrow):
    client, _ = client_and_server
    response = client.put("/hello/" + good_username, data={"dateOfBirth": tomorrow})
    assert response.status_code == 422, response.data


def test_tomorrows_birthday(client_and_server, good_username, tomorrow_date):
    client, server = client_and_server
    faker = fakeredis.FakeRedis(server=server)

    birth_date = message.yearsago(tomorrow_date, -1)

    date_of_birth = Date(dateOfBirth=birth_date)
    user = User(username=good_username, date_of_birth=date_of_birth)

    faker.set(user.username, json.dumps(user.dict(), default=str))
    response = client.get("/hello/" + user.username)
    assert response.status_code == 200, response.data

    assert response.json[
        "message"
    ] == message.MessageService.BIRTHDAY_IN_THE_FUTURE.format(
        username=user.username, n=1
    )


def test_today_birthday(client_and_server, good_username, today_date):
    client, server = client_and_server
    faker = fakeredis.FakeRedis(server=server)

    birth_date = message.yearsago(today_date, -1)

    date_of_birth = Date(dateOfBirth=birth_date)
    user = User(username=good_username, date_of_birth=date_of_birth)

    faker.set(user.username, json.dumps(user.dict(), default=str))
    response = client.get("/hello/" + user.username)
    assert response.status_code == 200, response.data

    assert response.json["message"] == message.MessageService.BIRTHDAY_TODAY.format(
        username=user.username, n=1
    )


def test_yesterday_birthday(client_and_server, good_username, yesterday_date):
    client, server = client_and_server
    faker = fakeredis.FakeRedis(server=server)

    birth_date = message.yearsago(yesterday_date, -1)

    date_of_birth = Date(dateOfBirth=birth_date)
    user = User(username=good_username, date_of_birth=date_of_birth)

    faker.set(user.username, json.dumps(user.dict(), default=str))
    response = client.get("/hello/" + user.username)
    assert response.status_code == 200, response.data

    assert "Your birthday is in" in response.json["message"]


# TODO(mmicu): add a test for 2/29 birthday's
