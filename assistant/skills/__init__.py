import importlib
import pkgutil
from types import ModuleType

skill_registry = {}

def load_all_skills():
    package = __package__  # 'assistant.skills'

    for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
        full_module_name = f"{package}.{module_name}"
        module: ModuleType = importlib.import_module(full_module_name)

        for attr in dir(module):
            obj = getattr(module, attr)
            if callable(obj) and hasattr(obj, "__is_skill__"):
                skill_registry[obj.__name__] = obj


load_all_skills()
