# zk-smart-search

Tool that helps to easier find "zettels" in large zettelkastens.

## Usage (Example)

To search for zettels containing the term "my zettelkasten" (or at least "my" and "zettelkasten"), simply type `zkss my zettelkasten` in your terminal and press enter. This is what it can look like:


[](https://user-images.githubusercontent.com/46703936/213792583-75f8f0d6-439c-43ef-af63-cc0aef314d5a.mp4)

       
The results are grouped, as you can see, and sorted by `last accessed`. Every zettel occurs only once in the result list.

You can "pipe" the result to handle the output, e.g.

    $ zkss my zettelkasten | grep "search"

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
