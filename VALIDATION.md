# Group 7 validation record

Validated locally on 25 September 2026 with Python 3.12.14 on Windows.
Public deployment has been verified. The submission remains a draft until student IDs and actual contributions are confirmed.

## Independent Jupyter execution

All 10 code cells ran in order in a fresh Jupyter kernel.
Execution counts are 1–10; no unhandled error outputs occurred.
Observed total execution time: 371.151 seconds.
The deliverable Notebook contains its real stdout and rich display outputs.
The earlier draft's in-process-only limitation has been resolved.
The simplified experiment and all other code cells were executed in this fresh kernel.
Only an outdated browser-load caveat in Markdown was removed afterward; code and outputs are unchanged.

## Full-grid and candidate verification

| Puzzle | Givens | FC full grid (s) | BC full grid (s) | Result |
|---|---:|---:|---:|---|
| 1 | 30 | 10.018 | 0.362 | PASS |
| 2 | 33 | 10.833 | 0.559 | PASS |
| 3 | 36 | 9.409 | 0.331 | PASS |
| 4 | 39 | 13.316 | 0.572 | PASS |
| 5 | 42 | 11.389 | 0.427 | PASS |

- All five FC and BC grids equal the supplied reference solutions.
- On every puzzle, all 729 Is queries were checked with both algorithms against
  the correct/incorrect candidate expectation: 3,645 candidate pairs, 7,290 assertions.
- Solvers receive only givens; the answer key is used only in validation.
- Three same-puzzle FC runs (s): [10.018, 16.053, 15.718].
- Three same-puzzle BC runs (s): [0.362, 0.438, 0.423].
- Median FC = 15.718 s; median BC = 0.423 s.
- Each full-grid call builds a fresh KB. The supplied FC algorithm resets its
  counters/agenda per candidate query and uses an indexed premise lookup. BC
  reuses proven subgoals and dependency tables across queries within the call.
  These measurements compare the submitted implementations, not inference
  direction alone. The workstation was not CPU-isolated; the per-run values show timing variability.

## Bounded general-KB experiments

- **resolution**: stopped at 30-second wall-time limit; observed wall time 30.025 s.
- **model checking**: stopped at 30-second wall-time limit; observed wall time 30.028 s.

Both original algorithms were actually entered. A separate child process permits
automatic stopping after approximately 30 seconds, including startup and KB construction.
A short psutil loop also monitors resident memory and stops a child above 768 MiB;
this is a sampled guard, not a hard operating-system memory cap. Neither stopping
condition is a Boolean entailment answer. The long Windows Job Object/ctypes code
has been removed. The previous MemoryError result is historical and is not reused.
The Notebook also contains passing small-grid resolution/model-checking examples.

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

## Experiment simplification

Replaced the platform-specific memory-limit code with a 54-line self-contained
experiment using unchanged library calls, a timeout, and a portable memory monitor.
The complete Notebook was rerun in an independent kernel; this document and
experiment_summary.json now report that new run. Core solver/app source and the
previously verified public deployment are unchanged. The original Notebook is backed
up under ../review_materials/before_experiment_simplification_*/.
