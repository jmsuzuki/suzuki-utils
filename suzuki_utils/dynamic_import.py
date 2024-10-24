import sys
import inspect
from pathlib import Path
from typing import Type, List, Tuple, Dict
from pkgutil import iter_modules
from importlib import import_module


def dynamic_import(file_from_package: str, file_name_from_package: str, type_to_import: Type, exclude_classes: List[Tuple] = None, exclude_modules: List[str] = None) -> Dict:
    """
    Dynamically Import Classes by searching for classes recursively starting at the file_from_package directory

    :param file_from_package: __file__ from within the __init__.py python package directory
    :param file_name_from_package: __name__ from within the __init__.py python package directory
    :param type_to_import: the type to dynamically import.
    :param exclude_classes: list of classes to exclude from importing
    :param exclude_modules: list of module to exclude from importing.
                            if the package contains a factory, exclude modules will typically contain the 'factory'
    :return: dynamically import classes / registrations
    """
    if not exclude_classes:
        exclude_classes = []

    if not exclude_modules:
        exclude_modules = []

    package_dir = str(Path(file_from_package).resolve().parent)

    registrations = {}

    for (_, module_name, _) in iter_modules([package_dir]):
        if module_name in exclude_modules:
            continue

        module_to_import = f"{file_name_from_package}.{module_name}"

        module = import_module(module_to_import)
        class_members = inspect.getmembers(
            sys.modules[module_to_import],
            lambda member: inspect.isclass(member)
                           and member != type_to_import
                           and not inspect.isabstract(member)
                           and issubclass(member, type_to_import)
        )

        if class_members and len(class_members) == 1:
            skip = False
            for exclude_class in exclude_classes:
                if exclude_class == class_members[0][1]:
                    skip = True
                    break

                class_bases = class_members[0][1].__bases__
                if exclude_class in class_bases:
                    skip = True
                    break

            if not skip:
                registrations[class_members[0][0]] = class_members[0][1]

    return registrations


