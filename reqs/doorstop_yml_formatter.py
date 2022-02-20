#!/usr/bin/env python

import os
import sys
import yaml

DIGITS = 4
SEPERATOR = '-'

def failure(msg):
    print("ERROR: %s. Failing %s." % (
        msg, __file__
    ))
    sys.exit(1)

def yaml_format(filename):
    contents = yaml.safe_load(filename)
    if not contents:
        failure("Unable to parse %s." % filename)
    
    contents['sep'] = SEPARATOR
    contents['digits'] = DIGITS
    if not contents['attributes']:
        contents['attributes'] = {}
    
    contents['attributes']['publish'] = [
        'verified-by',
        'type',
        'rationale'
    ]

    with open(filename, 'w') as yml_file:
        yaml.dump(contents, yml_file)


if __name__ == '__main__':
    for root, subdirs, files in os.walk('.'):
        for f in files:
            if f == '.doorstop.yml':
                yaml_format(os.path.join(root, f))

    sys.exit(0)