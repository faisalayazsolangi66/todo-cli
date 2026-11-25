# todo-cli

A simple to-do list manager stored in a JSON file.

Tasks are stored in `~/.local/share/todo-cli/todos.json` by default;
use `--file` to choose a different location.

## Requirements

- Python 3
- No third-party packages

## How to run

```bash
python3 main.py [--file todos.json] add "Buy milk" [--due 2026-11-30]
python3 main.py list [--all]
python3 main.py done 1
python3 main.py delete 1
python3 main.py clear
```

## Example

```bash
python3 main.py --file /tmp/todos.json add "Write report" --due 2026-11-30
python3 main.py --file /tmp/todos.json list
```

Sample output:

```
Added #1: Write report
  1. [ ] Write report (due 2026-11-30)
1 pending, 0 done.
```

## License

MIT — see `LICENSE`.
