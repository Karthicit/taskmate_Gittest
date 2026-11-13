"""Command-line interface:  python -m taskmate <command>"""
import argparse
import sys

from .service import TaskService
from .storage import TaskStore

print("this code is for Command line interface")

def format_task(task) -> str:
    mark = "x" if task.done else " "
    due = f" (due {task.due})" if task.due else ""
    return f"[{mark}] #{task.id} {task.title} <{task.priority}>{due}"


def build_parser():
    parser = argparse.ArgumentParser(prog="taskmate", description="Tiny task manager")
    parser.add_argument("--file", help="path to the JSON data file")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    add.add_argument("--priority", default="medium", choices=("low", "medium", "high"))
    add.add_argument("--due", help="due date, YYYY-MM-DD")

    ls = sub.add_parser("list", help="list tasks")
    ls.add_argument("--pending", action="store_true", help="hide finished tasks")

    done = sub.add_parser("done", help="mark a task as done")
    done.add_argument("id", type=int)

    rm = sub.add_parser("delete", help="delete a task")
    rm.add_argument("id", type=int)

    find = sub.add_parser("search", help="search task titles")
    find.add_argument("keyword")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    service = TaskService(TaskStore(args.file) if args.file else TaskStore())
    try:
        if args.command == "add":
            task = service.add(args.title, args.priority, args.due)
            print("added:", format_task(task))
        elif args.command == "list":
            for task in service.list_tasks(show_done=not args.pending):
                print(format_task(task))
        elif args.command == "done":
            print("done:", format_task(service.complete(args.id)))
        elif args.command == "delete":
            service.delete(args.id)
            print(f"deleted #{args.id}")
        elif args.command == "search":
            for task in service.search(args.keyword):
                print(format_task(task))
    except (KeyError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
