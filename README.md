# zk-smart-search

Tool that makes it easier to find "zettels" in large zettelkastens.

## Usage (Example)

### Keyword Search (Standard)
To search for zettels containing the term "my zettelkasten" (or at least "my" and "zettelkasten"), simply type `zkss my zettelkasten` in your terminal and press enter. This is what it can look like:

[](https://user-images.githubusercontent.com/46703936/213792583-75f8f0d6-439c-43ef-af63-cc0aef314d5a.mp4)
   
The results are grouped, as you can see, and sorted by `last accessed`. Every zettel occurs only once in the result list.

You can "pipe" the result to handle the output, e.g.

    $ zkss my zettelkasten | grep "search"

### Semantic Search
You can now search for notes by **meaning** rather than exact keywords. This is useful when you remember the *concept* but not the exact words.

    $ zkss -s "personal knowledge management"

Or use the long flag:

    $ zkss --semantic "personal knowledge management"

The first time you run this, it will build a local vector index (stored in `~/.zkss_index`). Subsequent runs will be instant, incrementally updating the index with any new or modified notes.

To force a complete rebuild of the index:

    $ zkss --reindex

### MCP Server (AI Integration)
You can expose your Zettelkasten to AI assistants (like Claude Desktop or Cursor) using the Model Context Protocol (MCP).

**Configuration for Cursor:**
1. Save as `.cursor/mcp.json` in your workspace root directory:

```json
{
  "mcpServers": {
    "zk-smart-search": {
      "command": "/YOUR/ABSOLUTE/PATH/TO/zk-smart-search/venv/bin/python",
      "args": ["/YOUR/ABSOLUTE/PATH/TO/zk-smart-search/mcp_server.py"]
    }
  }
}
```

2. Go to **Cursor Settings** > **Features** > **MCP Servers** and enable `zk-smart-search` (if not auto-detected).

Replace `/YOUR/ABSOLUTE/PATH/TO` with the actual path to your cloned repository.

**Configuration for Claude Desktop:**
Add the same JSON configuration to your `~/Library/Application Support/Claude/claude_desktop_config.json`.

**Available Tools:**
- `search_notes(query, semantic=False)`: Search for notes using keywords or semantic search.
- `read_note(filename)`: Read the full content of a note.

## Why zkss?

Software like [The Archive](https://zettelkasten.de/the-archive/) sort the search results by _title_, _creation date_ or _modification date_. However, for some search terms, the more zettels you have, the more time you spend skimming the list of search results.

By structuring the search results and showing the presumably most relevant first, you should be able to save time finding the desired zettels.

## Installation
First, you need Python, of course. On a Mac, it [works best with Homebrew](https://docs.brew.sh/Homebrew-and-Python). I prefer [uv](https://docs.astral.sh/uv/) because it can handle different versions of Python on the same machine in simple way.

Download the files above from GitHub (or use `git clone https://github.com/ralfzosel/zk-smart-search.git`). I chose the directory `code` in my home-directory.

⚠️ If you choose another directory, you have to change the PATH variable in `.zshenv`, see below.

### Dependencies
It is highly recommended to use a virtual environment - either with `uv` (I mentioned it above) or with `venv`:

```bash
cd ~/code/zk-smart-search
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To be able to start the script in the terminal by simply typing `zkss`, you have to add the following line to your `.zshenv`-file in your home directory (on a Mac):

    export PATH=~/code/zk-smart-search:$PATH

If you installed the script to another directory, you have to change the line.

Furthermore, to make colored output work, you have to add the following line to your `.zshenv`-file:

    export LESS=-r

Restart your terminal to make the changes of `.zshenv` work.

## Configuration

Change the file `settings.py` according to your needs:

- `ZK_BASE_DIR` is the directory where your zettels are stored.
- Change `ENDING` to ".txt" if that's the ending you are using instead of ".md".

## Further ideas

- Integrate smart search in [The Archive](https://zettelkasten.de/the-archive/). ;-)

Further ideas and improvements are welcome.

## Disclaimer

I have only tested on macOS, so I have now idea if it works on Windows, too.

When it comes to Python, I am just a hobbyist and this is my _first_ project I am publishing on GitHub. So it's very likely I made some mistakes. Please bear with me.

*Update (Dec 2025): This project has been significantly refactored and enhanced with Semantic Search capabilities and MCP support, built with the help of [Responsible Vibe MCP](https://github.com/mrsimpson/responsible-vibe-mcp) and Gemini 3 Pro.*
