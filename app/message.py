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

class MessageService:
    BIRTHDAY_TODAY = "Hello, {username}! Happy birthday!"
    BIRTHDAY_IN_THE_FUTURE = "Hello, {username}! Your birthday is in {n} day(s)"

    def __init__(self, today=None):
        self._today = today if today else date.today()

    def _get_days_until_birthday(self, birthday):
        try:
            next_birthday = birthday.replace(year=self._today.year)
        except ValueError:
            # It means you were born on a leap year
            next_birthday = birthday.replace(day=28, year=self._today.year)

        # this is it already passed
        if next_birthday < self._today:
            next_birthday = next_birthday.replace(year=self._today.year + 1)


        if next_birthday == self._today:
            return 0
        import pdb; pdb.set_trace()
        return (next_birthday - self._today).days
        # convert to a datetime
        # next_birthday = datetime.combine(next_birthday, datetime.min.time())
        # delta_untill_birthday = next_birthday - datetime.now()
        # days_until_birthday = delta_untill_birthday.days
        # if days_until_birthday == 0:
            # this means we have less then 1 day
            # return 1
        # return days_until_birthday

    def get_message(self, user: User) -> str:
        # There is an assumption that if you are on 2/29 you will
        # celebrate your day on 2/28
        days_until_birthday = self._get_days_until_birthday(
            user.date_of_birth.dateOfBirth
        )

        if days_until_birthday:
            return self.BIRTHDAY_IN_THE_FUTURE.format(
                username=user.username, n=days_until_birthday
            )
        return self.BIRTHDAY_TODAY.format(username=user.username)
