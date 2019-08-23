# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Extract fields to csv file for data review
#
#
# - parse email .msg files body
# - parse email subject
# - compile regex for all email dta features
# - add groups to named tuple to match features
# - append to one list of named tuples
# - write final csv

import extract_msg # for msg parsing
import re
from pathlib import Path
from typing import NamedTuple, TypeVar
from collections import namedtuple


# named tuple email data container
class EmailData(NamedTuple):
    ref_num: int
    phone_num: int
    first_name: str
    last_name: str
    address:str
    email: str


# +
# Create one regex per feature
# TODO improve regex

def _ref_num(email: str, subject: str) -> TypeVar:
    """
    Returns ref numer if found else settles for email suject
    """
    patt = re.search(r" number:(?P<ref_number>.*)\n", email)
    
    if patt:
        return patt.group(1)
    else:
        return subject

def _phone(email: str) -> TypeVar:
    patt = re.search(r"Telephone:(?P<phone>.*)\n", email)

    if patt:
        return patt.group(1)
    else:
        return "n/a"
      
def _first_name(email: str) -> TypeVar:
    patt = re.search(r"First name:(?P<f_name>.*)\n", email)

    if patt:
        return patt.group(1)
    else:
        return "n/a"

def _last_name(email: str) -> TypeVar:
    patt = re.search(r"Last name:(?P<l_name>.*)\n", email)

    if patt:
        return patt.group(1)
    else:
        return "n/a"

def _address(email: str) -> TypeVar:
    patt = re.search(r"Address:(?P<address>.*)\n", email)

    if patt:
        return patt.group(1)
    else:
        return "n/a"

def _email(email: str) -> TypeVar:
    patt = re.search(r"Email:(?P<email>.*)\n", email)

    if patt:
        return patt.group(1).strip(r"\r")
    else:
        return "n/a"
    
def email_regex(email: str, subject: str) -> NamedTuple:
    """parse email and return email_data named tuple
    subject parameter only applies to _ref_num parsing"""

    return EmailData(_ref_num(email, subject), 
                     _phone(email),
                     _first_name(email),
                     _last_name(email),
                     _address(email), 
                     _email(email))


# +
# extract emails paths and create generator
emails  = Path(r"emails_test/").glob("*.msg")

# add one EmailData container with features per email
emails_data = []
for email_path in emails:
    with extract_msg.Message(email_path) as msg:
        msg_body = msg.body
        msg_subject = msg.subject
        emails_data.append(email_regex(msg_body, msg_subject))


# -

def strip_string(feature: str) -> str:
    """Cleans whitespaces and return characters from email features"""
    return feature.strip("\r").strip("\n").strip()



# +
import csv

with open('test_email_data.csv', 'w') as f:
    csv_writer = csv.writer(f, delimiter=',')
    headers = ['ref_number','phone_num','first_name', 'last_name', 'address', 'email']
    csv_writer.writerow(headers)
    for email in emails_data:
        features = [strip_string(feature) for feature in email]
        csv_writer.writerow(features)
