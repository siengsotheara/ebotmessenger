from datetime import datetime
from dateutil import parser
from decimal import *

getcontext().prec

def to_datetime(val):
    if not val:
        return None
    return parser.parse(val)

def to_int(val):
    if not val:
        return 0
    return int(val)

def to_decimal(val):
    val = val.strip().split(' ')[0]
    val = val.replace('%', '')
    val = val if val else '0'
    return Decimal(val)