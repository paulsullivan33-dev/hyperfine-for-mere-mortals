# Recipes

Short forms for the jobs hyperfine is
actually hired for. Each recipe is an
application of a mechanism an earlier
chapter verified; where a recipe uses
an option the lab only described, it
says so.

## "Which of these two settings wins?"

Sweep the setting, keep the rest of the
command frozen (chapter 9):

```bash
hyperfine -L opt 1,2,3 './build --level {opt} && ./run-trial'
```

— except that `&&` needs a shell, so add
`-S`, and give the pair a `--warmup 1`
so the first setting is not paying for
everybody's cold cache. Read the result
by min or median if σ is fat, and
remember the reference is the first
value in your list: put the current
setting first, so the table reads as
"challengers against the incumbent".

## "Did my change make it slower?"

Benchmark the old and new invocations
in the **same session**, as one
comparison, then export the JSON:

```bash
hyperfine -n before -n after --export-json bench.json \
  './tool-old data.csv' './tool-new data.csv'
```

Same session is not a nicety: chapter
15's load experiment (transcript t09)
moved one command's mean from 256 ms
to 109 ms by doing nothing but stopping
a background job. A "before" measured
in the morning against an "after"
measured after lunch is measuring the
day, not the change. The JSON is the
record; the note you attach should say
what else the machine was doing.

## "How does it scale?"

A parameter scan over input sizes
(chapter 9, transcript t06):

```bash
hyperfine -S --parameter-scan size 10000 100000 -D 30000 \
  'head -n {size} input.txt | ./tool'
```

Read the *shape*: costs growing in
equal steps suggest linear behaviour;
each step costing more than the last
suggests worse, and the scan's later
points let you estimate where the tool
crosses from "fine" to "a problem"
before production data does it for you.

## "Time a job that eats its input"

Any command that consumes or rewrites
its input needs `--prepare` to rebuild
the starting state before every run
(chapter 7, transcript t07):

```bash
hyperfine --prepare 'cp pristine.db work.db' \
          --cleanup 'rm -f work.db' \
          './migrate work.db'
```

Without the prepare, run two would be
timing an already-migrated database —
usually suspiciously fast, and the
first benchmark lie most people meet.

## "Time one stage of a pipeline"

Quote the whole pipeline and add `-S`;
each stage's cost can then be isolated
by benchmarking the pipeline up to that
stage:

```bash
hyperfine -S 'cat log.txt | grep ERROR' \
             'cat log.txt | grep ERROR | wc -l'
```

The second table's difference from the
first is roughly the added stage's
price — roughly, because pipeline
stages run concurrently, so treat the
difference as an estimate, and if a
stage's own cost is the real question,
benchmark that stage alone on saved
input.

## "Time something that must be started and stopped"

For a server-shaped command, start it
in `--prepare`, and stop it in
`--conclude` (the per-run closing slot
from chapter 7 — described there from
the documentation, as the lab's
subjects all exited on their own):

```bash
hyperfine --prepare './server --port 18080 & sleep 0.3' \
          --conclude 'pkill -f "server --port 18080"' \
          'curl -s http://127.0.0.1:18080/health > /dev/null'
```

Include the startup wait in the prepare
(here, a blunt `sleep 0.3`) so it is not
charged to the timed request, and state
plainly in any report that a fixed
sleep makes the setup an approximation.
Benchmark your own server, on your own
machine — the rule in chapter 1 about
whose jobs you measure has a cousin
here about whose services you prod.
