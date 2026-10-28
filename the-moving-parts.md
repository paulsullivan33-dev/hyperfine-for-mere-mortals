# The Moving Parts

Hyperfine is one program, but a
benchmark it produces passes through
five distinct parts, and knowing which
part holds what turns later surprises
into named problems. This chapter is
the map; each part gets its own chapter
later.

## The runner

The runner starts your command, waits
for it to finish, and records how long
that took and how much memory it used at
its peak. Three decisions live here:

- **Directly or through a shell.** By
  default (in version 2) there is no
  shell: the command is started as a
  program with arguments. Pipes,
  redirection and `&&` do not exist
  until you ask for a shell with `-S` or
  `--shell` (chapter 8).
- **Where output goes.** The command's
  output is thrown away — sent to
  `/dev/null` — so printing cannot slow
  the measurement or flood your
  terminal. `--output` and
  `--show-output` change this, at a
  price chapter 8 states.
- **What counts as failure.** A command
  that exits non-zero stops the
  benchmark with an error, unless you
  say otherwise with `-i` (chapter 14
  shows the trap this sets for `grep`).

## Calibration

Starting a program is itself work, and
when a shell is involved, starting the
shell is work too. Before timing,
hyperfine measures that overhead — it
times empty invocations — so that shell
startup can be accounted for rather
than blamed on your command. There is a
floor to how precisely this can be
done, and when a benchmarked command is
faster than about 5 milliseconds
through a shell, hyperfine says so in a
warning (the lab's `grep` earned it;
chapter 6 shows the wording).

## The run loop

One timing is an anecdote, so the
runner repeats: optional **warmup runs**
first (untimed, to fill caches and let
the machine settle — chapter 7), then
timed runs. By default hyperfine decides
how many: at least ten, and for fast
commands it keeps going until it has
spent a reasonable time budget, which is
why the lab's `grep` got over a thousand
runs while its `sort` got fifteen.
`--runs`, `--min-runs` and `--max-runs`
put you in charge. Around each timed
run, optional **prepare** and
**conclude** commands can set up and
tear down state; around the whole set,
**setup** and **cleanup** (chapter 7).

## The statistics

The recorded times become a table:

- the **mean** — the average run;
- **σ (sigma), the standard deviation** —
  how widely the runs scattered around
  the mean; the number that decides
  whether the mean deserves trust;
- **min … max** — the fastest and
  slowest runs seen;
- and, in the exports, the **median** —
  the middle run when all are sorted.

With several commands, every command
after the first also gets a comparison
against the first: a percentage change
and a factor (*12.2x slower*). The first
command is the **reference**, so the
order you list commands in is part of
the report (chapter 5).

## The metrics

Time is the headline, but hyperfine
collects **metrics**: by default, wall
time and peak memory (resident set
size — the most physical memory the
process held at once). The `time`
preset adds CPU time, split into user
and system. Where the operating system
permits, hardware counters (instructions,
CPU cycles, cache misses) are available
too. `--metrics` chooses; chapter 10
shows each kind, including this
machine's refusal to hand over the
counters.

## Parameters and exports

Two parts turn one benchmark into an
investigation. **Parameters** (`-L` for
a list of values, `--parameter-scan`
for a range) substitute values into the
command text and benchmark every
resulting command (chapter 9).
**Exports** (`--export-json`,
`--export-markdown`, `--export-csv`,
and two more) write the results to
files — the JSON carrying every
individual run, the others summarising
(chapter 11).

Check: you can now predict the shape of
any hyperfine result before running it —
a runner making timed runs, a table of
mean ± σ and min … max per metric, and,
if you gave several commands, each
later one priced against the first.
