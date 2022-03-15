import ast
import sys
import inspect
import difflib as dl
import textwrap as tw
import importlib as il
import itertools as it


def walk(object, fullname, roster):
    for obj_name, obj in inspect.getmembers(object):
        if inspect.isclass(obj) and obj_name.startswith("__"):
            continue

        if inspect.isfunction(obj) or inspect.ismethod(obj):
            txt = inspect.getsource(obj)

            try:
                tree = ast.parse(txt)
            except IndentationError:
                txt = tw.dedent(txt)
                tree = ast.parse(txt)

            for node in ast.walk(tree):
                for attrib in ["name", "id", "arg", "attr"]:
                    if attrib in node.__dict__:
                        node.__dict__[attrib] = "_"

            roster[f"{fullname}.{obj_name}"] = ast.unparse(tree)

        if inspect.isclass(obj):
            walk(obj, f"{fullname}.{obj_name}", roster)


if __name__ == "__main__":
    roster = {}
    for module_name in sys.argv[1:]:
        module = il.import_module(module_name)
        walk(module, module_name, roster)

    for func1, func2 in it.combinations(roster.items(), 2):
        seq = dl.SequenceMatcher(None, func1[1], func2[1])

        if seq.ratio() > 0.95:
            print(f"{func1[0]} : {func2[0]}")

