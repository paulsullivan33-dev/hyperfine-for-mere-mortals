# Your First Benchmark

This chapter times a command whose
answer you already know, and takes the
output apart piece by piece. The outcome:
you can read every field of a hyperfine
result, and say where the time that is
not your command's has gone.

## The command

```bash
hyperfine 'sleep 0.2'
```

The command to benchmark goes in
quotes: it is one argument to hyperfine,
which will split it into a program and
its arguments itself. `sleep 0.2` waits
a fifth of a second and exits. Nothing
to install, nothing to prepare — and an
expected answer (about 200 ms) to check
the instrument against, which is what
first benchmarks are for.

The lab's result (transcript
`hyperfine-lab/transcripts/t01-first-benchmark.txt`):

```text
Benchmark 1: sleep 0.2 (14 runs)
                mean     ±       σ          min     …     max
  Wall Time    201.7 ms  ±     0.2 ms     201.5 ms  …   202.1 ms
  Memory         3.2 MiB ±     0.0 MiB      3.2 MiB …     3.2 MiB
```

## Reading it, field by field

- **`Benchmark 1: sleep 0.2`** — the
  command, numbered. With several
  commands (chapter 6) each gets its own
  numbered table.
- **`(14 runs)`** — hyperfine ran it
  fourteen times and timed them all. It
  chooses the count itself: at least
  ten, and more while the budget allows
  (chapter 7). A benchmark here is never
  one run politely repeated in print;
  the count is printed because it is
  part of the evidence.
- **`mean ± σ`** — the average wall
  time, 201.7 ms, plus or minus the
  standard deviation, 0.2 ms. Read it
  as: *a typical run took 201.7 ms, give
  or take two tenths of a millisecond of
  scatter.* Chapter 5 is about this pair
  of numbers and when to distrust them.
- **`min … max`** — the fastest and
  slowest single runs: 201.5 to 202.1
  ms. The whole observed range fits in
  six tenths of a millisecond.
- **`Wall Time`** — elapsed real time,
  as a clock on the wall would see it:
  the measure that includes waiting,
  scheduling, everything.
- **`Memory`** — the peak resident
  memory of the process, 3.2 MiB: what
  it costs to have a `sleep` exist at
  all on this machine, most of it the
  shared machinery of starting any
  program.

## The missing 1.7 milliseconds, accounted for

`sleep` was asked for 200 ms; the mean
says 201.7. The difference is not error.
Starting a program — finding it, loading
it, giving it memory, and later reaping
it — is real work that happens inside
the timed region, because from the
caller's point of view it is part of
what invoking the command costs. Every
hyperfine measurement includes the
invocation it measures, which is honest
— that is the cost you actually pay each
time you run the command — and chapter 5
returns to what it means for very fast
commands, where the invocation can cost
more than the job.

Check: run it yourself. Your mean will
not be 201.7 ms — it will be your
machine's number, probably a millisecond
or two above 200 with a small σ. If it
is wildly above, or the σ is large,
something else is using your machine;
that, too, is a benchmark result, and
chapter 15 (troubleshooting) takes it
up.

## Two habits to start with

Quote the command, always: hyperfine
takes the command as a single string,
and unquoted words would be split by
your own shell first, into a different
command than the one you meant. And
benchmark nothing else in the same
breath — while learning, keep the
machine otherwise idle, so the numbers
you meet in these chapters are the
command's and not a compilation's.
