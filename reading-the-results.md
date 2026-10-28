# Reading the Results

A hyperfine table is short — three
numbers per metric — and every beginner
mistake is a way of reading only the
first of them. This chapter delivers
the outcome the rest of the guide
depends on: you can look at any result,
including the lab's own, and say how
much of it to believe.

## The mean is a summary, not the result

The mean answers "what did a run
typically cost?" only when the runs
clustered. The number that tells you
whether they did is **σ, the standard
deviation**: roughly, the typical
distance of a run from the mean. Small
σ next to the mean (201.7 ± 0.2 ms) —
the runs agreed; quote the mean freely.
σ approaching the mean itself — the
runs were all over the place, and the
mean is an average of disagreements.

The lab's `grep` from chapter 11's
export shows the extreme case. On
paper: mean 1.70 ms. But its σ was
3.39 ms — twice the mean — and the
export's median tells the real story:

```text
grep: 574 runs, wall mean 1.70 ms, stddev 3.39 ms, median 0.70 ms, peak memory mean 3.6 MiB
```

(from `hyperfine-lab/transcripts/t08-exports.txt`).
Most runs took about 0.7 ms; a minority
were mugged by the machine (the slowest
took 25.7 ms) and dragged the mean to
two and a half times the median. The
**median** — the middle run — ignores
the muggings, which is why the exports
carry it even though the terminal table
does not. Rule of thumb: when σ is a
large fraction of the mean, compare
medians or minimums, not means, and ask
what the machine was doing.

## Min, max, and the steadiest number

The **min** is the run where everything
went right: caches warm, scheduler
kind, no interruptions. For CPU-bound
work it is often the most repeatable
number in the table — rerun the
benchmark and the min barely moves
while the mean wanders. The **max** is
the opposite: the worst the machine did
to the command. A max far from the min
(chapter 9's gzip at one setting:
56.5 ms min, 189.8 ms max) is not a
detail to average away; it is the
signature of interference, and chapter
15 treats it as a symptom to diagnose.

## The comparison column, and the reference

With several commands, each command
after the first is priced against the
**first** one:

```text
  Wall Time     22.6 ms  ±    20.5 ms      11.1 ms  …   111.0 ms         +1122.9%  (12.2x slower)
```

The percentage is the change in mean;
the factor in brackets is the same
thing said plainly. Two consequences.
First, the reference is a choice: list
the incumbent first and the report reads
as "the challenger is X% faster or
slower than what we have"; list them
the other way and the same data reads
in reverse. Neither is wrong, but a
report that hides which was the
reference is hiding a decision. Second,
the comparison inherits the uncertainty
of both means — a "+63.4% slower"
whose own σ is half its mean (chapter 9
has one) is a shrug wearing a number's
clothes.

## Memory readings

The Memory row is the peak resident set:
the most physical memory the process
held at any instant, not an average.
For most commands it barely scatters
(σ of 0.0–0.1 MiB in the lab's runs),
so differences are usually real: when
chapter 6's Python entry shows 10.1 MiB
against grep's 3.5 (+183.9%, *2.8x
more*), that gap is the interpreter's
resident footprint, and it will be there
every run. Read memory factors with the
same reference rule as time: they are
priced against the first command too.

## Run counts are part of the evidence

Hyperfine spends a time budget per
command, so fast commands accumulate
runs (the lab's `grep`: 1,163 runs) and
slow ones stop near the minimum (its
`sort`: 15). That is the right instinct
— a fast command needs more samples to
average out timer noise — and it means
a result based on 10 runs deserves less
confidence than one based on 1,000, all
else equal. The count is printed in the
header precisely so you can weigh it.

## Warnings are part of the result

Hyperfine interrupts its own tables
with warnings when the measurement
smells wrong: a first run far slower
than the rest, a command too fast for
its shell calibration, outliers. They
are not decoration and they are not
failures; they are the tool saying
*this number needs a caveat*. The lab
collected three kinds without trying
(chapters 6, 9 and 15 quote them
verbatim). Repeat in any report you
write the warnings your benchmark
printed — a number whose warning was
trimmed off has been edited, and not in
the reader's favour.

Check: take the table at the top of
this chapter's first section and state,
in one sentence each — what a typical
run cost, how much runs disagreed, and
which single number you would quote for
a rematch. Chapter 5's transcripts
(`t02`, `t05`, `t08`) are good practice
material.
