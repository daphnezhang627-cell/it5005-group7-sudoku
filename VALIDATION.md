# Group 7 validation record

Notebook revalidated locally on 27 September 2026 with Python 3.12.14 on Windows.
The inference and Streamlit regression checks below were performed on 25 September; those source files are unchanged.
Public deployment has been verified. The submission remains a draft until student IDs and actual contributions are confirmed.

## Independent Jupyter execution

All 10 code cells ran in order in a fresh Jupyter kernel.
Execution counts are 1–10; no unhandled error outputs occurred.
Observed total execution time: 373.985 seconds.
The deliverable Notebook contains its real stdout and rich display outputs.
The earlier draft's in-process-only limitation has been resolved.
The general-KB cell now follows the teacher's uncomment/run/interrupt template.
Both expensive calls are commented out during Run All. Their actual historical
bounded-run observations are explicitly attributed to the 25 September experiment.
This Run All verifies the remaining cells, including all five FC/BC grids and queries.

## Full-grid and candidate verification

| Puzzle | Givens | FC full grid (s) | BC full grid (s) | Result |
|---|---:|---:|---:|---|
| 1 | 30 | 14.571 | 0.538 | PASS |
| 2 | 33 | 16.730 | 0.460 | PASS |
| 3 | 36 | 15.411 | 0.561 | PASS |
| 4 | 39 | 13.018 | 0.426 | PASS |
| 5 | 42 | 12.040 | 0.466 | PASS |

- All five FC and BC grids equal the supplied reference solutions.
- On every puzzle, all 729 Is queries were checked with both algorithms against
  the correct/incorrect candidate expectation: 3,645 candidate pairs, 7,290 assertions.
- Solvers receive only givens; the answer key is used only in validation.
- Three same-puzzle FC runs (s): [14.571, 18.314, 17.432].
- Three same-puzzle BC runs (s): [0.538, 0.466, 0.483].
- Median FC = 17.432 s; median BC = 0.483 s.
- Each full-grid call builds a fresh KB. The supplied FC algorithm resets its
  counters/agenda per candidate query and uses an indexed premise lookup. BC
  reuses proven subgoals and dependency tables across queries within the call.
  These measurements compare the submitted implementations, not inference
  direction alone. The workstation was not CPU-isolated; the per-run values show timing variability.

## Historical bounded general-KB experiments (25 September)

- Resolution: no Boolean result before stopping at 30.025 s.
- Model checking: no Boolean result before stopping at 30.028 s.

Both supplied algorithms were entered, unchanged. These are historical observations
from automatic child-process limits, including startup and KB construction, not
new measurements from manually interrupting a Jupyter cell. Neither reached the
sampled memory stopping condition in that run. The original executed Notebook and
reports are preserved in ../review_materials/before_teacher_alignment_*/.
The current Notebook removes that wrapper and presents direct commented calls,
as instructed by the teacher. Run one call at a time, interrupt after about 30
seconds if needed, and record actual observations. Run All skips those calls.
Small-grid resolution/model-checking correctness assertions still execute and pass.

## Additional inference regression checks

- Five explicit cyclic-rule cases: no self-supporting truth and no premature
  negative cache preventing a later externally grounded proof.
- 2,400 FC/BC comparisons over 100 deterministic random Horn KBs, including
  reversed query orders with fresh proof tables.
- Cache invalidation after tell/retract on generic and indexed KBs.
- A 3,000-rule dependency chain and its 3,001-node proof.
- 810 Sudoku proof DAGs checked against actual KB rules, facts and prerequisite order.
- Empty 4×4 puzzles remain unresolved under both methods; 1×1 grids work.
- Eight malformed-input cases rejected.
- logic_.py, utils.py and puzzles.json match the teacher files byte-for-byte.
- Protected atom and Notebook loader are unchanged.
- Solver imports only utils and logic_; the app and Notebook do not duplicate core functions.

## Streamlit verification

Streamlit AppTest passed initial rendering, all five puzzle selectors, both complete
solvers on all five puzzles, elapsed-time display, given/deduced board classes,
true/false queries, proof slider and supporting cards, stale-result clearing after
puzzle changes, and clearing an earlier success when a new solve fails.
An empty 4×4 fixture verified the distinction between unknown and explicitly excluded.

