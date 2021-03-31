import pathlib
import os
from typing import Generator


class Path(pathlib.Path):
    """
    A pathlib.Path child class that allows concatenation with strings
    by overloading the addition operator.

    In addition, it implements the ``startswith`` and ``endswith`` methods
    just like in the base :obj:`str` type.

    The ``replace_`` implementation is meant to be an implementation closer
    to the :obj:`str` type.

    Iterating over a directory with ``iterdir`` that does not exists
    will return an empty iterator instead of throwing an error.

    Creating a directory with ``mkdir`` allows existing directory and
    creates parents by default.
    """

    _flavour = (
        pathlib._windows_flavour  # type: ignore[attr-defined]  # pylint: disable=W0212
        if os.name == "nt"
        else pathlib._posix_flavour  # type: ignore[attr-defined]  # pylint: disable=W0212
    )

    def __add__(self, string: str) -> Path:
        return Path(str(self) + string)

    def startswith(self, string: str) -> bool:
        return str(self).startswith(string)

    def endswith(self, string: str) -> bool:
        return str(self).endswith(string)

    def replace_(self, patt: str, repl: str) -> Path:
        return Path(str(self).replace(patt, repl))

    def iterdir(self) -> Generator:
        if self.exists():
            return pathlib.Path(str(self)).iterdir()
        # for x in []:  # type: ignore[var-annotated]
        #     yield x
        return iter([])

    def mkdir(
        self, mode=0o777, parents: bool = True, exist_ok: bool = True
    ) -> Path:
        super().mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
        return self