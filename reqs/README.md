# Requirements

## Table of Contents

- [Dependencies](#dependencies)
- [Layout](#layout)
- [Requirement Files](#requirement-files)
- [How to Validate the Requirements](#how-to-validate-the-requirements)
- [How to Export Requirements](#how-to-export-requirements)

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
- Project directives: `PROJ/`

An example layout of requirements is below.
```tree
.
├── build
├── REQ-0001.yml
├── PROJ
│   └── PROJ-0001.yml
├── HW
│   └── FLIGHT
│       └── FLIGHT-0001.yml
└── SW
    ├── CMD
    │   ├── CMD-0001.yml
    ├── HEALTH
    │   ├── HEALTH-0001.yml
    └── TLM
        ├── TLM-0001.yml
```

## Requirement Files

The requirements are individual `.yml` files. Each contains the requirement's primary text as well as metadata.

```yml
# reqs/SW/HEALTH/HEALTH-0001.yml
active: true
derived: false
header: ''
level: 1.0
links:
- REQ-0001: bBkf6YMFHFULHe5eLcjSBipaMvJL7t5BdNTRJdS-4Ug=
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
`links` | Links to parent requirements. In this case REQ-0001 (*The platform shall maintain the health status of each device*) is the parent requirement. **All lower level requirements must have a parent.** This is enforced with the `build` script.
`active` | If the requirement is in draft and you don't want to cause build errors, set this to `false`.


## How to Validate the Requirements

Use the `reqs/build` script.

`reqs/build` will call:
- `doorstop_hooks.py` (a wrapper around `doorstop` with extra rules)
- `doorstop publish all public/`
- `doorstop export REQ ./requirements.xlsx`

An ideal build will look like so:

```zsh
➜  reqs git:(main) ✗ ./build
building tree...
loading documents...
publishing tree to '/home/ams/gitprojects/arrowdrone-docs/reqs/REQ'...
published: /home/ams/gitprojects/arrowdrone-docs/reqs/REQ
building tree...
exporting document REQ to './requirements.xlsx'...
exported: ./requirements.xlsx
```

Common errors and their fixes:

Common Error | Fix
--- | ---
`EXAMPLE-0001: Rationale is required!` | Populate a `rationale` field in the requirement file.
`EXAMPLE-0001: A parent is required for a lower level requirement!` | `doorstop link EXAMPLE-0001 PARENT-0001`<br>Or manually update the `links` field for the req.
`EXAMPLE-0001: suspect link` | `doorstop clear EXAMPLE-0001`.<br>Use `all` resolving all suspect links. This occurs sometimes when the parent requirement changes.
`EXAMPLE-0001: unreviewed changes` | `doorstop review EXAMPLE-0001`.<br>Use `all` for resolving all reviews.

## How to Export Requirements

You may be more comfortable with viewing requirements in an Excel spreadsheet.

The `build` script should produce a `requirements.xlsx` file.

You can also run `doorstop export REQ path/to/tst.xlsx` (also supports tsv, csv, or yml).

## How to Add a Requirement Category

A requirement category can be added with `doorstop create`:

```bash
# doorstop create <category name> <path> --parent REQ
$ doorstop create PWR ./HW/PWR --parent REQ
building tree...
created document: PWR (@/reqs/HW/PWR)
```

You will see that a new directory was created and populated with a `.doorstop.yml` file:


If we build now, we will get a warning: `PWR: no items`.

## How to Add a Requirement

Requirements can be added with `doorstop add`:

```bash
# doorstop add <category>
$ doorstop add PWR
building tree...
created document: PWR (@/reqs/HW/PWR)
```