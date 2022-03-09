import cmd
import shlex
import functools
import importlib
import inspect
from pynames import GENDER, LANGUAGE
import pynames.generators


def catch_exception(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except RuntimeError as err:
            print(f"ERROR: {err}")
            return None
        except (ModuleNotFoundError, ValueError):
            print("Incorrect arguments. Please, consult 'help'")
            return None
        except KeyError as err:
            print("Incorrect arguments. Please, consult 'help'")
            return None
    return func


class Names:
    def __init__(self):
        self.default_language = LANGUAGE.NATIVE
        self.module_names, _ = zip(*filter(lambda x: inspect.ismodule(x[1]) and
                    x[1].__name__.startswith("pynames.generators") and x[0] != "module",
                    inspect.getmembers(pynames.generators)))

    def language(self, args):
        if len(args) < 1:
            raise RuntimeError("'language' command called without arguments")
        if len(args) > 1:
            raise RuntimeError("too many arguments")
        self.default_language = LANGUAGE.__dict__[args[0].upper()]

    def complete_language(self, text, line, begidx, endidx):
        args = filter(lambda y: not y.startswith("__"),
                    map(lambda x: x[0], inspect.getmembers(LANGUAGE)))

        if len(shlex.split(line)) - int(not not text) > 1:
            return []

        if not text:
            return list(args)
        return list(filter(lambda z: z.startswith(text.upper()), args))

    def generate_parser(self, chain):
        if len(chain) < 1:
            raise RuntimeError("'generate' command called without arguments")

        ret = dict()
        old_token, token = None, chain.pop(0)
        subclass_names,subclasses = None, None
        genders = ["female", "male"]

        while True:
            if old_token == None:
                if token not in self.module_names:
                    raise RuntimeError(f"Incorrect argument '{token}'")
                subclass_names,subclasses = self.__get_classes(token)
                subclass_names = self.__trim(subclass_names)
                ret["subclass"] = subclasses[0]

            elif old_token in self.module_names:
                if token in genders:
                    ret["gender"] = GENDER.MALE if token == "male" else GENDER.FEMALE
                elif token in subclass_names and len(subclass_names) > 1:
                    ret["subclass"] = subclasses[subclass_names.index(token)]
                elif token in subclass_names and len(subclass_names) == 1:
                    raise RuntimeError(f"Incorrect argument '{token}'")
                else:
                    raise RuntimeError(f"Incorrect argument '{token}'")

            elif old_token in subclass_names:
                if token in genders:
                    ret["gender"] = GENDER.MALE if token == "male" else GENDER.FEMALE
                else:
                    raise RuntimeError(f"Incorrect argument '{token}'")

            elif old_token in genders:
                raise RuntimeError("Too many arguments")

            if len(chain) == 0:
                break
            old_token, token = token, chain.pop(0)
        return ret

    def generate(self, args):
        generator = args["subclass"]()
        if "gender" in args:
            gender = args["gender"]
        else:
            gender = GENDER.MALE

        if self.default_language == LANGUAGE.ALL:
            name = generator.get_name(genders=[gender])
            for lang in generator.languages:
                print(name.get_for(gender, lang))
        else:
            if self.default_language not in generator.languages:
                print(generator.get_name_simple(gender, LANGUAGE.NATIVE))
            else:
                print(generator.get_name_simple(gender, self.default_language))

    def complete_generate(self, text, line, begidx, endidx):
        return self.__complete_info_gen(text, line, ["male", "female"])

    def info_parser(self, chain):
        if len(chain) < 1:
            raise RuntimeError("'info' command called without arguments")

        ret = dict()
        old_token, token = None, chain.pop(0)
        subclass_names,subclasses = None, None
        genders = ["female", "male"]

        while True:
            if old_token == None:
                if token not in self.module_names:
                    raise RuntimeError(f"Incorrect argument '{token}'")
                subclass_names,subclasses = self.__get_classes(token)
                subclass_names = self.__trim(subclass_names)
                ret["subclass"] = subclasses[0]

            elif old_token in self.module_names:
                if token in genders:
                    ret["gender"] = GENDER.MALE if token == "male" else GENDER.FEMALE
                elif token == "language":
                    ret["language"] = True
                elif token in subclass_names and len(subclass_names) > 1:
                    ret["subclass"] = subclasses[subclass_names.index(token)]
                elif token in subclass_names and len(subclass_names) == 1:
                    raise RuntimeError(f"Incorrect argument '{token}'")
                else:
                    raise RuntimeError(f"Incorrect argument '{token}'")
            elif old_token in subclass_names:
                if token in genders:
                    ret["gender"] = GENDER.MALE if token == "male" else GENDER.FEMALE
                elif token == "language":
                    ret["language"] = True
                else:
                    raise RuntimeError(f"Incorrect argument '{token}'")
            elif old_token in genders:
                raise RuntimeError("Too many arguments")
            elif old_token == "language":
                raise RuntimeError("Too many arguments")

            if len(chain) == 0:
                break
            old_token, token = token, chain.pop(0)
        return ret

    def info(self, args):
        generator = args["subclass"]()
        if "language" not in args:
            if "gender" in args:
                print(generator.get_names_number(args["gender"]))
            else:
                print(generator.get_names_number())
        else:
            print(*generator.languages)

    def complete_info(self, text, line, begidx, endidx):
        return self.__complete_info_gen(text, line, ["male", "female", "language"])

    def __complete_info_gen(self, text, line, case_args):
        def third_case(text):
            args = case_args
            if not text:
                return args
            return list(filter(lambda x: x.startswith(text), args))

        text = text.lower()
        split = shlex.split(line)
        c = len(split) - int(not not text)
        if c == 1:
            if not text:
                return list(self.module_names)
            return list(filter(lambda z: z.startswith(text), self.module_names))
        elif c == 2:
            class_name = shlex.split(line)[-1 - int(not not text)]
            subclasses, _ = self.__get_classes(class_name)

            if len(subclasses) < 2:
                return third_case(text)

            subclasses_trunc = self.__trim(subclasses)

            if not text:
                return list(subclasses_trunc)
            return list(filter(lambda x: x.startswith(text), subclasses_trunc))
        elif c == 3:
            if split[2] not in case_args:
                return third_case(text)
            else:
                return []
        else:
            return []

    def __get_classes(self, module_name):
        module = importlib.import_module("pynames.generators." + module_name)
        return zip(*
                filter(lambda t: inspect.isclass(t[1]) and t[1].__module__ == module.__name__,
                inspect.getmembers(module)))

    def __trim(self, args):
        return tuple(x.lower().replace("generator", "").replace("names", "").replace("fullname", "")
                for x in args)


class NameShell(cmd.Cmd):
    intro = 'Welcome to the name generator. Type help or ? to list commands.\n'
    prompt = '$ '
    file = None

    def __init__(self):
        super().__init__()
        self.names = Names()
        self.complete_language = self.names.complete_language
        self.complete_generate = self.names.complete_generate
        self.complete_info = self.names.complete_info

    @catch_exception
    def do_language(self, arg):
        "Set output language.\nSyntax: language arg"
        self.names.language(shlex.split(arg.lower()))

    @catch_exception
    def do_generate(self, arg):
        "Generate a name.\nSyntax: 'generate race [subclass] [gender]'"
        self.names.generate(self.names.generate_parser(shlex.split(arg.lower())))

    @catch_exception
    def do_info(self, arg):
        "Get info on the amount of names and available languages.\nSyntax: info race [subclass] [gender|language]"
        self.names.info(self.names.info_parser(shlex.split(arg.lower())))

    def do_EOF(self, arg):
        "Exit the application."
        return True


if __name__ == '__main__':
    NameShell().cmdloop()
