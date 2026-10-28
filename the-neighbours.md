# The Neighbours

Hyperfine is not the only way to time a
command, and several neighbours answer
nearby questions better. The tools below
are characterised, not benchmarked —
this chapter is a map, drawn from their
documentation and ordinary use, and it
does not pretend the lab raced them.

## The shell's `time`, and `/usr/bin/time`

Every shell has a `time` keyword, and
Unix has a `/usr/bin/time` program
(`-v` on GNU systems) that adds peak
memory and page faults to the report.
Their virtue is presence: they are
already on the machine, and for a
command that takes thirty seconds, one
timing with either is most of the
information there is. Their limit is
the subject of chapter 1: one run is
one sample, with no spread, no warmup,
and no second chance unless you make
the loop yourself. When a job is slow
and rare, reach for them; when two
things are close, you need repetitions
and statistics, which is hyperfine's
whole reason to exist.

## A stopwatch loop, by hand

```bash
for i in $(seq 10); do /usr/bin/time -f %e ./tool; done
```

Nothing stops you building the runner
yourself, and doing it once teaches
what hyperfine automates: varied run
counts, discarded outliers, the
statistics themselves. What the hand
loop will not give you without real
work is calibration, parameter sweeps,
exports, and the warnings — the parts
that catch you lying to yourself.

## `perf stat`

Linux's `perf` counts the hardware
events of chapter 10 — cycles,
instructions, cache misses — and prints
them for a single run. It is the tool
hyperfine's `all` preset borrows its
counters from, and it goes further into
profiling territory (`perf record`,
`perf report`) that hyperfine
deliberately does not enter. Where the
question turns from *how long* to
*why*, perf is usually the next door to
knock on — with the same permission
gates chapter 10 met, since both doors
are the same machinery.

## `timeit`, and in-language harnesses

Chapter 6's caveat has a home address:
to compare two *Python functions*, the
fair arena is inside one interpreter,
and Python's `timeit` module (and its
`%timeit` form in interactive shells)
times snippets there, millions of
times, with the interpreter's startup
paid once by the harness rather than
per sample. Other languages have their
equivalents — Rust's criterion, Go's
testing benchmarks, and their kin —
and they share the shape: small units,
in-process, statistics included. Use
hyperfine for whole commands as they
are really invoked; use a harness for
code as it runs inside a process. The
two answers can disagree, and both be
right, because they are answers about
different things.

## Load-testing tools

`wrk`, `k6`, `ab` and their relatives
time *services* under many simultaneous
clients: latency percentiles at a
stated request rate. That is a
different question from this guide's —
one invocation at a time, however often
repeated, says nothing about the
hundredth concurrent user — and the
tool shapes show it. A command-line
benchmark that starts answering service
questions has wandered out of its
chapter; see Limits, next.
