# Comparing Commands

This is the job hyperfine exists for:
several commands, one task, a verdict
with its uncertainty attached. The
outcome of this chapter is a comparison
done properly — which starts, perhaps
surprisingly, before any timing happens.

## First, prove they do the same job

A faster wrong answer is not faster;
it is just wrong sooner. So before
timing anything, run each contestant
once and compare what it *produces*.
The lab's question was a small, real
one: **how many ERROR lines are in this
log file?** Its fixture
(`hyperfine-lab/make_fixtures.py` builds
it) is a 50,000-line invented server
log, and the three contestants are the
three ways a shell user reaches for
first — `grep`, `awk`, and a small
Python script (`hyperfine-lab/count_errors.py`).
Transcript
`hyperfine-lab/transcripts/t02a-same-answer.txt`:

```text
$ grep -c ERROR log.txt
2471
$ awk '/ERROR/ {n++} END {print n}' log.txt
2471
$ python3 count_errors.py log.txt
2471
```

Three programs, one answer: 2,471.
Only now is a race between them a race
between equals.

## The race

```bash
hyperfine -S --warmup 2 -n grep -n awk -n python3 \
  'grep -c ERROR log.txt' \
  "awk '/ERROR/ {n++} END {print n}' log.txt" \
  'python3 count_errors.py log.txt'
```

Three new pieces of command line: `-S`
runs the commands through a shell
(chapter 8 — the `awk` command needs
one for its quoting); `--warmup 2`
discards two untimed runs per command
first (chapter 7); and `-n` gives each
command a short **name**, because the
report will be read by humans. The
lab's result (transcript t02):

```text
Benchmark 1: grep (1523 runs)
                mean     ±       σ          min     …     max
  Wall Time      1.8 ms  ±     1.5 ms       0.9 ms  …    16.7 ms
  Memory         3.5 MiB ±     0.1 MiB      3.1 MiB …     3.6 MiB

  Warning: Command took less than 5 ms to complete. Note that the
  wall-clock measurements might be inaccurate because hyperfine can
  not calibrate the shell startup time much more precise than this
  limit. You can try to use the `-N`/`--shell=none` option to
  disable the shell completely.

Benchmark 2: awk (137 runs)
  Wall Time     22.6 ms  ±    20.5 ms      11.1 ms  …   111.0 ms         +1122.9%  (12.2x slower)
  Memory         3.7 MiB ±     0.1 MiB      3.6 MiB …     3.9 MiB           +5.7%

Benchmark 3: python3 (86 runs)
  Wall Time     34.5 ms  ±     3.8 ms      30.8 ms  …    56.9 ms         +1770.8%  (18.7x slower)
  Memory        10.1 MiB ±     0.1 MiB      9.8 MiB …    10.2 MiB         +183.9%  (2.8x more)
```

## Reading the verdict honestly

`grep` wins by an order of magnitude,
which surprises no one: it is a small
native program doing the one thing it
exists to do. But read the three rows
the way chapter 5 taught:

- **Know what each number is made of.**
  At these sizes, the file scan itself
  is a millisecond or less. Most of
  awk's 22.6 ms and nearly all of
  Python's 34.5 ms is *starting the
  interpreter* — the benchmark compares
  invocations, not algorithms. That is
  the fair comparison if your real use
  is "run this from the shell each
  time", because you pay the startup
  every time. If instead you were
  choosing a technique inside a
  long-running Python program, this
  benchmark would be measuring the
  wrong thing entirely, and the
  rule from chapter 1 says so.
- **σ is a result, not noise to hide.**
  awk's spread (11.1 to 111.0 ms, σ
  nearly equal to its mean) says this
  machine interrupted awk constantly.
  The 12.2x factor is so large that the
  conclusion survives anyway; had the
  gap been 20%, that σ would have
  swallowed it, and the honest report
  would be "indistinguishable here".
- **The warning is part of grep's
  result.** At 1.8 ms through a shell,
  grep is near the floor where shell
  calibration loses precision, and
  hyperfine says so in plain words.
  Dropping the shell (`-N`, with the
  command given as a plain program and
  arguments) is the remedy it suggests;
  chapter 8 shows the shell's actual
  price on this machine.
- **Memory separates cleanly.** Python's
  10.1 MiB peak against ~3.5 for the
  others barely scatters — a stable,
  real difference, the interpreter's
  footprint, worth its own line in any
  report where memory is scarce.

Check: the three outputs in t02a are
identical, and the t02 table's factors
are priced against grep, the first
command. If you rerun the race, your
factors will differ in the decimals and
should agree in the story: grep first
by a wide margin, awk and Python an
order of magnitude behind, most of
their time spent starting up.
