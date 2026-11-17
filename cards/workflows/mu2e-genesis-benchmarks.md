---
xCard:
  card_type: workflow
  version: '0.1'

id: mu2e-genesis-benchmarks
name: Mu2e Genesis AI benchmark suite (optimizer, reporting agent, fast simulation)
description: |-
  Benchmark suite of the Mu2e Genesis phase 1 project that measures its AI components in the MLCommons Science
  benchmark ontology (arXiv:2511.05614: problem specification, dataset, metrics, reference solution,
  documentation, scored by the ontology's rubric) and packages each benchmark as a Codabench competition bundle.
  It benchmarks the Mu2eBO Bayesian optimizer (sample efficiency of batch pickers on standard test problems under a
  fixed evaluation budget and batch size: anytime log-regret and hypervolume progress against random and Sobol
  baselines), the Mu2eBO campaign reporting agent (grounded reports on synthetic optimization campaigns: required
  facts present, every number supported by the tool outputs, no value moved onto the wrong row; tokens and latency
  on zero-cost language models), and the Geant4-free GPU fast simulation (the three metrics of a code revision:
  validity against stock simulation in the Offline validation histograms, throughput against a stock grid slot, and
  cost per event). An agentic optimization case (a natural-language objective driven to a closed campaign, scored
  from the agent's decision traces) is planned. Submissions are results, never code: the scorers re-evaluate what
  they can (test functions from the submitted points, numbers against the frozen facts), so a submission cannot
  claim a better value than it reached. Public cases are synthetic; cases built from Mu2e simulation or campaigns
  are scored privately.

  Steps:
  1. Cases: test problems and budgets (optimizer), seeded synthetic campaigns with their facts and gold claims
     (reporting agent), stock reference histograms per workflow (fast simulation, private).
  2. A solution runs offline: an optimizer campaign (card mu2e-mu2ebo), the reporting agent on each campaign (card
     mu2e-mu2ebo-reporter), or a fast-simulation revision (cards mu2e-beam-fastsim, mu2e-crv-fastsim).
  3. The scorer checks the submission's contract and computes the metrics.
  4. A leaderboard ranks solutions on a bounded primary metric, with weak baselines and the reference solution
     beside them; the same scorer runs inside the Codabench bundle.
  5. The benchmark is self-scored with the ontology's rubric and re-scored whenever a verified fact changes.

science:
  - particle-physics
keywords:
  - mu2e
  - benchmark
  - ai benchmark
  - mlcommons science benchmark ontology
  - codabench
  - bayesian optimization benchmark
  - sample efficiency
  - hypervolume
  - llm agent evaluation
  - grounded report generation
  - hallucination check
  - fast simulation validation
  - surrogate modeling
  - reproducibility
  - genesis mission
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.0.0'
last_updated: '2026-11-17'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2e-xcards/blob/main/LICENSE

datasets: []
relationships:
  - type: has_part
    target: mu2e-mu2ebo
    target_label: Mu2eBO closed-loop Bayesian optimization (benchmarked optimizer)
  - type: has_part
    target: mu2e-mu2ebo-reporter
    target_label: Mu2eBO campaign reporting agent (benchmarked agent)
  - type: has_part
    target: mu2e-beam-fastsim
    target_label: Mu2e muon-beam and conversion-electron fast simulation (benchmarked)
  - type: has_part
    target: mu2e-crv-fastsim
    target_label: Mu2e CRV fast simulation (benchmarked)
  - type: references
    target: mu2e-run1-optimization
    target_label: Mu2e Agentic Run-1 Experiment Optimization Workflow (the workflow these benchmarks serve)
---

# Mu2e Genesis AI benchmark suite

The Mu2e Genesis phase 1 project measures its AI components the way the Genesis benchmarks site does: each
benchmark has the five elements of the MLCommons Science benchmark ontology, a self-score on its rubric, and a
Codabench competition bundle validated locally. The suite's source is a Mu2e repository that is not public yet; the
fast-simulation benchmark lives in the public fast-simulation repository
([RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim), `benchmarks/`).

## Benchmarks

| Benchmark | Measures | Submission | Scored from |
|---|---|---|---|
| Optimizer sample efficiency | how fast a batch optimizer closes the gap to the optimum (simple regret or hypervolume) under a fixed budget and batch size, on Branin, Branin-Currin and a held-out Hartmann-6 | the evaluated points, per round | the test functions, re-evaluated at the submitted points |
| Grounded campaign reports | whether a report states the campaign's key facts, supports every number with a tool output, and keeps each value on its own row; tokens and latency | one report per synthetic campaign, plus token usage | the frozen facts and gold claims; the reporting agent's own number check, vendored unchanged |
| Fast-simulation revision | validity in the Offline validation histograms against stock (same events, shapes, paired shards, yields), both float precisions; throughput against a stock grid slot; cost per event (private) | binned histograms and a timing file | hidden stock reference histograms and their reseeded-stock floor |
| Agentic optimization (planned) | task success on natural-language objectives and constraint scenarios, steps, tokens, cost, trace completeness | the agent's run directory and its campaign records | the re-evaluated campaign points and the decision trace |

## Access and limitations

- The bundles are prepared for the Genesis Benchmarks site but not uploaded; results are kept by the project.
- Mu2eBO repeats from an empty board are identical (its picks are seeded by index), so the optimizer benchmark does
  not measure Mu2eBO's run-to-run spread.
- Results that involve Mu2e simulation or campaigns are Mu2e results and are not published through this card.
