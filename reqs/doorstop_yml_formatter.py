#!/usr/bin/env python

import os
import sys
import yaml

DIGITS = 4
SEPARATOR = '-'

def failure(msg):
    print("ERROR: %s. Failing %s." % (
        msg, __file__
    ))
    sys.exit(1)

def yaml_format(filename):
    with open(filename, 'r') as f:
        contents = yaml.safe_load(f)
        if not contents:
            failure("Unable to parse %s." % filename)
        
        if not contents.get('settings'):
            contents['settings'] = {}

        contents['settings']['sep'] = SEPARATOR
        contents['settings']['digits'] = DIGITS

        if not contents.get('attributes'):
            contents['attributes'] = {}
        
        contents['attributes']['publish'] = [
            'verified-by',
            'type',
            'rationale'
        ]

        if not contents['attributes'].get('defaults'):
            contents['attributes']['defaults'] = {}
            contents['attributes']['defaults']['type'] = 'Requirement'

    with open(filename, 'w') as yml_file:
        yaml.dump(contents, yml_file)


if __name__ == '__main__':
    for root, subdirs, files in os.walk('.'):
        for f in files:
            if f == '.doorstop.yml':
                yaml_format(os.path.join(root, f))

    sys.exit(0)