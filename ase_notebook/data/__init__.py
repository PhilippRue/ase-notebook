"""Module for storing and loading data files."""
import json
from pathlib import Path

from ase_notebook import data
from ase_notebook.atoms_convert import deserialize_atoms


def load_data_file(name: str, load_json: bool = True, as_binary: bool = False):
    """Load a package resource from the package's data folder.

    Parameters
    ----------
    name : str
        Name of the resource file.
    load_json : bool, optional
        If True, load the resource as JSON and return the deserialized object.
        If False, return the raw string.
    as_binary : bool, optional
        If True, return the resource as bytes.
        If False, return the resource as string.

    Returns
    -------
    str or bytes or object
        The resource as string, bytes, or deserialized JSON object.
    """
    path_module = Path(data.__file__).parents[0]
    path_resource = path_module / name
    if as_binary:
        return path_resource.read_bytes()
    string = path_resource.read_text()

    if load_json and name.endswith(".json"):
        return json.loads(string)
    return string

    # DEV note:
    # In case this way of accessing package resources (via __file__) is problematic (e.g. in scripts),
    # replace with importlib methods from Python STL. To ensure Python version compatibility,
    # use try-except approach on AttributeError.
    #
    # - Use package = data, resource = name.
    # - try (Python >= 3.11): use replacements to to read_text, read_binary.
    #   - https://docs.python.org/3.11/library/importlib.resources.html#deprecated-functions
    # - except AE (Python >= 3.9): use read_text, read_binary.
    #   - https://docs.python.org/3.10/library/importlib.html#module-importlib.resources
    # - except AE (Python < 3.9): use find_spec to replace .__file__, then Path.read_text, Path.read_binary.
    #   - https://docs.python.org/3.6/library/importlib.html


def get_example_atoms(name="pyrite"):
    """Load an example ase.Atoms instance."""
    data = load_data_file(f"example_{name}.atoms.json", load_json=False)
    return deserialize_atoms(data)
