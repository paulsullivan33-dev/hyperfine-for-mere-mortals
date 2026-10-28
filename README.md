# Hyperfine for Mere Mortals

You have two ways of doing the same
job, and you want to know which is
faster. Timing each once proves almost
nothing: the first run read its file
from disk, the second found it in
memory, and a background job woke up
during one of them. **Hyperfine** is
the command-line benchmarking tool that
answers properly. It runs a command
many times, throws the output away,
and reports the statistics — mean time
with its standard deviation, fastest
and slowest runs, peak memory — and,
given several commands, prices each
one against the first: *12.2 times
slower*, with the scatter printed next
to the verdict.

This guide explains how to run your
first benchmark and read every field
of the result, how to stage a fair
comparison between three ways of doing
one job, how warmups, run counts and
preparation decide what state the
measurement starts from, what a shell
adds to a number and when to leave it
out, how to sweep a setting across its
values with lists and scans, what the
other metrics (CPU time, hardware
counters) can and cannot show, and how
to export the numbers so next month's
question — *did that change make it
slower?* — has something to stand on.

The rule that governs everything here
is stated in chapter 1: **a benchmark
is a claim. Measure the job you
actually care about, on data like the
real data, under conditions you state —
and report the spread next to the
winner.** Hyperfine will manufacture
precise numbers for a rigged comparison
as happily as for a fair one; the
honesty has to come from the person
staging it, and this guide points at
the rigging opportunities as they
appear.

The lab behind this guide ran the real
thing: **hyperfine 2.0.0**, the
official release binary, on a small
shared Linux machine, against fixtures
it generated itself — an invented
50,000-line server log, 200,000
shuffled numbers, 8 MB of invented
prose (`hyperfine-lab/make_fixtures.py`
rebuilds them deterministically). On
those fixtures the lab verified that
three different commands produce the
same answer before racing them; raced
them (`grep`, `awk`, Python — an order
of magnitude apart, and mostly
interpreter startup); measured a shell's
price at a millisecond or two; swept
gzip's compression levels and caught a
single outlier bending one row's mean
out of order; scanned a sort across
four input sizes; decompressed a file
reset by `--prepare` before every run;
exported one benchmark three ways and
read the JSON back; timed a sort with
both of the machine's CPUs pinned by
busywork and watched its mean go from
108.6 to 256.3 ms; and split CPU time
into user and system under the `time`
metric preset.

What the lab could not do, it did not
fake. The machine is shared and noisy,
and the guide does not hide that: the
scatter in its own transcripts is used
as teaching material, and absolute
numbers differ between transcripts an
hour apart — chapter 14 explains why
that is expected, and why comparisons
must be made back-to-back. The
processor's hardware counters
(instructions, cycles, cache misses)
are refused by this machine outright,
so they are described from the
documentation and labelled as such,
with the refusal itself captured.
Cache-clearing preparation, which needs
administrator rights the lab did not
use, is likewise documented-only.
`criteria.md` keeps the full ledger of
what was run and what was only read.

## What this guide covers

- [**What hyperfine is**](what-hyperfine-is.md) —
  the question a benchmark answers, why
  one timing is not an answer, and the
  honesty rule the whole guide works by
- [**The moving parts**](the-moving-parts.md) —
  the runner, calibration, the run loop,
  the statistics, the metrics, and where
  parameters and exports fit
- [**Installing hyperfine**](installing-hyperfine.md) —
  the release binary and the package
  managers, and why version 2's changed
  shell default matters when you read
  older advice
- [**Your first benchmark**](your-first-benchmark.md) —
  timing a `sleep`, and every field of
  the output taken apart
- [**Reading the results**](reading-the-results.md) —
  mean and σ, min and max, the median
  hiding in the exports, the reference
  command, and warnings as part of the
  result
- [**Comparing commands**](comparing-commands.md) —
  proving three commands do the same job
  before racing them, and reading a
  12.2x verdict without overclaiming it
- [**Warmups, runs and preparation**](warmups-runs-and-preparation.md) —
  what state a measurement starts from:
  warmups, run counts, `--prepare`,
  and the setup, conclude and cleanup
  slots
- [**Shells, and what gets timed**](shells-and-what-gets-timed.md) —
  version 2's no-shell default, `-S` and
  `--shell`, what the shell costs, and
  where a command's output goes
- [**Parameters — lists and scans**](parameters.md) —
  `-L` lists and `--parameter-scan`
  ranges, a gzip sweep with a misleading
  row, and a sort whose cost grows with
  its input
- [**Choosing what to measure**](metrics.md) —
  the metric presets, CPU against wall
  time, user against system, peak
  memory, and the hardware counters
  this machine refused to give
- [**Exports**](exports.md) — Markdown
  for the report, CSV for the
  spreadsheet, JSON with every run in
  it, read back and checked
- [**Recipes**](recipes.md) — choosing a
  setting, regression-checking a change,
  scaling tests, inputs that get eaten,
  pipeline stages, and starting and
  stopping a server per run
- [**The neighbours**](the-neighbours.md) —
  the shell's `time`, `/usr/bin/time`, a
  hand-rolled loop, `perf stat`,
  in-language harnesses like `timeit`,
  and load-testing tools: which question
  each one answers
- [**Limits**](limits.md) — whole
  invocations only, no reasons why,
  numbers that belong to one machine and
  one moment, caches as a choice, the
  very fast and the very slow, and what
  a load tester would say instead
- [**Troubleshooting**](troubleshooting.md) —
  the exit-code trap, the first-run and
  under-5-ms warnings quoted and
  answered, wild scatter traced to load,
  the counters refusal, and pipelines
  that fail until `-S`
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Profiling — why a program is slow, as
opposed to how slow — beyond pointing
at the tools that do it. Load testing
a service under concurrent users.
Benchmarking interactive programs, where
the timing belongs to the human. Any
claim that a number measured here
transfers to your machine: the guide
teaches you to produce numbers on
yours, and its limits chapter explains
why borrowed ones are rumours.

## How to use this guide

Read chapter 1 for the rule and
chapter 2 for the map; both are short
and everything later leans on them.
Chapter 4 is your first benchmark, in
the same sitting as the install, on a
command whose answer you already know —
`criteria.md` and chapter 5 are where
the reading skill is built, so do not
skip 5: most benchmark nonsense in the
world is chapter 5's material, ignored.
The lab's fixtures and transcripts
live in `hyperfine-lab/` — regenerate
the fixtures with `make_fixtures.py`,
and treat the transcripts as the
expected shape of results, not the
expected numbers. Its reading script
is `hyperfine-lab/readback.py`; its
notes are `examples/lab-notes.txt`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Bash for Mere Mortals](https://paulsullivan33-dev.github.io/bash-for-mere-mortals/)
- [GNU Parallel for Mere Mortals](https://paulsullivan33-dev.github.io/gnu-parallel-for-mere-mortals/)
- [Watching Your System for Mere Mortals](https://paulsullivan33-dev.github.io/watching-your-system-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/hyperfine-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/hyperfine-for-mere-mortals/blob/main/LICENSE-CODE).
