#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Turbidsoul Chen
# @Date:   2013-11-19 14:47:00
# @Last Modified by:   Turbidsoul Chen
# @Last Modified time: 2014-03-15 12:26:43


import signal

def empty(name):
    while True:
        print("<empty process> " + name)
        yield None

def termination(name, maxn):
    for i in xrange(maxn):
        print("Hear %s, %d out of %d" % (name, i, maxn))
        yield None


def delay(duration=.8):
    pass

