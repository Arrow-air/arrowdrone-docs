#!/usr/bin/env python


import sys
from doorstop import build, settings, DoorstopInfo, DoorstopWarning, DoorstopError

# Reorder document `level` fields automatically if a REQ is deleted
settings.REORDER = True

# Parent links are set to null then regenerated every time with the ./build script
# Don't need to check
settings.CHECK_SUSPECT_LINKS = False

# Not all requirements will have children
settings.CHECK_CHILD_LINKS  = False

def main():
    tree = build()
    success = tree.validate(document_hook=check_document, item_hook=check_item)
    sys.exit(0 if success else 1)


def check_document(document, tree):
    if sum(1 for i in document if i.normative) < 10:
        yield DoorstopInfo("fewer than 10 normative items")

def check_item(item, tree, document):
    if not item.get('rationale'):
        yield DoorstopError("Rationale is required!")

    if not item.get('type'):
        yield DoorstopError("Type is required!")

    uid = item.get('path').split('/')[-1]
    if len(item.get('links')) == 0 and not uid.startswith('REQ'):
        yield DoorstopError("A parent is required for a lower level requirement!")

if __name__ == '__main__':
    main()