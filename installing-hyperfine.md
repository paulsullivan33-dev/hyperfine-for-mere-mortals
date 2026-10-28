# Installing Hyperfine

Hyperfine is a single self-contained
program, written in Rust, and it is
installed the ways such programs are: a
binary download from the project's
GitHub releases, a package manager, or
Cargo (Rust's package tool). This
guide's lab used the official release
binary, unpacked into a scratch folder —
nothing installed system-wide, and
deleting the folder deletes the tool.
That is the route taught here; the
package-manager routes end at the same
one command.

## The release binary

From the releases page of
`github.com/sharkdp/hyperfine`, download
the archive for your platform (the lab's
was `hyperfine-v2.0.0-x86_64-unknown-linux-gnu.tar.gz`),
unpack it, and the `hyperfine` binary
inside is the whole tool:

```bash
tar xzf hyperfine-v2.0.0-x86_64-unknown-linux-gnu.tar.gz
./hyperfine-v2.0.0-x86_64-unknown-linux-gnu/hyperfine --version
```

Check: the lab's version printout
(transcript
`hyperfine-lab/transcripts/t00-version.txt`)
reads:

```text
$ hyperfine --version
hyperfine 2.0.0
```

Move the binary somewhere on your path
(`/usr/local/bin` or `~/bin`) if you
want to call it as plain `hyperfine`,
as the rest of this guide does.

## Package managers

The project also ships through the usual
channels — among them Debian and Ubuntu
(`sudo apt install hyperfine`), Fedora
(`sudo dnf install hyperfine`), Arch
(`sudo pacman -S hyperfine`), macOS
(`brew install hyperfine`), Windows
package managers, and Cargo
(`cargo install hyperfine`). These
routes are described from the project's
documentation; the lab exercised only
the release binary. One caution, and it
matters for this tool: a distribution
package may lag the current release by
a version or more, and version 2
changed a default that older advice
assumes (see below). Whatever route you
took, `--version` tells you which
hyperfine you have.

## The version matters more than usual

This guide is written against
**hyperfine 2.0.0**, and 2.0 changed
the default shell behaviour: version 1
ran every command through a shell unless
told otherwise; version 2 runs commands
directly, with no shell, unless you ask
for one with `-S` or `--shell`. Tips
written for version 1 — including some
in the project's own older examples —
may quietly assume a shell is present,
so a pipeline that "just worked" in an
old blog post can fail in 2.0 with a
file-not-found error until `-S` is
added. Chapter 8 covers this properly.
The transcripts in this guide are all
from 2.0.0, and `hyperfine --help` on
your machine is the final authority on
your version's flags.

## Where it writes things

Almost nowhere. Hyperfine keeps no
configuration file and no state folder:
a run reads nothing and leaves nothing
behind except the export files you
explicitly ask for (chapter 11). That
makes it safe to drop into a borrowed
shell or a build machine, and it means
every behaviour in this guide comes
from the command line in front of you,
not from a setting you forgot.
