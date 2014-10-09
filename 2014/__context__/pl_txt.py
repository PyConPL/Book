#!/usr/bin/python
# -*- coding: UTF-8 -*-


def apply_patch(diffsrc, test_mode=0):
    return "cat " + (diffsrc + ["/dev/null"])[test_mode] + " | patch -d .tmp"

