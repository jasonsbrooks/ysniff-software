#!/usr/bin/env python

import fileinput

index = 12
for line in fileinput.input():
    splitline = line.split(" ")
    if index < len(splitline):
        print line.split(" ")[12]
