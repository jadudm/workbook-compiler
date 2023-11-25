

https://packaging.python.org/en/latest/tutorials/packaging-projects/

https://python-poetry.org/docs/basic-usage/

https://formulas.readthedocs.io/en/stable/doc.html#

https://pypi.org/project/xlcalculator/

https://github.com/bradbase/flyingkoala

## Testing

Run

```
poetry run pytest
```

from within `wbc``

```
coverage run -m pytest ; coverage report -m
```

```
jsonnet fixtures/workbooks/additional_ueis.jsonnet > fixtures/workbooks/au.json && poetry run wbc fixtures/workbooks/au.json fixtures/workbooks/au.xlsx 
```

### Adding packages

```
poetry add <package>
```


## Testing

Running the command line

```
poetry install ; poetry run wbc tests/fixtures/addl_ueis.jsonnet /tmp/foo.xlsx
```


## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
