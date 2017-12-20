#!/usr/bin/python
#
# hashcash.py
#
# simple (and slow) python Hashcash version 1 implementation
#

import base64
import datetime
import sha
import random
import string

def sha1(string):
    return sha.sha(string).digest()

def randb64str(l):
    b64chars = string.ascii_letters + "+/="
    return ''.join([random.choice(b64chars) for _ in range(l)])

def strtobstr(s):
    return ''.join(format(ord(c), 'b').zfill(8) for c in s)

def valid(hashcash):
    ver, bits, date, resource, ext, rand, counter = hashcash.split(':')
    return '0'*int(bits) in strtobstr(sha1(hashcash))[:int(bits)]

VERSION = "1"
BIT_COLLISION = "20"
EXT = ""
SALT_SIZE = 8

def generate(resource, version=VERSION, bits=BIT_COLLISION, ext=EXT,
             salt_size=SALT_SIZE):
    if version != "1":
        raise

    rand = randb64str(salt_size)
    date = '%s%s%s' % (
        str(datetime.datetime.now().year)[2:].zfill(2),
        str(datetime.datetime.now().month).zfill(2),
        str(datetime.datetime.now().day).zfill(2))

    counter = 0
    while 1:
        candidate = ':'.join([str(version), str(bits),
            date, resource, ext, rand, hex(counter)[2:]])
        if valid(candidate):
            return candidate
        counter += 1