Real headless Microsoft Edge checks exercised the local HTTP app: initial board,
BC solving, true proof, false exclusion proof, switching puzzles, and a 390px mobile
viewport. Screenshots and browser status are saved in validation_outputs.
The first browser attempts found a test-control issue (editable combobox focus did
not open the menu); the test now opens the actual menu with ArrowDown and selects
its option. This did not require an inference or puzzle-state change.
Visual inspection found the top label behind Streamlit's header; app spacing was fixed.

## Changes from the supplied completed draft

- Preserved the existing solver implementation after code review and regression tests.
- Merged Group 7 and the four member names without inventing IDs or contributions.
- Made bounded Notebook experiments work on Windows, expanded all-candidate FC checks
  to every puzzle, added cyclic-proof regression checks, and saved fresh-kernel outputs.
- Cleared stale solve results on failure and fixed the app's header spacing.
- Updated execution instructions, added reproducible tests and a guarded packaging script.
- Original completed-project files are backed up outside the project in
  ../review_materials/complete_project_original.zip.

## Remaining submission requirements

1. CHOOG SHENG HONG's student ID. The other three IDs have been supplied and recorded.
2. User confirmation of each member's actual contribution; CHOOG SHENG HONG remains
   recorded as not yet contacted, with no invented testing contribution.
Public deployment is complete and verified; the real URL is saved in the Notebook.

No public URL is invented. Group7_DRAFT.zip contains only Group7/ with the three
required files and is explicitly not ready for submission. The packaging script
refuses final Group7.zip while required information or deployment evidence is missing.

## Public deployment verification

URL: https://daphnezhang627-cell-it5005-group7-sudoku-sudoku-app-lkd5pg.streamlit.app/

Checked: 2026-09-25T13:51:15.939Z. Fresh unauthenticated Edge session.

- Puzzle 1: both solvers, exact grid, elapsed time, true/false queries, proof controls and switch reset PASS
- Puzzle 2: both solvers, exact grid, elapsed time, true/false queries, proof controls and switch reset PASS
- Puzzle 3: both solvers, exact grid, elapsed time, true/false queries, proof controls and switch reset PASS
- Puzzle 4: both solvers, exact grid, elapsed time, true/false queries, proof controls and switch reset PASS
- Puzzle 5: both solvers, exact grid, elapsed time, true/false queries, proof controls and switch reset PASS

No JavaScript page errors occurred. The 390px mobile board fits the viewport.
Cloud solve times (displayed by the application):

| Puzzle | Method | Time |
|---|---|---|
| 1 | Backward chaining | 0.635 s |
| 1 | Forward chaining | 25.865 s |
| 2 | Backward chaining | 0.745 s |
| 2 | Forward chaining | 23.922 s |
| 3 | Backward chaining | 0.613 s |
| 3 | Forward chaining | 21.471 s |
| 4 | Backward chaining | 0.605 s |
| 4 | Forward chaining | 18.472 s |
| 5 | Backward chaining | 0.642 s |
| 5 | Forward chaining | 16.925 s |

The public app is inside Streamlit Cloud's streamlitApp iframe. The browser test
waits for the iframe and lazy-loaded controls before asserting. Early locator/loading
failures were corrected in the test harness; application source did not change.
Only Notebook Markdown was edited to add the URL; executed code and outputs are unchanged.

## Member information update

Three student IDs and the agreed task allocation have been recorded in the Notebook.
Responsibilities are explicitly planned assignments, not confirmed completed contributions.
CHOOG SHENG HONG remains uncontacted; no completed work is attributed to this member.
Code cells and saved execution outputs were preserved unchanged.

## Teacher-template alignment (27 September)

Removed automatic timeout and memory-monitor code from the deliverable Notebook.
Preserved attributed historical slow-experiment observations and updated Q2.
Ran the revised Notebook in a fresh independent Jupyter kernel and updated FC/BC
outputs and the measurements above. The teacher libraries, solver and app are
unchanged; their previous deployment and regression results remain applicable.
