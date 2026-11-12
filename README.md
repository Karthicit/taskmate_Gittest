# TaskMate
highway to hell
A tiny command-line task manager. Pure Python (3.8+), zero dependencies.
It exists so you have a *real* codebase to practice Git and GitHub on.

## Run it

```bash
python -m taskmate add "Learn git" --priority high --due 2026-12-01
python -m taskmate list
python -m taskmate done 1
python -m taskmate search git
python -m taskmate delete 1
```

Use a throwaway data file while practicing:

```bash
python -m taskmate --file sample_tasks.json list
```

## Run the tests

```bash
python -m unittest -v
```

## Project layout

```
taskmate/
  models.py     Task dataclass + validation
  storage.py    JSON file read/write
  service.py    business logic (add, complete, delete, search)
  cli.py        argparse command-line interface
tests/          unittest test suite
docs/BACKLOG.md ideas to build on feature branches
```
