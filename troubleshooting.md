# Troubleshooting

The failures this guide's own lab met,
in the order a reader is likely to
meet them, each with its cause and its
check. Nothing here is invented: every
entry is in a transcript in
`hyperfine-lab/transcripts/`.

## "Command terminated with a non-zero exit code"

```text
$ hyperfine 'grep -c NOSUCHLEVEL log.txt'
Error: Command 'grep -c NOSUCHLEVEL log.txt' terminated with
non-zero exit code 1 in the first benchmark run. Use the
'-i'/'--ignore-failure' option if you want to ignore this.
Alternatively, use the '--show-output' option to debug what
went wrong.
```

(transcript t90). The lab's `grep` was
not broken: it counted zero matches,
printed `0`, and exited 1, because that
is `grep`'s contract — failure means
"no lines selected". Hyperfine stops
because a failed command's timing is
usually the timing of its failure, not
of the job. Two honest ways forward:
`-i` when the exit code is part of the
job's normal behaviour (expect the
warning `Ignoring non-zero exit code`
in the output, and leave it in any
report), or `--show-output` when you do
not yet know why the command fails.
Benchmarking a command whose failure
you have not looked at is measuring a
surprise.

## "The first benchmarking run was significantly slower"

Hyperfine's own words (t05, t06, t07):

```text
Warning: The first benchmarking run for this command was
significantly slower than the rest (75.0 ms). This could be
caused by (filesystem) caches that were not filled until
after the first run. You should consider using the '--warmup'
option to fill those caches before the actual benchmark.
```

Cause: the first run pays for cold
caches. Decide which state is your real
one and set it deliberately — `--warmup`
to measure warm, a cache-clearing
`--prepare` to measure cold (chapter
7). The variant in t07 is subtler:

```text
... You are already using the '--prepare' option which can
be used to clear caches. If you did not use a cache-clearing
command with '--prepare', you can either try that or
consider using the '--warmup' option ...
```

— the prepare there restored an input
file but cleared nothing, and the
first run was still the cold one. The
warning adapts to what you already did;
read it to the end before acting on it.

## "Command took less than 5 ms to complete"

Through a shell, hyperfine calibrates
the shell's startup and subtracts it —
but only to a precision floor, and
below about 5 ms of command it prints
the warning quoted in chapter 6. If the
command does not need the shell, rerun
with `-N` and the calibration problem
disappears with the shell. If it does
need the shell, keep the warning in the
report: the number is usable, its last
millisecond is not.

## The numbers wobble: σ near the mean, a wild max

One row of t02: mean 22.6 ms, σ 20.5,
runs from 11.1 to 111.0 ms. The command
did not change its mind about how to
run; the machine did other work during
some runs. Diagnose before believing:
rerun on a quiet machine, or prove the
load is the cause the way t09 did —
two `yes` processes pinning both of the
lab machine's CPUs moved `sort` from
108.6 ± 8.6 ms to 256.3 ± 32.9 ms.
Under load, everything in this guide
still *works*; it just measures the
load too. If you cannot quiet the
machine, compare medians or minimums,
take more runs, and write the
conditions in the report.

## "Metric 'instructions' is unavailable"

```text
Error: Metric 'instructions' is unavailable for 'sort -n
numbers.txt'. Check platform support and hardware-counter
permissions.
```

(transcript t10). Hardware counters
need the operating system's permission,
and virtual machines, containers, and
shared hosts commonly withhold it. It
is not a hyperfine fault and there is
no flag that argues with it: fall back
to `--metrics time`, and if the
counters matter, run on a machine where
you hold the permissions (chapter 10).

## "No such file or directory" for a pipeline that works in your shell

```bash
hyperfine 'grep ERROR log.txt | wc -l'   # no shell: fails
hyperfine -S 'grep ERROR log.txt | wc -l' # works
```

Version 2 runs commands directly, with
no shell (chapter 8): the pipe was
handed to `grep` as literal arguments,
and the "file" it went looking for was
named `|`. If the command line contains
`|`, `>`, `&&`, or `$(...)`, it needs
`-S`. This is also the first thing to
check when an example copied from an
older article — written when the shell
was the default — fails unchanged.

## My result disagrees with the documentation's (or a colleague's)

Check, in order: the version
(`hyperfine --version` — chapter 3's
shell default changed between 1.x and
2.0, and statistics presentation with
it); the machine (chapter 14 — numbers
do not travel); the state (warm or
cold caches, chapter 7); and the load
(the entry above). A disagreement that
survives all four checks is a finding;
most do not survive the second.
