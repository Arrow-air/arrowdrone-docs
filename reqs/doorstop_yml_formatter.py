#!/usr/bin/env python

import os
import sys
import re
import yaml

DIGITS = 4
SEPARATOR = '-'
TYPE = 'Requirement'

def failure(msg):
    print("ERROR: %s. Failing %s." % (
        msg, __file__
    ))
    sys.exit(1)

def req_yaml_format(filename):
    with open(filename, 'r') as f:
        contents = yaml.safe_load(f)
        if not contents:
            failure("Unable to parse %s." % filename)

        contents['type'] = TYPE
        if not contents.get('rationale'):
            contents['rationale'] = None

        x = contents.get('verified-by')
        if not x or x is None:
            contents['verified-by'] = 'unverified'

    with open(filename, 'w') as yml_file:
        yaml.dump(contents, yml_file)

def doorstop_yaml_format(filename):
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

        # Needs to be specific value
        contents['attributes']['defaults']['type'] = 'Requirement'
        
        # Default is None
        if not contents['attributes']['defaults'].get('rationale'):
            contents['attributes']['defaults']['rationale'] = None

        # Default is "Unverified"
        x = contents['attributes']['defaults'].get('verified-by')
        if not x or x is None:
            contents['attributes']['defaults']['verified-by'] = 'Unverified'


    with open(filename, 'w') as yml_file:
        yaml.dump(contents, yml_file)


if __name__ == '__main__':
    for root, subdirs, files in os.walk('.'):
        for f in files:
            if f == '.doorstop.yml':
                doorstop_yaml_format(os.path.join(root, f))
            elif re.search('[A-Z]+-[0-9]+.yml', f):
                req_yaml_format(os.path.join(root, f))

    sys.exit(0)