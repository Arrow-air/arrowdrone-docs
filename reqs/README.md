# Requirements

## Table of Contents

- [Dependencies](#dependencies)
- [Layout](#layout)
- [Requirement Files](#requirement-files)
- [How to Validate the Requirements](#how-to-validate-the-requirements)
- [How to Export Requirements](#how-to-export-requirements)
- [How to Add a Requirement Category](#how-to-add-a-requirement-category)
- [How to Add a Requirement](#how-to-add-a-requirement)
- [How to View Requirements](#how-to-view-requirements)

## Dependencies

```python3
pip3 install doorstop pyyaml
```

Requirements are managed with [doorstop](https://doorstop.readthedocs.io/en/latest/).

The `doorstop` command can be run in any directory, but this README assumes the current directory is `reqs/`.

## Layout

The top level requirement directory is `reqs`. The requirements in this repository are the highest level platform requirements. They have the prefix `REQ`.

Lower level requirement locations:
- Software-related: `SW/`
- Electronics-related: `HW/`
- Mechanical-related: `MECH`
- Project directives: `PROJ/`

An example layout of requirements is below.
```tree
.
├── build
├── REQ-0001.yml
├── PROJ
│   └── PROJ-0001.yml
├── HW
    └── HW-0001.yml
│   └── FLIGHT
│       └── FLIGHT-0001.yml
└── SW
    └── SW-0001.yml
    ├── CMD_SVC
    │   ├── CMD_SVC-0001.yml
    ├── HEALTH_SVC
    │   ├── HEALTH_SVC-0001.yml
    └── TLM_SVC
        ├── TLM_SVC-0001.yml
```

## Requirement Files

The requirements are individual `.yml` files. Each contains the requirement's primary text as well as metadata.

```yml
# reqs/SW/HEALTH/HEALTH_SVC-0001.yml
active: true
derived: false
header: ''
level: 1.0
links:
- SW-0001: bBkf6YMFHFULHe5eLcjSBipaMvJL7t5BdNTRJdS-4Ug=
normative: true
rationale: |
  If a device is acting offnominally, the software manager in charge of that device may elect to mark it as SICK or DEAD
   to prevent accidental further usage.
ref: ''
reviewed: 7Pi6ZnjoRSEqcevT_DevP6N0liXRQPDnPh1W4QYxSz4=
text: |
  HEALTH_SVC shall provide an interface to mark a device as HEALTHY, SICK, or DEAD.
```

Important Field | Description
---- | ---
`text` | The primary text of the requirement
`rationale` | Why the requirement exists, explanation of values in requirement, etc. This is a required field and is enforced with the `build` script.
`links` | Links to parent requirements. In this case SW-0001 (*The platform shall maintain the health status of each device*) is the parent requirement. **All lower level requirements must have a parent.** This is enforced with the `build` script.
`active` | If the requirement is in draft and you don't want to cause build errors, set this to `false`.


## How to Validate the Requirements

Use the `reqs/build` script.

`reqs/build` will call:
- `doorstop_yml_formatter.yml`
  - Enforces the existence of the following fields: `verified-by`, `verified-date`, `verified-comments`, `type`, `rationale`
  - Sets all parent link signatures to `null`
      - `doorstop_hooks.py` will regenerate all signatures
      - This avoids common "suspect link" error
- `doorstop_hooks.py`
  - A wrapper around `doorstop` with extra rules:
    - `rationale` and `type` are required non-empty fields
  - Will not check that all requirements have children (may be turned on later)
  - Will not check for suspect links
      - All parent link signatures were set to `null` in `doorstop_yml_formatter.py`
  - Will regenerate link signatures
  - Will reorder the `level` fields of documents to be consecutive
- `doorstop publish all public/`
- `doorstop export all ./csv_files/`

An ideal build will look like so:

```zsh
➜  reqs git:(main) ✗ ./build
building tree...
loading documents...
publishing tree to '/home/ams/gitprojects/arrowdrone-docs/reqs/REQ'...
published: /home/ams/gitprojects/arrowdrone-docs/reqs/REQ
building tree...
loading documents...
exporting tree to './csv_files'...
exported: ./csv_files
```

Common errors and their fixes:

Common Error | Fix
--- | ---
`EXAMPLE-0001: Rationale is required!` | Populate a `rationale` field in the requirement file.
`EXAMPLE-0001: A parent is required for a lower level requirement!` | `doorstop link EXAMPLE-0001 PARENT-####`<br>Or manually update the `links` field in the requirement's `.yml`.
`EXAMPLE-0001: suspect link` | Set the suspect link to `null` in the requirement's `.yml`
`EXAMPLE-0001: unreviewed changes` | `doorstop review EXAMPLE-0001`.<br>Use `all` for resolving all reviews.
`WARNING: no item with UID: EXAMPLE-0001` | This can happen if `active:false` in `EXAMPLE-0001.yml`.

## How to Export Requirements

You may be more comfortable with viewing requirements in an Excel spreadsheet.

The `build` script should produce a `reqs/csv_files` directory.

You can also run `doorstop export REQ path/to/tst.xlsx` (also supports tsv, csv, or yml), or similarly call it for any other requirement category.

## How to Add a Requirement Category

A requirement category can be added with `doorstop create`:

```bash
# doorstop create <category name> <path> --parent REQ
$ doorstop create PWR ./HW/PWR --parent HW
building tree...
created document: PWR (@/reqs/HW/PWR)
```

You will see that a new directory was created and populated with a `.doorstop.yml` file:
```yaml
settings:
  digits: 3
  parent: HW
  prefix: PWR
  sep: ''
```

We have specific fields for this project. All `.doorstop.yml` files not following the project standard will be rectified when the `build` script is called.

Output after `./build`:

```yaml
attributes:
  publish:
  - verified-by
  - type
  - rationale
settings:
  digits: 4
  parent: HW
  prefix: PWR
  sep: '-'
```

If we build now, we will get a warning: `PWR: no items`.

## How to Add a Requirement

Requirements can be added with `doorstop add`:

```bash
# doorstop add <category>
$ doorstop add PWR
building tree...
added item: PWR-0001 (@/reqs/HW/PWR/PWR-0001.yml)
```
The new file can be manually populated with the required fields.

You must then link the requirement to a parent requirement before the build can succeed:

`doorstop link PWR-0001 HW-####`

You can add multiple requirements add the same time with the `-c` option:

```bash
$ doorstop add PWR -c 3
building tree...
added item: PWR-0002 (@/reqs/HW/PWR/PWR-0002.yml)
added item: PWR-0003 (@/reqs/HW/PWR/PWR-0003.yml)
added item: PWR-0004 (@/reqs/HW/PWR/PWR-0004.yml)
```

## How to View Requirements

To view the requirements outside of source code, do one of the following:
1) `doorstop-server`
    - Visit `localhost:7867` in your browser
2) `cd public/; python -m http.server PORT` 
    - Visit `localhost:PORT` in your browser
3) `doorstop-gui`
    - tkinter application
4) TODO: Visit arrowair.com arrowdrone subdir
5) Open the csv file(s) in Excel.