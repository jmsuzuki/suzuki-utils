import inspect
import sys
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Type, List, Tuple, Dict


def dynamic_nested_import(file_from_package: str, file_name_from_package: str, type_to_import: Type, exclude_classes: List[Tuple] = None,
                   exclude_modules: List[str] = None) -> Dict:
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

    package_dir = Path(file_from_package).resolve().parent
    registrations = {}

    # Helper function to traverse directories recursively
    def search_modules(package_name, package_path):
        for module_info in iter_modules([str(package_path)]):
            if module_info.name in exclude_modules:
                continue

            module_to_import = f"{package_name}.{module_info.name}"
            module = import_module(module_to_import)

            # Recursively check submodules/packages
            if module_info.ispkg:
                sub_package_path = package_path / module_info.name
                search_modules(module_to_import, sub_package_path)
            else:
                # Inspect classes within the module
                class_members = inspect.getmembers(
                    sys.modules[module_to_import],
                    lambda member: inspect.isclass(member)
                                   and member != type_to_import
                                   and not inspect.isabstract(member)
                                   and issubclass(member, type_to_import)
                )

                # Add valid classes to the registrations dictionary
                for class_name, class_obj in class_members:
                    if class_obj not in exclude_classes and not any(issubclass(cls, class_obj) for cls in exclude_classes):
                        registrations[class_name] = class_obj

    # Start searching from the root module
    search_modules(file_name_from_package, package_dir)

    return registrations


