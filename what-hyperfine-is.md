# What Hyperfine Is

Two ways of doing the same job sit in
front of you — two commands, two flags,
two builds of the same program — and you
want to know which is faster. So you run
one with `time`, then the other, and get
two numbers. The trouble is that each
number is a single sample from a machine
that was also doing other things: the
first run read the file from disk, the
second found it in memory; a background
job woke up during one and not the
other. One run each proves almost
nothing, and everybody who has compared
two `time` outputs knows the rematch
often reverses them.

**Hyperfine is a benchmarking tool for
the command line.** You hand it one or
more commands; it runs each one many
times — dozens or hundreds of times for
fast commands — and reports honest
statistics instead of a single number:
the mean time with its standard
deviation, the fastest and slowest runs,
and the peak memory used. Give it
several commands and it compares them
against the first: *this one is 12.2
times slower*. Give it a parameter and
it sweeps the parameter across values,
benchmarking each. Ask, and it exports
everything — every individual run — to
files you can keep, diff, and plot.

The outcome this chapter delivers: you
can say what question hyperfine answers,
and the rule that governs every honest
answer it gives.

## The rule, stated before everything else

A benchmark is not a fact about a
program. It is a measurement of one
program, on one machine, on one input,
at one moment, under one load — and it
is very easy to rig without meaning to.
Warm the cache for your favourite and
not its rival, benchmark on a toy input
the real job never sees, run each once
and quote the better number: every one
of those produces a confident, wrong
claim. So this guide has one rule, and
it is not fine print:

> **A benchmark is a claim. Measure the
> job you actually care about, on data
> like the real data, under conditions
> you state — and report the spread next
> to the winner.**

Chapter 5 shows how to read the spread.
Chapter 14 is the full list of ways a
benchmark lies. Every chapter between
points back at this rule where the
tooling makes cheating easy, because
hyperfine will happily produce precise
numbers for a meaningless measurement:
precision is its job, meaning is yours.

## A first taste

After installing (chapter 3), the whole
tool is one line:

```bash
hyperfine 'sleep 0.2'
```

`sleep 0.2` asks the machine to pause
for a fifth of a second, so the answer
should be about 200 milliseconds — a
command whose truth you already know,
which makes it the right first subject.
The lab's run (transcript
`hyperfine-lab/transcripts/t01-first-benchmark.txt`):

```text
Benchmark 1: sleep 0.2 (14 runs)
                mean     ±       σ          min     …     max
  Wall Time    201.7 ms  ±     0.2 ms     201.5 ms  …   202.1 ms
  Memory         3.2 MiB ±     0.0 MiB      3.2 MiB …     3.2 MiB
```

Fourteen runs, a mean of 201.7 ms (the
extra 1.7 is starting the program and
the timer's own overhead), a spread so
small the result is boring — which, for
a first benchmark, is exactly what you
want. Chapter 4 takes this output apart
piece by piece.

## Why anyone would do this

- **Choosing.** Two tools do the job;
  one is twelve times faster (chapter 6
  finds a gap that size between three
  one-liners). On a job you run a
  thousand times a day, that is the
  difference between a pause and a
  workflow.
- **Tuning.** A flag, a buffer size, a
  thread count: sweep the values and let
  each one be measured (chapter 9),
  instead of arguing from folklore.
- **Checking a change.** You edited the
  script. Is it slower than yesterday,
  or do you just feel that it is?
  Benchmark before and after, same
  session, and keep the exported numbers
  (chapter 11) as evidence.
- **Retiring guesses.** "That program is
  slow" often means "that program was
  slow once, on a loaded machine, with a
  cold cache." A benchmark with its
  spread stated either confirms the
  complaint or acquits the program.

## Who it is for

The programmer deciding between two
implementations. The system administrator
who suspects a daily job could take half
the time. The tool author who wants a
number in the release notes that would
survive someone else re-measuring it.
The common thread is a command, a
question — *how long, how variably, how
much memory* — and a wish for an answer
with its uncertainty attached.

## What it is not

Hyperfine is not a **profiler**: it
times whole commands from outside and
cannot tell you which function inside
was slow (chapter 13 points at the
tools that can). It is not a **load
tester**: it runs one invocation at a
time and says nothing about a server
under a hundred simultaneous users. It
is not a stopwatch for interactive work —
a human in the loop makes the timing
the human's, not the program's. And it
is not an oracle: its numbers describe
the machine it ran on, and chapter 14
explains why carrying them to another
machine, or another hour, needs care.
