#!/usr/bin/env python3
"""A simple to-do list manager stored in a JSON file."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

DEFAULT_FILE = Path.home() / ".local" / "share" / "todo-cli" / "todos.json"


def load(path):
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Error reading {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    return data if isinstance(data, list) else []


def save(path, todos):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(todos, indent=2), encoding="utf-8")


def next_id(todos):
    return max((t["id"] for t in todos), default=0) + 1


def show(todos, show_done=False):
    visible = [t for t in todos if show_done or not t["done"]]
    if not visible:
        print("No tasks." + (" (all done!)" if todos else " Add one with: add"))
        return
    for t in visible:
        mark = "[x]" if t["done"] else "[ ]"
        extra = f" (due {t['due']})" if t.get("due") else ""
        print(f"{t['id']:>3}. {mark} {t['title']}{extra}")


def main():
    parser = argparse.ArgumentParser(description="Simple to-do list manager.")
    parser.add_argument("--file", default=str(DEFAULT_FILE),
                        help="JSON file to store todos in "
                             "(default: ~/.local/share/todo-cli/todos.json)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title", help="Task description")
    p_add.add_argument("--due", default=None, help="Due date, YYYY-MM-DD")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--all", action="store_true",
                        help="Include completed tasks")

    p_done = sub.add_parser("done", help="Mark a task done")
    p_done.add_argument("id", type=int, help="Task id")

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int, help="Task id")

    sub.add_parser("clear", help="Delete all completed tasks")
    args = parser.parse_args()
    path = Path(args.file).expanduser()
    todos = load(path)

    if args.command == "add":
        if args.due:
            try:
                date.fromisoformat(args.due)
            except ValueError:
                print("Error: --due must be YYYY-MM-DD.", file=sys.stderr)
                sys.exit(1)
        task = {"id": next_id(todos), "title": args.title,
                "done": False, "due": args.due}
        todos.append(task)
        save(path, todos)
        print(f"Added #{task['id']}: {args.title}")
    elif args.command == "list":
        show(todos, args.all)
        pending = sum(1 for t in todos if not t["done"])
        print(f"{pending} pending, {len(todos) - pending} done.")
    elif args.command in ("done", "delete"):
        task = next((t for t in todos if t["id"] == args.id), None)
        if task is None:
            print(f"Error: no task #{args.id}.", file=sys.stderr)
            sys.exit(1)
        if args.command == "done":
            task["done"] = True
            save(path, todos)
            print(f"Done #{task['id']}: {task['title']}")
        else:
            todos.remove(task)
            save(path, todos)
            print(f"Deleted #{task['id']}: {task['title']}")
    elif args.command == "clear":
        before = len(todos)
        todos = [t for t in todos if not t["done"]]
        save(path, todos)
        print(f"Cleared {before - len(todos)} completed task(s).")


if __name__ == "__main__":
    main()
