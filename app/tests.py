#!/usr/bin/env python3
"""
Test for the birthday app.
"""

from datetime import date, timedelta, datetime
import string
import random
import json


from injector import singleton
import pytest
import fakeredis  # type: ignore

from app import create_app
import storage
import message
from models import Date, User


@pytest.fixture
def client_and_server():
    """Create the flask client and a fake server."""
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
    """Return todays date."""
    return date.today()


@pytest.fixture
def yesterday_date(today_date):
    """Return yesterdays date."""
    return today_date - timedelta(days=1)


@pytest.fixture
def tomorrow_date(today_date):
    """Return tomorrows date."""
    return today_date + timedelta(days=1)


@pytest.fixture
def today(today_date):
    """Return todays date as a string."""
    return str(today_date)


@pytest.fixture
def yesterday(yesterday_date):
    """Return yesterdays date as a string."""
    return str(yesterday_date)


@pytest.fixture
def tomorrow(tomorrow_date):
    """Return tomorrows date as a string."""
    return str(tomorrow_date)


@pytest.fixture
def good_username():
    """Return a valid username."""
    return "".join(random.sample(string.ascii_letters, random.randint(1, 25)))


@pytest.fixture
def bad_username(good_username):
    """Return a invalid username."""
    return good_username + "1"


def test_wrong_username_put(client_and_server, bad_username, yesterday):
    """
    Test the API when the username is invalid.
    """
    client, _ = client_and_server
    response = client.put("/hello/" + bad_username, data={"dateOfBirth": yesterday})
    assert response.status_code == 404, response.data


def test_date_in_past(client_and_server, good_username, yesterday):
    """
    Test the API when the birthday is in the past.
    """
    client, _ = client_and_server
    response = client.put("/hello/" + good_username, data={"dateOfBirth": yesterday})
    assert response.status_code == 204, response.data


def test_date_in_the_future(client_and_server, good_username, tomorrow):
    """
    Test the API when the birthday is in the future.
    """
    client, _ = client_and_server
    response = client.put("/hello/" + good_username, data={"dateOfBirth": tomorrow})
    assert response.status_code == 422, response.data


def test_tomorrows_birthday(client_and_server, good_username, tomorrow_date):
    """
    Test the API when the birthday was already set and is tomorrow
    """
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
    """
    Test the API when the birthday was already set and is today
    """
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
    """
    Test the API when the birthday was already set and was yesterday
    """
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
def test_birtday_on_leap_years(good_username):
    """If the birthday is on 2/29 we have an edge case and we celebrate it on 2/28."""
    birthday = date(2004, 2, 29)
    curret_date = date(2021, 2, 28)
    msg = message.MessageService(curret_date)
    assert msg._get_days_until_birthday(birthday) == 0

