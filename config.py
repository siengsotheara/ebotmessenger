﻿import os

SECRET_KEY = 'cambodiakingdomofwonder$12312%s'

FACEBOOK_TOKEN = "EAAG8ZCCEzUlEBAI5DiewsBvJrd3kADU8dCZAZBP6X5am7ZBrsV4G3pLIAnZACZAQSv8L6EHjiIPP2ZCdNhxmQ3hhSrVrNhUhMgskbMdkMtSnQyp9gfPhrFyuW1j12L5CZC2Pgc6sqNOjHT4OZBqXf4Mmr5sHOGnKCf1sCDKZCI0BUdFgZDZD"
VERIFY_TOKEN = "ebot messenger$$"

CASA_LINK = ""

#SET ENV VARIABLE TO FEED ORACLE DATABASE
os.environ["NLS_LANG"] = "AMERICAN.AL32UTF8"

#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:underadmin@localhost/test'
#SQLALCHEMY_DATABASE_URI = "postgresql://esslquvzobcfyy:ccd5b8edfe9853f9b9a15885cd0087095128e901f2b968a9fcc347d3c18c9148@ec2-204-236-236-188.compute-1.amazonaws.com/dfejcsakdnp8kn"
#SQLALCHEMY_DATABASE_URI = "oracle://k:Pr0_K_MIS@192.168.2.5:1521/KRDPDUAT"
SQLALCHEMY_DATABASE_URI = 'oracle://app:Ms#S3cure2018@192.168.2.12:1521/KRDDEV'