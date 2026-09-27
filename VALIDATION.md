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
Only the Q4 notation clarification and deployment/member Markdown may
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
Real Edge browser checks passed all five puzzles with both solvers, exact displayed
grids, givens, true/false queries, expanded proof text, switching and a 390px
mobile layout, with no JavaScript page errors. See browser_tests.json.
Initial browser checks were corrected to wait for Streamlit rerender completion;
these were test synchronization changes, not additional application changes.
Public integration-branch deployment also passed the same browser suite.
URL: https://daphnezhang627-cell-it5005-group7-sudoku-sudoku-app-grou-s9qpys.streamlit.app/
Repository: daphnezhang627-cell/it5005-group7-sudoku; branch: group7-integration;
entrypoint: sudoku_app.py; Python: 3.12. Runtime source commit: 5beb71d.
All six runtime file hashes match runtime_manifest.json and this submission.
Cloud FC times were 29.29, 35.84, 27.04, 26.33, 23.67 seconds; BC times were
0.83, 1.04, 0.83, 0.84, 1.06 seconds. These are separate from Notebook timings.
See public_deployment.json. The older main app is retained.

## Submission status

The three participating members' IDs and Part B responsibilities are confirmed.
CHOOG SHENG HONG is unreachable and the instructor has been informed; his
ID/contribution remain unconfirmed. Other individual contributions are not invented.
Cloud verification passed. Group7.zip contains exactly the three required files
under Group7/. No unresolved deployment or confirmed-member metadata blocker remains.
