# Parameters — Lists and Scans

One command is a question; a command
with a varying knob is an investigation.
Hyperfine can take a value out of the
command, substitute a whole list or a
whole range of values in its place, and
benchmark every resulting command as
one comparison. The outcome of this
chapter: you can sweep a setting across
its plausible values and read the shape
of the answer — and you will meet, in
the lab's own results, a case where the
sweep's headline order is a lie told by
one bad run.

## Lists: `-L`

`-L name value1,value2,...` benchmarks
the command once per value, replacing
`{name}` wherever it appears in the
command text. The lab swept the obvious
knob on `gzip` — its compression level,
1 (fastest, loosest) through 9
(slowest, tightest) — over its 8 MB
prose fixture (transcript
`hyperfine-lab/transcripts/t05-parameter-list.txt`):

```bash
hyperfine -L level 1,6,9 'gzip -c -{level} article.txt'
```

```text
Benchmark 1: gzip -c -1 article.txt (40 runs)
  Wall Time     44.4 ms  ±     5.3 ms      41.7 ms  …    75.0 ms
Benchmark 2: gzip -c -6 article.txt (52 runs)
  Wall Time     72.5 ms  ±    28.5 ms      56.5 ms  …   189.8 ms           +63.4%  (1.6x slower)
Benchmark 3: gzip -c -9 article.txt (34 runs)
  Wall Time     67.8 ms  ±    10.5 ms      60.0 ms  …    96.9 ms           +52.9%  (1.5x slower)
```

The broad story is sane: level 1 is
fastest, the higher levels cost about
half again as much time. But look at
benchmarks 2 and 3. Taken by their
means, level 9 (67.8 ms) *beat* level 6
(72.5 ms) — the tighter, harder-working
setting apparently faster, which should
make you suspicious on its face. The
rest of benchmark 2's row explains it:
its slowest run was 189.8 ms, two and a
half times its own typical run — one
interruption, preserved in the
statistics, dragged the mean above
level 9's honest figure. Compare the
**min** column instead (56.5 against
60.0) and the expected order restores
itself: level 6's best run beats level
9's best run, both free of the
interruption. This is chapter 5's
lesson with its sleeves rolled up — in
a sweep, compare rows by min or median
when σ is fat, and treat a mean-only
surprise as a prompt to look, not a
finding.

(The level-1 row also carries the
first-run warning quoted in chapter 7 —
one benchmark can teach two lessons.)

## Scans: `--parameter-scan` and `-D`

Where a list names its values, a scan
generates them: `--parameter-scan name
MIN MAX` steps through the range, and
`-D DELTA` sets the stride (without it,
the step is 1). The lab asked how
sorting scales with input size
(transcript t06), feeding `sort` the
first N lines of its 200,000-number
fixture. The pipe means a shell, so:

```bash
hyperfine -S --parameter-scan lines 50000 200000 -D 50000 \
  'head -n {lines} numbers.txt | sort -n'
```

```text
Benchmark 1: head -n 50000 numbers.txt | sort -n (78 runs)
  Wall Time     35.6 ms  ±     9.2 ms      30.2 ms  …   102.4 ms
Benchmark 2: head -n 100000 numbers.txt | sort -n (43 runs)
  Wall Time     76.7 ms  ±    18.3 ms      63.0 ms  …   168.0 ms          +115.6%  (2.2x slower)
Benchmark 3: head -n 150000 numbers.txt | sort -n (18 runs)
  Wall Time    114.2 ms  ±    17.6 ms     102.6 ms  …   161.7 ms          +221.1%  (3.2x slower)
Benchmark 4: head -n 200000 numbers.txt | sort -n (21 runs)
  Wall Time    162.2 ms  ±    27.6 ms     136.7 ms  …   237.2 ms          +355.8%  (4.6x slower)
```

The shape is the finding: each extra
50,000 lines costs roughly another
39 ms — growth a little worse than
linear (sorting's extra comparison work
showing), and peak memory climbing from
5.5 to 9.3 MiB alongside. A scan turns
"it gets slower with more data" into
"here is the rate, and here is where it
would cross your patience" — the
difference between a worry and a plan.
Decimal ranges work too (`-P delay 0.3
0.7 -D 0.2` timing `sleep {delay}` is
the help text's own example), and the
substituted value can also be used
inside `--env` assignments, so a thread
count, say, can be handed to the program
through its environment as well as its
arguments.

## Grids and names

`-L` may be given more than once, and
hyperfine then benchmarks every
combination — a grid: two compilers by
three optimisation levels is six
benchmarks from one invocation. The lab
ran single-parameter sweeps only, so
grids are described here, not
demonstrated; the mechanics are the
same substitution, multiplied.
Whichever form you use, each
benchmark's name in the report is the
fully substituted command, so a sweep
is self-labelling — and `-n` (chapter
6) can still rename results when the
command text is not the label you want
to publish.

Check: in the t05 sweep, state which
row you would actually quote for level
6, and why it is not its mean. Then
look at t06 and extrapolate, with the
stated rate, what 400,000 lines would
cost — that extrapolation, from real
measured points, is what scans are for.
