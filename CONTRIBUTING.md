# Contributing

Add a component to the appropriate `database/*.json` file using the
[schema](schema/component.schema.json). Assign a new ID to each package or board
revision. MCU package numbers and development-board connector numbers must remain
separate; aliases should resolve only to the same physical layout.

Verify each pin against a manufacturer datasheet or original board schematic.
Include the source link and viewing orientation. Describe power, ground, unused
connections, boot straps and reserved flash pins. List common alternate functions
in `functions`, and state voltage tolerance explicitly. Supply recommendations
must be distinguished from absolute maximum ratings.

The catalog's IC pin facts were cross-checked with KiCad 10 symbols and manufacturer
references. Board records cite vendor or original board guides. Clone hardware
can differ from these reference layouts.

## Validate changes

```sh
python -m pip install jsonschema
python tools/validate_database.py
```

Update [CATALOG.md](CATALOG.md) when adding or renaming a component. Preserve the
clean `ascii_art` compatibility field alongside structured pins when changing a
layout. If the CLI is installed, also run `pinout --validate database`.

## Refresh the CLI snapshot

From a nearby pinout-cli checkout:

```sh
cd ../pinout-cli
python tools/sync_database.py ../pinout-pages/database
python -m pytest -q
python -m build
```

Submit the catalog change together with its CLI snapshot update. The
[database guide](https://github.com/norbertsawe/pinout-cli/blob/main/docs/database.md)
explains layouts, custom definitions and compatibility behavior.
