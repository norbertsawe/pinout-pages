# pinout-pages

The shared electronic component database for
[pinout-cli](https://github.com/norbertsawe/pinout-cli): **88 components and 1,315 pins**,
with package-specific pin maps, electrical notes, alternate functions and source
references.

Browse the [complete catalog](CATALOG.md).

## Database layout

| File | Contents |
| --- | --- |
| [microcontrollers.json](database/microcontrollers.json) | Bare MCU packages and physical pad numbers |
| [boards.json](database/boards.json) | Development-board headers and reference revisions |
| [analog.json](database/analog.json) | Timers, amplifiers, converters, comparators and regulators |
| [digital.json](database/digital.json) | Logic, interfaces, expanders, memory and drivers |
| [connectors.json](database/connectors.json) | USB, GPIO and programming/debug connectors |
| [discrete_sensors.json](database/discrete_sensors.json) | Transistors, power parts and sensors |

Each JSON file maps component IDs to structured definitions. Records identify the
package, supply limits, pin orientation and sources. Pins include descriptions,
semantic types, optional functions and voltage notes. Clean `ascii_art` remains
available for older CLI versions.

The CLI bundles a validated snapshot for offline use. Run `pinout --update` to
refresh its cached definitions from this repository.

## Validation

```sh
python -m pip install jsonschema
python tools/validate_database.py
```

The validator checks the [schema](schema/component.schema.json), duplicate keys
and IDs, alias conflicts, pin numbers and layout coverage. CI runs it on every
push and pull request. With the CLI installed, `pinout --validate database` also
validates the catalog.

## Contributing

Use a distinct ID for each package or board revision. Verify pins against a
manufacturer datasheet or board schematic, include the source, and describe the
viewing orientation. Document reserved pins, boot straps and voltage limits;
keep operating recommendations separate from absolute maximum ratings.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution and snapshot workflow,
and the CLI's [database guide](https://github.com/norbertsawe/pinout-cli/blob/main/docs/database.md)
for examples and layout conventions.
