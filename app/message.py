#!/usr/bin/env python3
from datetime import datetime, timedelta, date
import calendar
from models import User


def yearsago(conversion_date, years):
    date_in_datetime = datetime.combine(conversion_date, datetime.min.time())
    try:
        return date_in_datetime.replace(year=date_in_datetime.year + years).date()
    except ValueError:
        # Must be 2/29!
        return date_in_datetime.replace(
            month=2, day=28, year=date_in_datetime.year + years
        )


def get_age(birthday):
    today = date.today()
    return (
        today.year
        - birthday.year
        - ((today.month, today.day) < (birthday.month, birthday.day))
    )


class MessageService:
    BIRTHDAY_TODAY = "Hello, {username}! Happy birthday!"
    BIRTHDAY_IN_THE_FUTURE = "Hello, {username}! Your birthday is in {n} day(s)"

    @staticmethod
    def _get_days_until_birthday(birthday):
        today = date.today()
        if today.month == birthday.month:
            if today.day == birthday.day:
                return 0

            # There is an assumption that if you are on 2/29 you will
            # celebrate your day on 2/28
            if (
                birthday.day == 29
                and today.day == 29
                and not calendar.isleap(today.year)
            ):
                return 0

        next_birthday = datetime.combine(
            yearsago(birthday, get_age(birthday) + 1), datetime.min.time()
        )

        delta_untill_birthday = next_birthday - datetime.now()
        days_until_birthday = delta_untill_birthday.days
        if days_until_birthday == 0:
            # this means we have less then 1 day
            return 1
        return days_until_birthday

    def get_message(cls, user: User) -> str:
        # There is an assumption that if you are on 2/29 you will
        # celebrate your day on 2/28
        days_until_birthday = cls._get_days_until_birthday(
            user.date_of_birth.dateOfBirth
        )

        if days_until_birthday:
            return cls.BIRTHDAY_IN_THE_FUTURE.format(
                username=user.username, n=days_until_birthday
            )
        return cls.BIRTHDAY_TODAY.format(username=user.username)
