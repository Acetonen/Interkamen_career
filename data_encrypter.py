#!/usr/bin/env python3.7

"""Encrypt data files."""

import os
import pickle
from pathlib import Path
from Crypto.Cipher import AES
from Crypto import Random


BASES = os.listdir('data1')
KEY = Path('secret_key').read_bytes()

for base in BASES:
    if base not in ('users_base', 'file.log'):

        base_path = Path('data1').joinpath(base)
        data = base_path.read_bytes()

        IV = Random.new().read(AES.block_size)
        cipher = AES.new(KEY, AES.MODE_CFB, IV)
        enc_data = IV + cipher.encrypt(data)

        base_path.write_bytes(enc_data)


# TEST:
MCR_PATH = Path('data1').joinpath('email_prop')
MCR_BASE = MCR_PATH.read_bytes()
try:
    BASE = pickle.loads(MCR_BASE)
except pickle.UnpicklingError:
    print("Data sucsessfully encrypt.")

IV = MCR_BASE[:AES.block_size]
CIPHER = AES.new(KEY, AES.MODE_CFB, IV)
DECR_MCR_BASE = CIPHER.decrypt(MCR_BASE[AES.block_size:])
try:
    BASE = pickle.loads(DECR_MCR_BASE)
    print("Data sucsessfully decrypt.")
except:
    raise
