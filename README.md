# zk-smart-search

Tool that helps to easier find "zettels" in large zettelkastens.

## Usage (Example)

To search for zettels containing the term "my zettelkasten" (or at least "my" and "zettelkasten"), simply type `zkss my zettelkasten` in your terminal and press enter. I get the following results (shortened):


    $ zkss my zettelkasten
    - "my zettelkasten" very exact in filename:
        202204070958 my zettelkasten
    - "my zettelkasten" in filename:
        202211261148 using VS Code for my Zettelkasten
        202204161345 version control for my zettelkasten
        202204130750 my zettelkasten scripts
    - "my" and "zettelkasten" in filename:
        202301030853 using English as default makes my work with the zettelkasten more meaningful
        202212290911 write my own zettelkasten editor in Python
    - "my zettelkasten" in content:
        202203291701 Google Drive
        202203310823 zettelkasten scripts
        202203151020 zettelkasten
        202203170840 keep your zettelkasten personal
        202204031957 automate everything that can be automated
    - "my" and "zettelkasten" in content:
        202208291407 get last access time of a file with Python
        202204121937 smart search for zettelkasten

        
The results are grouped, as you can see, and sorted by `last accessed`. Every zettel occurs only once in the result list.

You can "pipe" the result to handle the output, e.g.

    $ zkss my zettelkasten | less

## Why zkss?

Software like "The Archive" sort the search results by _title_, _creation date_ or _modification date_. However, for some search terms, the more zettels you have, the more time you spend skimming the list of search results.

By structuring the search results and showing the presumably most relevant first, you should be able to save time finding the desired zettels.

## Installation

First, you need Python, of course. On a Mac, it [works best with Homebrew](https://docs.brew.sh/Homebrew-and-Python). I even prefer [pyenv](https://realpython.com/intro-to-pyenv/) because it can handle different versions of Python on the same machine.

Download the files above from GitHub (or use `git clone https://github.com/ralfzosel/zk-smart-search.git`). I chose the directory `code` in my home-directory.

⚠️ If you choose another directory, you have to change the PATH variable in `.zshenv` see below.

Usually, for Python, a virtual environment is recommended (though we only have _one_ package to install with `pip` - namely `rich` for colorful results). This can be done with [venv](https://docs.python.org/3/library/venv.html) or via `pyenv` (see above).

To be able to start the script in the terminal by simply typing `zkss`, you have to add the following line to your `.zshenv`-file in your home directory (on a Mac):

    export PATH=~/code/zk-smart-search:$PATH

If you installed the script to another directory, you have to change the line.

Furthermore, to +make colored output work, you have to add the following line to your `.zshenv`-file:

    export LESS=-r

Restart your terminal to make the changes of `.zshenv` work.

## Configuration

Change the file `settings.py` according to your needs:

- `ZK_BASE_DIR` is the directory where your zettels are stored.
- Change `ENDING` to ".txt" if that's the ending you are using.

## Further ideas


- Integrate smart search in [The Archive](https://zettelkasten.de/the-archive/). ;-)

Further ideas and improvements are welcome.

## Disclaimer

I have only tested on macOS, so I have now idea if it works on Windows, too.

When it comes to Python, I am just a hobbyist and this is my _first_ project I am publishing on GitHub. So it's very likely I made some mistakes. Please bear with me.
