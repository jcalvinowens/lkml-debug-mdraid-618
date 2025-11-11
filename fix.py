#!/usr/bin/env python3

import bz2
import os

with open("combined-corrupt-lba-list.txt", "r") as f:
    lbas = [int(x.rstrip()) for x in f.readlines()]

fd_sda = os.open("/dev/null", os.O_RDWR | os.O_EXCL)
fd_sdb = os.open("/dev/null", os.O_RDWR | os.O_EXCL)

for lba in lbas:
    f1 = f"lba-{lba}.sda.bin"
    with open(f1, "rb") as f:
        d1 = f.read()
    l1 = len(bz2.compress(d1))

    f2 = f"lba-{lba}.sdb.bin"
    with open(f2, "rb") as f:
        d2 = f.read()
    l2 = len(bz2.compress(d2))

    if l1 < l2:
        print(f"sda bad, sdb good: {lba}")
        os.pwrite(fd_sda, d1, lba * 512)
        os.pwrite(fd_sdb, d2, lba * 512)
    elif l2 < l1:
        print(f"sda good, sdb bad: {lba}")
        os.pwrite(fd_sda, d2, lba * 512)
        os.pwrite(fd_sdb, d1, lba * 512)
    else:
        raise RuntimeError(f"can't tell: {lba}")
