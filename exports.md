# Exports

A terminal table evaporates. The
benchmark you will want next month —
when someone asks "did this change make
it slower?" — has to live in a file,
with enough detail to be re-read,
re-plotted, and argued with. That is
what the exports are for. The outcome
of this chapter: one run of the
benchmark produces a table for humans,
a file for spreadsheets, and a complete
record for programs, and you can read
all three back.

## One run, three files

The lab re-ran chapter 6's first two
contestants with all three main exports
attached (transcript
`hyperfine-lab/transcripts/t08-exports.txt`):

```bash
hyperfine -S --warmup 2 -n grep -n awk \
  --export-markdown bench.md \
  --export-json bench.json \
  --export-csv bench.csv \
  'grep -c ERROR log.txt' \
  "awk '/ERROR/ {n++} END {print n}' log.txt"
```

The benchmark runs once; each
`--export-*` writes its file as the
results arrive. Nothing about the
measurement changes — the files are
three renderings of the same runs.

## Markdown: the table for the report

`bench.md`, whole:

```markdown
| Command | Mean Wall Time [ms] | Change | Factor |
|:---|---:|---:|:---|
| `grep` | 1.5 ± 1.1 |  |  |
| `awk` | 15.3 ± 6.6 | +922.5% | (10.2x slower) |
```

This is the paste-into-the-document
form: mean ± σ for the primary metric,
the change and factor against the first
command, ready for a pull request, a
wiki page, or a release note. Two more
markup exports exist in the same
spirit — `--export-asciidoc` and
`--export-orgmode` — listed here from
the documentation; the lab exercised
the Markdown one.

## CSV: the summary for spreadsheets

One row per command, one column per
statistic, for every selected metric:

```text
command,time_wall_clock_unit,time_wall_clock_mean,time_wall_clock_stddev,time_wall_clock_median,time_wall_clock_min,time_wall_clock_max,memory_peak_resident_unit,...
grep,s,0.0016970516290592357,0.0033922111163101508,0.0007017984200000003,0.0005364664200000003,0.025731667420000003,B,...
awk,s,0.01776618564666666,0.009331486452651803,0.012863866920000001,0.01040678142,0.054221122420000001,B,...
```

(the full header is in the transcript).
Two things to notice. The values are in
base units — seconds and bytes, named
in the `*_unit` columns — not the
milliseconds and mebibytes the terminal
chose for readability; a spreadsheet
can rescale, a human reading raw CSV
must remember to. And the CSV carries
the **median**, which the terminal
table omits: this is where chapter 5's
grep skew lives (mean 0.00170 s against
a median of 0.00070 s — the mean is
nearly two and a half medians), visible
only because the export kept it.

## JSON: the complete record

The JSON export is the lab notebook.
Its shape, from the lab's file:

- `schema_version` — 2, so readers can
  depend on the layout;
- `metadata` — the hyperfine version,
  the start time, the platform;
- `primary_metric` — `time_wall_clock`;
- `results` — one entry per command,
  each with the command and its name,
  a `summary` of statistics per metric,
  and `measurements`: **every
  individual run**, every metric, and
  the run's exit code.

It also quietly collects more than the
terminal showed: the summaries include
CPU, user and system time even though
the run used the default preset, so a
JSON saved from an ordinary benchmark
can answer questions you did not know
you would ask. Reading it back takes a
few lines — the lab's
`hyperfine-lab/readback.py`, whose
output closes transcript t08:

```text
$ python3 readback.py
schema 2 | primary metric: time_wall_clock
grep: 574 runs, wall mean 1.70 ms, stddev 3.39 ms, median 0.70 ms, peak memory mean 3.6 MiB
awk: 150 runs, wall mean 17.77 ms, stddev 9.33 ms, median 12.86 ms, peak memory mean 3.9 MiB
```

Because every run is kept, anything
derived can be recomputed: a different
percentile, a histogram, the same
statistics with the first run dropped.
When a benchmark is evidence in an
argument, the JSON is the form that
lets the other side check your working.

## Keeping exports honestly

An export freezes numbers; it cannot
freeze their conditions, and the
metadata it keeps (version, time,
platform) is the beginning, not the
whole, of the context. When you keep a
benchmark that a decision rests on, note
with it the things chapter 14 will
insist on: what else the machine was
doing, whether caches were warm, the
size of the input. Two JSONs from
different afternoons on a shared
machine are two measurements of
different machines, in effect — the
format will not warn you, so the note
has to.

Check: export a benchmark of your own
three ways, and confirm the three files
agree with the terminal table they came
from — same means, same counts — and
that the CSV's median and the JSON's
per-run list let you say something the
terminal did not.
