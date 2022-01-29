# Music ontology

## Creating the ontology

To create the ontology file from source (when not present), one should run

```bash
make ontology.owl
```

or alternatively, to recreate and overwrite the existing ontology, run

```bash
make ontology
```

Both commands can create the ontology file in the root project directory.

This command also creates a virtual environment called `venv`, activates it and installs the needed dependencies in it in case this has not been done yet. Alternatively, the virtual environment can be created manually by running `make venv` or `make dependencies` (the former is run only if the `venv` directory is not present).

## Running the tests

⚠️ **The reasoning tests require `java` to be installed.**

Running all the tests can be done by

```bash
make test
```