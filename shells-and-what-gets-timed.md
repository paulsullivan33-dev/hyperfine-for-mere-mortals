# Shells, and What Gets Timed

Every hyperfine number quietly answers
a question you may not have asked: what,
exactly, was timed? This chapter makes
the answer explicit. The outcome: you
can say whether a given result is the
price of a program, or of a program
plus the shell that launched it, and
choose on purpose.

## The default in version 2: no shell

Hyperfine 2 runs commands **directly**:
the string you give is split into a
program and its arguments, and the
program is started as-is. There is no
shell in between — which means the
things a shell normally provides do
not exist:

- no pipes (`|`) or redirection (`>`, `<`),
- no `&&`, `;`, or `$(...)`,
- no `~` or glob expansion,
- no shell builtins.

A command string that needs any of
those fails — typically "file not
found", because the whole remainder was
treated as argument text. The fix is to
ask for a shell, below. (Version 1
behaved the other way — shell by
default — which is why older examples
online do not mention any of this;
chapter 3's warning.)

## Asking for a shell

- `-S` (or `--shell=default`) — the
  platform shell: `sh` on Linux and
  macOS, `cmd.exe` on Windows.
- `--shell 'bash --norc'` — any shell,
  by name or path, with its own flags
  if you want them.
- `-N` (or `--shell=none`) — spell out
  the default: no shell.

What does a shell cost? The lab timed
the same `sleep 0.05` three ways
(transcript
`hyperfine-lab/transcripts/t04-shells.txt`):

```text
$ hyperfine 'sleep 0.05'
  Wall Time     52.8 ms  ±     1.9 ms      51.3 ms  …    61.0 ms
$ hyperfine -S 'sleep 0.05'
  Wall Time     54.3 ms  ±     3.1 ms      51.3 ms  …    64.8 ms
$ hyperfine --shell 'bash --norc' 'sleep 0.05'
  Wall Time     52.0 ms  ±     1.8 ms      50.9 ms  …    62.1 ms
```

On this machine, an `sh` in front of the
command added a millisecond or two;
bash landed in the same place. Small —
but chapter 6's `grep` finished its
whole job in 1.8 ms, so for fast
commands the shell is not a detail, it
is most of the measurement. Hyperfine
knows this: when a shell is used it
calibrates by timing empty shell
invocations and accounts for the
startup, and when the command is faster
than about 5 ms it prints the warning
chapter 6 quoted, because that
calibration has a precision floor.

The rule for choosing: **benchmark the
command the way it will really be run.**
If the real use is a pipeline typed in
a shell, benchmark the pipeline, with
`-S`, shell and all — the shell is part
of the real cost. If the real use is a
program started by another program,
benchmark it bare with `-N`, and quoting
a through-the-shell number for it would
be the chapter 1 rule broken in a small,
plausible way.

Two things always use a shell, whatever
you choose: the housekeeping commands
(`--setup`, `--prepare`, `--conclude`,
`--cleanup` — chapter 7), because they
are given as command lines. And note
that quoting still matters with no
shell: hyperfine splits your string on
spaces honouring quotes, so
`grep -c ERROR log.txt` arrives as three
arguments, while the `awk` program in
chapter 6 — full of spaces that belong
together — is exactly the kind of
command that is simpler through `-S`.

## Where the command's output and input go

By default the benchmarked command's
output is discarded to `/dev/null` and
its input is `/dev/null` too. That is
deliberate: a benchmark should not slow
down filling your terminal, nor wait
for keyboard input. The controls:

- `--output pipe` — through a pipe
  before discarding; `--output <file>` —
  into a file; `--output inherit` (or
  `--show-output`) — onto your terminal.
- `--input <file>` — feed the command
  from a file instead of the void.

These exist because discarded output is
itself a condition that can mislead:
some programs notice. The tool's own
help gives the example — `grep` detects
when its output is `/dev/null` and
applies optimisations — so a pipeline
whose real destination is a file or
another program may behave measurably
differently from its `/dev/null`
benchmark. Showing output
(`--show-output`) also costs real time
and is meant for debugging what a
command does, not for timing it.
Chapter 14 lists this among the limits;
the defence is to benchmark with the
output arrangement the real job uses.

Check: take a command you have already
benchmarked and state which of these
was inside your number — a shell (which
one), what output arrangement, whose
startup. If any answer is "I don't
know", the number is not yet one you
can defend; rerun it deliberately both
ways, as t04 does, and keep the pair.
