# Choosing What to Measure

So far every table has shown the two
default **metrics**: wall time and peak
memory. Hyperfine can collect more, and
some of the most useful questions —
*is it waiting or working? is it using
one core or all of them?* — are answered
by the other metrics. The outcome of
this chapter: you can choose what a
benchmark measures, and read the CPU
breakdown when it appears.

## The default preset, and the `time` preset

`--metrics` selects what is collected.
A **preset** names a set: `default`
(wall time and peak memory), `time`
(wall, CPU, user and system time), and
`all` (everything the platform offers).
Or name metrics individually, with
optional units —
`--metrics time_cpu,instructions`,
`--metrics memory_peak_resident:MiB,time_wall_clock:ms`.

The lab ran its sorting fixture under
the `time` preset (transcript
`hyperfine-lab/transcripts/t10-metrics.txt`):

```text
$ hyperfine --metrics time --runs 10 'sort -n numbers.txt'
Benchmark 1: sort -n numbers.txt (10 runs)
                  mean     ±       σ          min     …     max
  Wall Time      132.8 ms  ±    24.0 ms     109.5 ms  …   183.2 ms
  CPU time       161.7 ms  ±    15.7 ms     140.7 ms  …   197.1 ms
  User time      150.3 ms  ±    16.0 ms     133.3 ms  …   190.6 ms
  System time     11.4 ms  ±     4.4 ms       6.6 ms  …    18.6 ms
```

Three readings this table offers that
the default one cannot:

- **CPU time exceeds wall time** (161.7
  against 132.8 ms). A single-threaded
  program cannot spend more CPU than
  elapsed time; spending more means the
  work ran on several cores at once, as
  GNU sort does when it splits its
  merging across threads. The signature
  of parallelism, visible without
  opening the program.
- **User against system.** Of the CPU
  time, 150.3 ms is *user* — the
  program's own computation — and only
  11.4 ms is *system*, the kernel
  working on its behalf (reading,
  allocating, writing). A command whose
  system time dominates is spending its
  life asking the operating system for
  things, a different disease with a
  different cure.
- **Wall against CPU, the other way.**
  Had wall time greatly exceeded CPU
  time, the command would have been
  *waiting* — on disk, on network, on
  sleep — rather than working. `sleep
  0.2` from chapter 4 is the pure case:
  201.7 ms of wall, essentially no CPU.

Which metrics land in which export is
covered in chapter 11; in short, the
terminal and the markup exports lead
with the primary metric (wall time by
default), the CSV carries all selected
metrics, and the JSON carries
everything collected regardless.

## Memory, precisely

The memory metric is **peak resident
set size**: the greatest amount of
physical memory the process held at any
one moment, in bytes under the hood and
shown in MiB by default. It is a
high-water mark, not an average and not
a total allocation. Two cautions belong
with it. Pages shared with other
processes (shared libraries, above all)
are counted in each process that maps
them, so adding the peaks of a pipeline
overstates the pipeline's true cost.
And a program that forks helpers has
its peak taken as the process tree's
combined resident high-water mark on
this platform — a reasonable figure,
but one to describe as the tree's, not
a single process's.

## The hardware counters — and this machine's refusal

The `all` preset adds **hardware
counters**: `instructions` retired,
`cpu_cycles`, `cache_references`,
`cache_misses`, `branch_misses`. These
come from the processor itself, counted
by the kernel's performance-events
machinery, and they answer the deepest
form of the speed question — not *how
long* but *how much work, and where it
stalled*. They are also the one part of
hyperfine this guide's lab could not
exercise. Asking for them directly
(transcript t10):

```text
$ hyperfine --metrics instructions,cpu_cycles --runs 5 'sort -n numbers.txt'
Error: Metric 'instructions' is unavailable for 'sort -n numbers.txt'.
Check platform support and hardware-counter permissions.
exit code: 1
```

The sandbox withholds performance
events, as many virtualised and shared
machines do (the kernel setting
`perf_event_paranoid`, container
policies, and hypervisors all gate
them). So the counters are described
here from the documentation and the
tool's help, and labelled as such: on a
machine where you hold the permissions,
the same command produces two more rows
in the table and the same statistics
over them; the reading skills from
chapter 5 apply unchanged. What the lab
could verify is the failure mode, which
is a good one — a clear error naming
the metric and the likely cause, exit
code 1, no silent fallback to a lesser
measurement.

Check: run one of your own commands
under `--metrics time` and state, from
the three time rows alone, whether it
is working, waiting, or parallel — then
check whether that story matches what
you know of the program. That reading,
more than any single mean, is what the
extra metrics are for.
