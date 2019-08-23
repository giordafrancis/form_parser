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

import extract_msg
import re
from pathlib import Path
from typing import NamedTuple
from collections import namedtuple


def email_regex(email: str) -> NamedTuple:
    """parse email and return email_data named tuple"""
    
    email = str(email)
    # create the named tupe required and default fileds
    fields = ['ref_number', 'first_name', 'last_name', 'address', 'email', 'phone']
    EmailData = namedtuple('EmailData', fields, defaults=(None,) * len(fields))
    
    # individual regex for each field
    phone = re.search(r"Telephone:(?P<phone>.*)\n", email)
    ref_number = re.search(r" number:(?P<ref_number>.*)\n", email)
    first_name = re.search(r"First name:(?P<f_name>.*)\n", email)
    last_name = re.search(r"Last name:(?P<l_name>.*)\n", email)
    address = re.search(r"Address:(?P<addres>.*)\n", email)
    email = re.search(r"Email:(?P<email>.*)\n", email)
    
    return EmailData(ref_number.group(1), 
                     first_name.group(1),
                     last_name.group(1),
                     address.group(1),
                     email.group(1), 
                     phone.group(1))


# extract fields to csv file for data review
#
# - parse email .msg files body
# - parse all emails into equivalent txt files
# - loop over each text filee
# - compile regex for all data capture points for file loop
# - add groups to named tuple
# - append to one list of named tuples
# - write final csv

# extract emails paths and create gen
emails  = Path(r"tariq_emals_automation/").glob("*.msg")

# +
emails_data = []
for email_path in emails:
    with extract_msg.Message(email_path) as msg:
        msg_body = msg.body
        print(msg_body)
        emails_data.append(email_regex(email_path))
        
msg_body
# -

# instanciate gen of txt files
txts = Path(r"tariq_emals_automation/").glob("*.txt")

test_string = """
Submitted on Wednesday, August 21, 2019 - 11:32


Submission reference number: 

Submitted values are:



==Your details==

 name: 

Last name: 

Address:  

Email:  

Telephone:  

"""







lines = []
for line in test_string.split('\n'):
    if line:
        lines.append(line.strip())
lines

file1 = open("msg_txt")

file1.readline()

lines = []
for line in file1:
    if line:
        lines.append(line.strip("\n").strip())
lines


