import importlib
import os
import sys

from bmipy import Bmi


ENV_BMI_MODULE = "BMI_MODULE"
ENV_BMI_CLASS = "BMI_CLASS"


def from_env() -> Bmi:
    """
    Build and return an instance of a BMI implementation based on the environment variables.

    The following environment variables are used:
    - BMI_PATH: The path to the BMI implementation module. If provided, the path will be added to the system path.
    - BMI_MODULE: The name of the BMI implementation module.
    - BMI_CLASS: The name of the BMI implementation class.

    Returns:
        object: An instance of a BMI implementation.

    Raises:
        ValueError: If the BMI implementation class or module name is missing.
    """
    path = os.environ.get("BMI_PATH", None)
    module_name = os.environ.get(ENV_BMI_MODULE, "")
    if not module_name:
        raise ValueError("Missing module name: module could not be derived from environment "
                         "variable %s" % (ENV_BMI_MODULE))

    class_name = os.environ.get(ENV_BMI_CLASS, "")
    if not class_name:
        raise ValueError("Missing bmi implementation: class could not be derived from environment"
                         "variable %s" % (ENV_BMI_CLASS))

    return build(module_name, class_name, path)

def build(module_name: str, class_name: str, path=None) -> Bmi:
    """
    Build and return an instance of a BMI implementation based on the provided module and class names.

    Args:
        module_name: The name of the BMI implementation module.
        class_name: The name of the BMI implementation class.
        path: The path to the BMI implementation module. If provided, the path will be added to the system path.

    Returns:
        object: An instance of a BMI implementation.
    """
    if path is not None:
        sys.path.append(path)
    class_ = getattr(importlib.import_module(module_name), class_name)
    return class_()