#!/usr/bin/env python
"""
Application to generate fake requests.
"""
import argparse
import requests
import time
import random
import json
from urllib.parse import urljoin
from datetime import date, timedelta
import string

from models import Date

def get_parser():
    """Return the CLI Argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help="Host to target for requests")
    parser.add_argument('--sleep', type=float, default=1, help='Time to sleep between requests')
    return parser

def get_good_username():
    """Return a valid username."""
    return "".join(random.sample(string.ascii_letters, random.randint(1, 25)))

def main():
    parser = get_parser()
    args = parser.parse_args()
    base_url = urljoin(args.host, '/hello')
    # generate a set of valid base_ur/username
    valid_users = {urljoin(base_url, get_good_username()): None for _ in range(50)}

    while True:
        day_in_the_past = date.today() - timedelta(days=random.randint(5, 30))
        url = random.choice(list(valid_users.keys()))
        print(f"Request for {url}")
        date_of_birth = valid_users[url]

        if date_of_birth is None:
            valid_users[url] = date_of_birth
            requests.put(url, data=Date(dateOfBirth=day_in_the_past).dict())
            continue

        # random action between get/put
        if random.random() <= 0.5:
            requests.put(url, data=Date(dateOfBirth=day_in_the_past).dict())
        else:
            requests.get(url)
        time.sleep(args.sleep)

if __name__ == '__main__':
    main()
