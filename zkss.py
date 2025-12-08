import os
import re
import sys
from typing import List, Callable, Optional

from rich.console import Console
from rich import print
from settings import ZK_BASE_DIR, ENDING


class ZKSearcher:
    SPLIT_CHARACTERS = "[ \.,\[\]\(\)\n]"

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
            def check_very_exact(filename):
                try:
                    stripped = self.strip_ending(filename.lower())
                    # Strip leading numbers for "very exact" match logic from original code
                    # Original: re.search(r"^[0-9]* (.*)", strip_ending(filename.lower())).group(1)
                    match = re.search(r"^[0-9]* (.*)", stripped)
                    cleaned_name = match.group(1) if match else stripped
                    return search_string_lower == cleaned_name
                except Exception:
                    return False

            filenames = self.filter_and_print(
                filenames,
                check_very_exact,
                f'- "{search_string_lower}" very exact in [yellow]filename:',
            )

            # 2. Exact Word in Filename
            def check_exact_filename(filename):
                return search_string_lower in set(re.split(self.SPLIT_CHARACTERS, filename.lower()))

            filenames = self.filter_and_print(
                filenames,
                check_exact_filename,
                f'- "{search_string_lower}" exact in [yellow]filename:',
            )

            # 3. Substring in Filename
            def check_substring_filename(filename):
                return search_string_lower in filename.lower()

            filenames = self.filter_and_print(
                filenames,
                check_substring_filename,
                f'- "{search_string_lower}" in [yellow]filename:',
            )

            # 4. Multi-word in Filename
            if len_search_string > 1:
                def check_multi_filename(filename):
                    return all(word in filename.lower() for word in search_words)

                filenames = self.filter_and_print(
                    filenames,
                    check_multi_filename,
                    f"- {message} in [yellow]filename:",
                )

            # Content Searches
            # Optimization: Read content once per file if possible, but the list shrinks.
            # Since we have to iterate the remaining files for each check, we might read the same file multiple times 
            # if it fails the first content check but passes a later one.
            # To avoid re-reading, we could cache content, but that might be memory intensive.
            # Given the original script read it every time, we'll stick to that or slightly optimize.
            # The original script did: loop 5, loop 6, loop 7, loop 8.
            # If a file matches in loop 5, it's removed.
            
            # 5. Exact Word in Content
            def check_exact_content(filename):
                content = self.get_file_content(filename)
                return search_string_lower in set(re.split(self.SPLIT_CHARACTERS, content))

            filenames = self.filter_and_print(
                filenames,
                check_exact_content,
                f'- "{search_string_lower}" exact in [yellow]content:',
            )

            # 6. Substring in Content
            def check_substring_content(filename):
                content = self.get_file_content(filename)
                return search_string_lower in content

            filenames = self.filter_and_print(
                filenames,
                check_substring_content,
                f'- "{search_string_lower}" in [yellow]content:',
            )

            if len_search_string > 1:
                # 7. Multi-word Exact in Content
                def check_multi_exact_content(filename):
                    content = self.get_file_content(filename)
                    content_words = set(re.split(self.SPLIT_CHARACTERS, content))
                    return all(word in content_words for word in search_words)

                filenames = self.filter_and_print(
                    filenames,
                    check_multi_exact_content,
                    f"- {message} exact in [yellow]content:",
                )

                # 8. Multi-word in Content
                def check_multi_content(filename):
                    content = self.get_file_content(filename)
                    return all(word in content for word in search_words)

                filenames = self.filter_and_print(
                    filenames,
                    check_multi_content,
                    f"- {message} in [yellow]content:",
                )


if __name__ == "__main__":
    searcher = ZKSearcher()
    searcher.run()
