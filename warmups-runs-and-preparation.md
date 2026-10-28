# Warmups, Runs and Preparation

Left alone, hyperfine makes sensible
choices: how many runs, in what state,
on a machine as it finds it. This
chapter hands you the controls, and the
outcome is that you can say — for any
benchmark you run — *in what state the
measured runs began, and how many of
them there were.*

## Warmups: let the machine settle

The first time a command runs, it pays
costs no later run pays: the program
and its file are read from disk into
the memory cache, libraries are mapped,
caches inside the program fill. Measure
that run and you have benchmarked the
warming, not the work. `--warmup N`
runs the command N times untimed,
first, so the timed runs all start from
the settled state. Hyperfine will tell
you when you needed one and skipped it.
From the lab's gzip benchmark
(transcript
`hyperfine-lab/transcripts/t05-parameter-list.txt`):

```text
  Warning: The first benchmarking run for this command was
  significantly slower than the rest (75.0 ms). This could be
  caused by (filesystem) caches that were not filled until
  after the first run. You should consider using the '--warmup'
  option to fill those caches before the actual benchmark.
  Alternatively, use the '--prepare' option to clear the
  caches before each timing run.
```

Note what the warning does: it *excludes
nothing and hides nothing* — the slow
run stays in the statistics, and the
warning flags it. The two remedies it
names are the two honest positions:
warmup if your real-world use is warm
(a tool you run all day), prepare-clears
if your real-world use is cold (a
nightly job on a fresh machine). Picking
the one that flatters your favourite
command is the chapter 1 rule, broken.

## How many runs

Three knobs: `--runs N` (exactly N),
`--min-runs` and `--max-runs` (bounds on
hyperfine's own choice). The default
choice adapts — fast commands get many
runs, slow ones few — and transcript t03
shows both halves of that sentence. A
left-alone `sort` of the lab's 200,000
numbers:

```text
Benchmark 1: sort -n numbers.txt (15 runs)
  Wall Time    273.0 ms  ±   103.2 ms     155.9 ms  …   490.9 ms
```

Fifteen runs, a mean of 273 ms — and a
σ of 103 ms, over a third of the mean,
because the lab machine is shared and
other work came and went during those
four seconds. The rerun with the knobs
turned, `--warmup 2 --runs 20`:

```text
Benchmark 1: sort -n numbers.txt (20 runs)
  Wall Time    242.7 ms  ±    74.5 ms     143.1 ms  …   379.1 ms
```

More runs narrowed the picture
somewhat; they did not and cannot fix
the scatter, because the scatter is the
machine, not the sampling. That is the
honest lesson of run counts: more runs
describe the noise better; they do not
remove it. When σ stays huge no matter
what you set, the answer is a quieter
machine or a less ambitious claim —
chapter 15 shows the same command with
its noise source found and removed.

## Preparation: the same starting line, every run

Some commands change the world they
measure: a decompressor consumes its
input, a compiler leaves objects
behind, a cache fills. `--prepare CMD`
runs CMD — untimed — before **each**
timed run, so every run starts from the
same state. The lab's decompression
benchmark (transcript t07) needs its
input file restored every time, so:

```bash
hyperfine --prepare 'cp article.txt.gz work.gz' \
          --cleanup 'rm -f work.gz' \
          'gzip -dc work.gz'
```

```text
Benchmark 1: gzip -dc work.gz (28 runs)
  Wall Time     46.1 ms  ±    13.8 ms      37.6 ms  …    93.2 ms
```

The prepare copy is not in the 46.1 ms;
only the decompression is timed.
(The warning this run printed is quoted
in chapter 15 — hyperfine noticed the
first run was still slow and observed,
correctly, that the prepare was not a
cache-clearing one.)

The classic prepare is the opposite of
a warmup: clearing the filesystem cache
(`sync; echo 3 | sudo tee /proc/sys/vm/drop_caches`
on Linux) so every run is a cold run.
The lab did not run that form — it
needs administrator rights the lab did
not use — and the guide labels it
documented-only; the pattern is the
option above with a different command.

## Setup, conclude, cleanup: the other three

Four housekeeping slots exist, and
their difference is *when*:

- `--setup CMD` — once, before a
  command's whole set of runs. The
  place for compiling the program under
  test with the current parameters.
- `--prepare CMD` — before every run
  (above).
- `--conclude CMD` — after every run.
  The place for stopping something a
  prepare started, such as a server.
- `--cleanup CMD` — once, after a
  command's runs are done. The lab's
  t07 used it to delete the scratch
  file, and proved it in the same
  transcript: a following `ls work.gz`
  reports *No such file or directory*.

Setup and conclude are described here
from the documentation; the lab ran
prepare and cleanup for real. All four
run through a shell even when the
benchmarked command does not (chapter
8), since they are given as command
lines, not programs.

Check: for one of your own commands,
name which slot each piece of
housekeeping belongs in — build it
(setup), reset its input (prepare),
stop its helper (conclude), remove its
outputs (cleanup) — and which of your
runs should be warm and which cold.
That naming is most of benchmarking
hygiene; the flags are the easy part.
