# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's traffic is the lab talking to itself.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 14 names what the tool
   cannot do: it times whole invocations and cannot say why
   they take the time they take, its numbers belong to the
   machine and moment that produced them, caches are a state
   the measurer chooses, output is discarded by default and
   some commands notice, the memory figure is a peak and an
   approximation, and a command run one at a time says nothing
   about a service under concurrent load.
8. **The honesty rule is in the text, early.** Chapter 1 and
   the README state the rule plainly — *a benchmark is a claim:
   measure the job you actually care about, on data like the
   real data, and report the spread next to the winner* —
   before any procedure depends on it, and later chapters point
   back to it where a warm cache, a loaded machine, or a
   trimmed warning would manufacture the winner you wanted.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox.
Hyperfine **2.0.0** was downloaded as the official release
tarball from the project's GitHub releases and unpacked into a
scratch folder — no system-wide install. All transcripts live
in `hyperfine-lab/transcripts/`. The fixtures are the lab's
own, generated deterministically (fixed seeds) by
`hyperfine-lab/make_fixtures.py`: an invented 50,000-line
server log (5% ERROR lines), 200,000 shuffled integers, and
8 MB of invented prose, plus its gzip-compressed form.

Run for real, with transcripts as evidence:

- Version printout of the release binary (t00), and a first
  benchmark of `sleep 0.2`: 14 runs, 201.7 ms ± 0.2 (t01).
- The same-answer check before any racing: `grep -c`,
  `awk`, and the lab's `count_errors.py` all print 2,471 on
  the fixture log (t02a).
- The three-way comparison with `-S`, `--warmup 2` and `-n`
  names (t02): grep 1.8 ms, awk 22.6 ms (12.2x slower),
  python3 34.5 ms (18.7x slower, 2.8x the memory) — including
  hyperfine's own verbatim warning that the sub-5-ms command
  strains its shell calibration.
- Run-count control: `sort` left to choose (15 runs,
  273.0 ± 103.2 ms) and rerun with `--warmup 2 --runs 20`
  (242.7 ± 74.5 ms) (t03).
- Shell pricing: `sleep 0.05` with no shell (52.8 ms), with
  `-S` (54.3 ms), and with `--shell 'bash --norc'` (52.0 ms)
  (t04).
- A parameter list: `-L level 1,6,9` over gzip (t05),
  including the first-run-slower warning verbatim and a real
  misleading row — level 9's mean below level 6's because one
  189.8 ms outlier bent level 6's statistics.
- A parameter scan: `--parameter-scan lines 50000 200000
  -D 50000` over a sort pipeline (t06): 35.6 / 76.7 / 114.2 /
  162.2 ms, memory 5.5 → 9.3 MiB.
- `--prepare` restoring a fresh input copy before every run
  and `--cleanup` deleting it afterwards, proven by a
  following failed `ls` in the same transcript (t07), plus
  the adapted first-run warning that notes a prepare is
  already in use.
- Exports of one benchmark to Markdown, CSV and JSON, all
  three files read back in the transcript (t08); the JSON
  (schema 2) read with the lab's `readback.py`, showing
  grep's mean of 1.70 ms against its median of 0.70 ms.
- Noise, demonstrated deliberately: two `yes` processes
  pinning both CPUs moved the same sort from 108.6 ± 8.6 ms
  (quiet) to 256.3 ± 32.9 ms (loaded), same session,
  `--runs 12` both times (t09).
- The `time` metrics preset (t10): wall 132.8 ms, CPU
  161.7 ms — more CPU than wall, the multi-core signature —
  user 150.3 ms, system 11.4 ms.
- The exit-code trap (t90): a `grep` that finds nothing
  exits 1 and hyperfine refuses, verbatim; `-i` benchmarks it
  with the "Ignoring non-zero exit code" warning.

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- The hardware counters (`instructions`, `cpu_cycles`,
  `cache_references`, `cache_misses`, `branch_misses`): the
  sandbox refuses them, and the refusal itself is the
  transcript (t10: "Metric 'instructions' is unavailable …
  Check platform support and hardware-counter permissions",
  exit code 1). Their meaning is described; no counter
  numbers are presented as measured.
- Cache-clearing `--prepare` commands (dropping the kernel's
  page cache needs administrator rights the lab did not use);
  the `--prepare` mechanism itself was run for real with a
  file restore.
- `--setup` and `--conclude` (the per-set and per-run
  housekeeping slots); `--prepare` and `--cleanup` were run.
- Multiple `-L` options combined into a grid; the single-list
  and single-scan substitutions were run.
- `--export-asciidoc` and `--export-orgmode`; the Markdown,
  CSV and JSON exports were run and read back.
- Install routes other than the release tarball (package
  managers, Cargo), and behaviour on Windows and macOS,
  including `cmd.exe` as the platform shell.
- The neighbouring tools of chapter 13 (`time`,
  `/usr/bin/time`, `perf`, `timeit` and other in-language
  harnesses, load-testing tools) are characterised, not
  benchmarked.

Fixtures are this guide's own and deliberately generic: an
invented log from invented workers, shuffled integers, and a
paragraph about a harbour office, repeated. No example is
modelled on any real person, machine, network, service or
organisation, and every benchmark the lab ran measured the
lab's own commands on the lab's own machine.

One honesty note the guide makes about itself: the build
machine is shared, so its absolute numbers wander between
transcripts (the same sort reads 273 ms in t03 and 109 ms in
t09's quiet half). The guide uses that scatter as teaching
material rather than re-running until the numbers look calm;
comparisons the text draws conclusions from were always made
inside a single transcript, back-to-back.
