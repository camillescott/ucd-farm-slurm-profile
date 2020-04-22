#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2019
# File   : common.snakefile
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 08.04.2020


from datetime import timedelta


def as_minutes(**kwargs):
    return timedelta(**kwargs).seconds // 60

