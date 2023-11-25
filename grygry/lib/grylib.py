import contextlib
import sys
from pathlib import Path


class NoPatternError(ValueError):
    pass


class Grygry:
    def __init__(self, config: dict):
        self.show_unicode_error = config.get("show_unicode_error", False)
        self.sort_files = config.get("sort_files", False)
        self.context_lines = config.get("context_lines", 0)
        self.with_suffix = set(config.get("with_suffix", []))
        self.no_suffix = set(config.get("no_suffix", []))
        self.no_start_dir = config.get("no_start_dir", ["."])
        self.no_start_file = config.get("no_start_file", [".", "~"])
        self.pattern = ""
        self.path = Path()
        self.found = {}

    def search(self) -> None:
        if len(sys.argv) < 2:
            raise NoPatternError
        self.pattern = " ".join(sys.argv[1:])
        self.grep_pattern()

    def grep_pattern(self) -> None:
        if not self.pattern:
            raise NoPatternError
        self.grep_folder(Path.cwd())

    def grep_folder(self, path: Path) -> None:
        self.path = path
        for no_start in self.no_start_dir:
            if self.path.name.startswith(no_start):
                return
        sub_dirs = []
        files = []
        for path in self.path.glob("*"):
            self._list_files(path, files, sub_dirs)
        if self.sort_files:
            self._sorted_show_found_words(files)
            for path in sorted(sub_dirs):
                self.grep_folder(path)
        else:
            self._show_found_words(files)
            for path in sub_dirs:
                self.grep_folder(path)

    def _list_files(self, path: Path, files: list, sub_dirs: list) -> None:
        if path.is_dir():
            sub_dirs.append(path)
            return
        if (self.with_suffix and path.suffix not in self.with_suffix) or (
            self.no_suffix and path.suffix in self.no_suffix
        ):
            return
        for no_start in self.no_start_file:
            if path.name.startswith(no_start):
                return
        files.append(path)

    def _show_found_words(self, files: list) -> None:
        for path in files:
            self.show_find_word(path)

    def _sorted_show_found_words(self, files: list) -> None:
        for path in sorted(files):
            self.show_find_word(path)

    def show_find_word(self, path: Path) -> None:
        self.find_word(path)
        if not self.found:
            return
        self.show_found(path)

    def show_found(self, path: Path) -> None:
        print(path)
        sorted_dict = dict(sorted(self.found.items()))
        if self.context_lines:
            self._show_found_context(sorted_dict)
        else:
            self._show_found_no_context(sorted_dict)
        print()

    def _show_found_context(self, sorted_dict: dict[int, str]) -> None:
        previous = 0
        for idx, line in sorted_dict.items():
            if previous and idx > previous + 1:
                print()
            previous = idx
            print(f" {idx:4d}: {line.rstrip()}")

    def _show_found_no_context(self, sorted_dict: dict[int, str]) -> None:
        for idx, line in sorted_dict.items():
            print(f" {idx:4d}: {line.rstrip()}")

    def find_word(self, path: Path) -> None:
        # assuming reading the full file
        self.found = {}
        pattern = self.pattern
        try:
            with path.open() as file:
                content = file.readlines()
                for index, line in enumerate(content):
                    if pattern not in line:
                        continue
                    self.found[index + 1] = line
                    if not self.context_lines:
                        continue
                    for step in range(1, self.context_lines + 1):
                        with contextlib.suppress(IndexError):
                            self.found[index + 1 + step] = content[index + step]
                        with contextlib.suppress(IndexError):
                            self.found[index + 1 - step] = content[index - step]

        except UnicodeDecodeError:
            if self.show_unicode_error:
                print("Unicode error for", path)
            self.found = {}
        except OSError as e:
            print(e)
            print(path)
            self.found = {}
