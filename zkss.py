import os
import re
import sys

from rich.console import Console
from rich import print
from settings import ZK_BASE_DIR, ENDING

SPLIT_CHARACTERS = "[ \.,\[\]\(\)\n]"


def strip_ending(filename):
    return re.search(rf"(.*){ENDING}$", filename).group(1)


file_and_folder_names = os.listdir(ZK_BASE_DIR)


files_with_last_access_time = {
    f"{filename}": os.lstat(os.path.join(ZK_BASE_DIR, filename)).st_atime
    for filename in file_and_folder_names
    if os.path.isfile(os.path.join(ZK_BASE_DIR, filename))
    and filename[-3:] == ENDING  # filenames only, no foldernames
}

filenames_sorted = list(
    dict(
        sorted(
            files_with_last_access_time.items(), key=lambda item: item[1], reverse=True
        )
    )
)

console = Console()
with console.pager(styles=True):

    if len(sys.argv) > 1:
        search_string = " ".join(sys.argv[1:])
        len_search_string = len(search_string.split(" "))
    else:
        print("[red]No search string given.")
        sys.exit()

    print_heading = True
    for filename in filenames_sorted:
        try:
            stripped_filename = re.search(
                r"^[0-9]* (.*)", strip_ending(filename.lower())
            ).group(1)
        except:
            stripped_filename = ""

        if search_string.lower() == stripped_filename:
            if print_heading:
                console.print(
                    f'- "{search_string.lower()}" very exact in [yellow]filename:'
                )
                print_heading = False
            console.print("    " + strip_ending(filename))
            filenames_sorted.remove(filename)

    print_heading = True
    for filename in filenames_sorted:
        if search_string.lower() in set(re.split(SPLIT_CHARACTERS, filename.lower())):
            if print_heading:
                console.print(f'- "{search_string.lower()}" exact in [yellow]filename:')
                print_heading = False
            console.print("    " + strip_ending(filename))
            filenames_sorted.remove(filename)

    print_heading = True
    for filename in filenames_sorted:
        if search_string.lower() in filename.lower():
            if print_heading:
                console.print(f'- "{search_string.lower()}" in [yellow]filename:')
                print_heading = False
            console.print("    " + strip_ending(filename))
            filenames_sorted.remove(filename)

    if len_search_string > 1:

        message = ""
        search_words = search_string.lower().split(" ")
        i = 1
        for s in search_words:
            message += f'"{s}"'
            if i < len(search_words):
                message += " and "
            i += 1

        print_heading = True
        for filename in filenames_sorted:
            hit_count = 0
            for search_word in search_string.lower().split():
                if search_word in filename.lower():
                    hit_count += 1
            if hit_count == len_search_string:
                if print_heading:
                    console.print(f"- {message} in [yellow]filename:")
                    print_heading = False
                console.print("    " + strip_ending(filename))
                filenames_sorted.remove(filename)

    print_heading = True
    for filename in filenames_sorted:
        with open(os.path.join(ZK_BASE_DIR, filename), "r") as f:
            content = f.read().lower()
            if search_string.lower() in set(re.split(SPLIT_CHARACTERS, content)):
                if print_heading:
                    console.print(
                        f'- "{search_string.lower()}" exact in [yellow]content:'
                    )
                    print_heading = False
                console.print("    " + strip_ending(filename))
                filenames_sorted.remove(filename)

    print_heading = True
    for filename in filenames_sorted:
        with open(os.path.join(ZK_BASE_DIR, filename), "r") as f:
            content = f.read().lower()
            if search_string.lower() in content:
                if print_heading:
                    console.print(f'- "{search_string.lower()}" in [yellow]content:')
                    print_heading = False
                console.print("    " + strip_ending(filename))
                filenames_sorted.remove(filename)

    if len_search_string > 1:
        print_heading = True
        for filename in filenames_sorted:
            hit_count = 0
            with open(os.path.join(ZK_BASE_DIR, filename), "r") as f:
                content = f.read().lower()
                for search_word in set(re.split(SPLIT_CHARACTERS, content)):
                    if search_word in content:
                        hit_count += 1
                if hit_count == len_search_string:
                    if print_heading:
                        console.print(f"- {message} exact in [yellow]content:")
                        print_heading = False
                    console.print("    " + strip_ending(filename))
                    filenames_sorted.remove(filename)

    if len_search_string > 1:
        print_heading = True
        for filename in filenames_sorted:
            hit_count = 0
            with open(os.path.join(ZK_BASE_DIR, filename), "r") as f:
                content = f.read().lower()
                for search_word in search_string.lower().split(" "):
                    if search_word in content:
                        hit_count += 1
                if hit_count == len_search_string:
                    if print_heading:
                        console.print(f"- {message} in [yellow]content:")
                        print_heading = False
                    console.print("    " + strip_ending(filename))
                    filenames_sorted.remove(filename)
