# Limits

What hyperfine cannot do, stated as
plainly as what it can. Every limit
here is one the lab's own transcripts
met, except where the text says
otherwise.

## It times whole invocations, startup included

The timed region begins when the
process is started and ends when it
exits. Finding the program, loading it,
starting an interpreter if there is
one: all inside the number. For
chapter 6's Python that was nearly the
whole 34.5 ms. This is honest — the
invocation is what you pay in real
use — but it means hyperfine cannot
compare *code* fairly across runtimes,
only *commands*. The in-process
question belongs to chapter 13's
harnesses.

## It cannot tell you why

A benchmark says a command took 132.8 ms
of wall time and 161.7 ms of CPU. It
does not say which function, which
line, or which wait. When the question
becomes *why is it slow*, the tool you
want is a profiler (`perf`, your
language's profiler), and hyperfine's
job shrinks to verifying that the
profiler-guided fix actually helped.
Confusing the two produces benchmarks
of changes that were aimed by guesswork.

## Its numbers belong to one machine, one moment

The lab's own afternoon is the
evidence. The same sort, on the same
machine and file: 273 ms in transcript
t03, 109 ms in the quiet half of t09,
133 ms in t10. Nothing was wrong with
any of them — the machine's other
occupants changed between runs of this
guide's lab, and each measurement
faithfully included them. Under
deliberate load (t09), the mean moved
from 108.6 to 256.3 ms and σ nearly
quadrupled. Consequences, without
exceptions: compare only measurements
taken back-to-back under like
conditions; never quote a hyperfine
number as a property of a program,
only as a property of a program *on
that occasion*; and treat any result
imported from another machine — or
another hour — as a rumour.

## Caches are a state you choose, not a truth

Warm-cache and cold-cache timings of
the same command can differ by an
order of magnitude, and both are real
measurements — of different jobs.
Warmup runs manufacture the warm
position; a cache-clearing `--prepare`
manufactures the cold one. Neither is
"the" speed of the command. The honest
report names the state it measured,
and the dishonest one — chapter 1's
rule again — quietly measures each
contestant in whichever state flatters
it.

## The very fast and the very slow are both hard

Below a few milliseconds, the
measurement floor — process startup,
timer resolution, shell calibration —
is the same size as the subject; the
tool itself warns at 5 ms through a
shell (t02), and no warning is needed
to know that a 0.7 ms median with a
25 ms max is a picture of the machine
more than of `grep`. At the other end,
a command that takes ten minutes can
be run perhaps six times in an hour of
benchmarking, and six samples is an
anecdote with a mean attached.
Hyperfine still helps at both ends —
it keeps the samples honestly — but
its confidence should shrink with
yours.

## Output is discarded, and some commands notice

The default `/dev/null` is not what
your command's real output destination
looks like, and programs can tell the
difference: hyperfine's own help warns
that `grep` optimises when writing to
`/dev/null`, and a program writing to a
terminal pays for scrolling you never
see in the benchmark. Where the real
destination is a file, a pipe, or a
screen, `--output` (chapter 8) lets
the benchmark match it; where you did
not match it, the limit stands whether
you name it or not.

## Memory is a peak, and an approximation

Peak resident set counts shared pages
in every process that maps them, and a
process tree's peak is the tree's
combined figure (chapter 10). It is a
useful approximation for "how much
room does this need", and a poor one
for "how much memory does this
program, uniquely, own". Tools like
`/usr/bin/time -v` report the same kind
of figure with the same caveat;
accounting memory exactly is a harder
problem than benchmarking it.

## The counters are the operating system's to give

Hardware counters exist only where the
platform and your permissions allow
(t10's refusal, in this sandbox,
despite the tool supporting them).
Anywhere virtualised, shared, or
locked down, expect the time and
memory metrics and not the counters —
and do not let a missing row be filled
in by numbers from a different machine.

## It is not a load tester, and it runs things

One invocation at a time means no
concurrency story at all: nothing here
speaks to a service under parallel
demand (chapter 13). And the obvious
limit, worth stating: hyperfine
*executes the commands you give it*,
as you, with your permissions,
including the housekeeping ones.
Benchmark commands you understand, on
machines that are yours — a surprising
sentence to need in a guide about a
stopwatch, but a benchmarking command
is still a command.
