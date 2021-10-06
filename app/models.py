#!/usr/bin/env python
"""
Application to store and retrieve a date of birth.
"""
from flask import Flask, request, jsonify
from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from flask import request

from converters import OnlyLettersConverter


class Date(BaseModel):
    dateOfBirth: date

    @validator("dateOfBirth")
    def must_be_a_date_before_today(cls, value):
        if value >= date.today():
            raise ValueError(f"value must be a date before the today date.")
        return value

    class Config:
        schema_extra = {
            # provide an example
            "example": {"dateOfBirth": "1996-08-23"}
        }


class Message(BaseModel):
    message: str

    class Config:
        schema_extra = {
            # provide an example
            "example": {"message": "Hello, <username>! Happy birthday!"}
        }


class User(BaseModel):
    username: str
    date_of_birth: Date
