# GHCLI: GitHub Command Line Tools

## Authentication

Create a [personal access token][pat] and place it in a JSON file that looks like:

    {
      "token": "...token goes here..."
    }

Then point the `gh` command at the file using the `-t` argument:

    gh -t credentials.json repo ls

Or by setting the `GITHUB_TOKEN_FILE` enviroment variable to the location of that file:

    export GITHUB_TOKEN_FILE "$PWD/credentials.json"
    gh repo ls

[pat]: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

## Commands

### repo ls

The `gh repo ls` command lists your GitHub repositories:

    Usage: gh repo ls [OPTIONS] [PATTERNS]...

    Options:
      -I, --data-in FILENAME
      -O, --data-out FILENAME
      -u, --user TEXT
      -o, --org TEXT
      --forks / --no-forks
      -r, --reverse
      -s, --sort [created|updated|pushed]
      --url
      -f, --format TEXT
      -t, --type [owner|member|public|private|forks|sources]
      --public
      --private
      --help                          Show this message and exit.
