#!/usr/bin/env python3

from classes.Scribe import Scribe
from os import path

# TODO: Font and container relative to image size

if __name__ == "__main__":
    do_it = Scribe(path.dirname(path.realpath(__file__)))
    do_it.start()
