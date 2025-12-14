import os
import re
import sys
from typing import List, Callable, Optional

from rich.console import Console
from rich import print
from settings import ZK_BASE_DIR, ENDING


class ZKSearcher:
    SPLIT_CHARACTERS = r"[ \.,\[\]\(\)\n]"

    def __init__(self, base_dir: str = ZK_BASE_DIR, ending: str = ENDING):
        self.base_dir = base_dir
        self.ending = ending
        self.console = Console()

    def strip_ending(self, filename: str) -> str:
        """Removes the file extension from the filename."""
        match = re.search(rf"(.*){self.ending}$", filename)
        if match:
            return match.group(1)
        return filename

    def get_sorted_filenames(self) -> List[str]:
        """Returns a list of filenames sorted by last access time (descending)."""
        try:
            file_and_folder_names = os.listdir(self.base_dir)
        except FileNotFoundError:
            self.console.print(f"[red]Directory not found: {self.base_dir}[/red]")
            return []

        files_with_last_access_time = {
            filename: os.lstat(os.path.join(self.base_dir, filename)).st_atime
            for filename in file_and_folder_names
            if os.path.isfile(os.path.join(self.base_dir, filename))
            and filename.endswith(self.ending)
        }

        return sorted(
            files_with_last_access_time.keys(),
            key=lambda f: files_with_last_access_time[f],
            reverse=True,
        )

    def filter_and_print(
        self,
        filenames: List[str],
        predicate: Callable[[str], bool],
        header_message: str,
    ) -> List[str]:
        """
        Filters filenames based on a predicate, prints matches, and returns remaining files.
        """
        matches = []
        remaining = []
        print_heading = True

        for filename in filenames:
            if predicate(filename):
                matches.append(filename)
                if print_heading:
                    self.console.print(header_message)
                    print_heading = False
                self.console.print("    " + self.strip_ending(filename))
            else:
                remaining.append(filename)
        
        return remaining

    def get_file_content(self, filename: str) -> str:
        try:
            with open(os.path.join(self.base_dir, filename), "r", errors="ignore") as f:
                return f.read().lower()
        except Exception:
            return ""

    # --- Search Predicates ---

    def check_very_exact(self, filename: str, search_string_lower: str) -> bool:
        """Checks if filename (minus ID) exactly matches search string."""
        try:
            stripped = self.strip_ending(filename.lower())
            match = re.search(r"^[0-9]* (.*)", stripped)
            cleaned_name = match.group(1) if match else stripped
            return search_string_lower == cleaned_name
        except Exception:
            return False

    def check_exact_filename(self, filename: str, search_string_lower: str) -> bool:
        """Checks if search string is an exact word in filename."""
        return search_string_lower in set(re.split(self.SPLIT_CHARACTERS, filename.lower()))

    def check_substring_filename(self, filename: str, search_string_lower: str) -> bool:
        """Checks if search string is a substring of filename."""
        return search_string_lower in filename.lower()

    def check_multi_filename(self, filename: str, search_words: List[str]) -> bool:
        """Checks if all search words are present in filename."""
        return all(word in filename.lower() for word in search_words)

    def check_exact_content(self, filename: str, search_string_lower: str) -> bool:
        """Checks if search string is an exact word in content."""
        content = self.get_file_content(filename)
        return search_string_lower in set(re.split(self.SPLIT_CHARACTERS, content))

    def check_substring_content(self, filename: str, search_string_lower: str) -> bool:
        """Checks if search string is a substring of content."""
        content = self.get_file_content(filename)
        return search_string_lower in content

    def check_multi_exact_content(self, filename: str, search_words: List[str]) -> bool:
        """Checks if all search words are exact words in content."""
        content = self.get_file_content(filename)
        content_words = set(re.split(self.SPLIT_CHARACTERS, content))
        return all(word in content_words for word in search_words)

    def check_multi_content(self, filename: str, search_words: List[str]) -> bool:
        """Checks if all search words are present in content."""
        content = self.get_file_content(filename)
        return all(word in content for word in search_words)

    def run(self):
        if len(sys.argv) > 1:
            search_string = " ".join(sys.argv[1:])
        else:
            print("[red]No search string given.")
            sys.exit()

        search_string_lower = search_string.lower()
        search_words = search_string_lower.split()
        len_search_string = len(search_words)
        
        # Format message for multi-word search
        message = ""
        if len_search_string > 1:
             message = " and ".join([f'"{s}"' for s in search_words])

        filenames = self.get_sorted_filenames()

        with self.console.pager(styles=True):
            # 1. Very Exact Filename
            filenames = self.filter_and_print(
                filenames,
                lambda f: self.check_very_exact(f, search_string_lower),
                f'- "{search_string_lower}" very exact in [yellow]filename:',
            )

            # 2. Exact Word in Filename
            filenames = self.filter_and_print(
                filenames,
                lambda f: self.check_exact_filename(f, search_string_lower),
                f'- "{search_string_lower}" exact in [yellow]filename:',
            )

            # 3. Substring in Filename
            filenames = self.filter_and_print(
                filenames,
                lambda f: self.check_substring_filename(f, search_string_lower),
                f'- "{search_string_lower}" in [yellow]filename:',
            )

            # 4. Multi-word in Filename
            if len_search_string > 1:
                filenames = self.filter_and_print(
                    filenames,
                    lambda f: self.check_multi_filename(f, search_words),
                    f"- {message} in [yellow]filename:",
                )

            # Content Searches
            # 5. Exact Word in Content
            filenames = self.filter_and_print(
                filenames,
                lambda f: self.check_exact_content(f, search_string_lower),
                f'- "{search_string_lower}" exact in [yellow]content:',
            )

            # 6. Substring in Content
            filenames = self.filter_and_print(
                filenames,
                lambda f: self.check_substring_content(f, search_string_lower),
                f'- "{search_string_lower}" in [yellow]content:',
            )

            if len_search_string > 1:
                # 7. Multi-word Exact in Content
                filenames = self.filter_and_print(
                    filenames,
                    lambda f: self.check_multi_exact_content(f, search_words),
                    f"- {message} exact in [yellow]content:",
                )

                # 8. Multi-word in Content
                filenames = self.filter_and_print(
                    filenames,
                    lambda f: self.check_multi_content(f, search_words),
                    f"- {message} in [yellow]content:",
                )


if __name__ == "__main__":
    searcher = ZKSearcher()
    searcher.run()
