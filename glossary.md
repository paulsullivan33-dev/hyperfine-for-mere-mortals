# Glossary

**Benchmark** — a controlled
measurement of a command: the same
invocation, repeated, with the results
summarised statistically (chapter 1).

**Calibration** — hyperfine's
measurement of shell startup time,
accounted for when commands run through
a shell; it has a precision floor that
produces the under-5-ms warning
(chapters 2, 6).

**Cold cache** — the state where a
command's program and data must be read
from disk on first use; the opposite of
warm. Measuring cold is a choice made
with `--prepare`, not an accident
(chapter 7).

**CPU time** — the time the processor
spent on a command, user plus system;
can exceed wall time when several
cores work at once (chapter 10).

**Hardware counters** — measurements
taken by the processor itself
(instructions, cycles, cache misses,
branch misses), available only where
the operating system permits
(chapter 10).

**Max** — the slowest single run in a
benchmark; a max far from the min is
the signature of interference
(chapter 5).

**Mean** — the average of the runs.
Trustworthy in proportion to how small
σ is beside it (chapter 5).

**Median** — the middle run when all
runs are sorted; resistant to a few
wild runs, and carried by the exports
though not the terminal table
(chapters 5, 11).

**Metric** — a kind of quantity a
benchmark collects: wall time, CPU
time, peak memory, hardware counters.
Chosen with `--metrics` (chapter 10).

**Min** — the fastest single run; for
CPU-bound work, often the most
repeatable number in the table
(chapter 5).

**Outlier** — an individual run far
from the pack, usually the machine's
fault rather than the command's;
hyperfine reports rather than deletes
them (chapters 5, 9).

**Parameter list** — `-L`: benchmark a
command once per value from an explicit
list, substituting `{name}` in the
command text (chapter 9).

**Parameter scan** — `--parameter-scan`:
the same substitution over a generated
range, with `-D` setting the step
(chapter 9).

**Peak resident set size (peak RSS)** —
the memory metric: the most physical
memory the process held at any one
moment (chapter 10).

**Prepare** — `--prepare`: a command
run, untimed, before every timed run,
to give each run the same starting
state (chapter 7).

**Reference** — the first command in a
comparison; every later command's
change and factor are priced against
it (chapter 5).

**Run** — one timed invocation of the
command. A benchmark is a set of runs
plus their statistics (chapter 4).

**σ (sigma)** — the standard deviation:
how widely the runs scattered around
the mean. The mean's trustworthiness,
printed next to it (chapter 5).

**Setup / conclude / cleanup** — the
housekeeping slots around the runs:
setup once before a command's runs,
conclude after each run, cleanup once
after them (chapter 7).

**System time** — CPU time spent in the
kernel on the command's behalf, as
opposed to **user time**, spent in the
program itself (chapter 10).

**Wall time** — elapsed real time from
start to exit, as a clock on the wall
sees it; includes all waiting
(chapter 4).

**Warmup** — `--warmup N`: N untimed
runs before the timed ones, so caches
and the machine settle first
(chapter 7).
