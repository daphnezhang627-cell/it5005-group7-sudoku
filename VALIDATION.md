# Validation — 28 September 2026

Baseline: teammate current-assignment at be772cc; work branch group7-integration.
Python 3.12.14; supplied runtime dependencies unchanged.

## Fresh independent kernel

All 9 normal code cells ran in order; no error outputs.
Elapsed full Notebook time: 95.065 seconds.
The slow general-KB calls stay commented as permitted by the template.
The teammate's recorded Observation on Is1_1_1 is preserved verbatim; it is a
reported interrupted experiment, not remeasured in this run. Its 0.2 seconds
is explicitly KB construction time. No timeout is interpreted as False.
Only the Q4 notation clarification and pending deployment/member Markdown may
change after execution; all code and outputs remain matched to the executed snapshot.

| Puzzle | FC seconds | BC seconds | Exact reference grid |
|---|---:|---:|---|
| 1 | 14.82 | 0.68 | PASS |
| 2 | 18.795 | 0.637 | PASS |
| 3 | 18.454 | 0.660 | PASS |
| 4 | 18.348 | 0.616 | PASS |
| 5 | 16.513 | 0.618 | PASS |

All five complete FC/BC grids and 3,645 BC correct/incorrect candidate queries
passed. Timings include fresh KB construction for each solver call. One sample
per puzzle/method is recorded; no claim of universal BC superiority is made.

## Regression checks

- Ungrounded and externally grounded cycles, duplicate premises, and cache reset
  after adding/retracting facts pass.
- 3,000-rule chain terminates without recursive proof-propagation overflow.
- 1,000 random Horn queries match the teacher FC on a duplicate-free equivalent
  reference KB; raw duplicate rules were removed from the FC reference to avoid
  its repeated-counter-notification behavior. No teacher code is modified.
- 810 successful positive/exclusion proof DAGs checked for actual KB rules,
  fact roots, and prerequisite order.
- 50 direct FC/BC Sudoku correct/incorrect query comparisons pass.
- Both methods reject an underdetermined empty 4x4 grid instead of guessing.
- Supplied logic_.py, utils.py and puzzles.json are byte-identical to originals.
  atom and load_pool ASTs are unchanged; solver imports only utils and logic_.

## UI checks

Streamlit AppTest passes all five puzzle selectors, both solvers' exact grids,
positive/negative queries and nonempty reasoning. Switching away and back clears
results. An empty 4x4 fixture distinguishes no proof from explicit exclusion.
A real Edge browser test report is recorded separately in browser_tests.json.
Public integration-branch deployment is not yet verified; the older app is not
claimed as validation of this version.

## Submission status

Pending FANG XUYI's ID conflict, actual contribution confirmation, and Cloud
configuration/public verification of group7-integration. CHOOG SHENG HONG is
recorded as uncontacted with ID/contribution unconfirmed, following the latest
user instruction. Only a clearly named draft ZIP may be produced at this stage.
