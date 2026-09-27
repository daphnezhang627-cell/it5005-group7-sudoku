# Group 7 integration branch

Base: current-assignment at 7cf5850. The three source assignment files matched
those supplied for review from Desktop/11 byte for byte.

## Changes in this commit

Only Sudoku_Assignment.ipynb is changed, alongside this explanatory file.
The teammate solver, Streamlit app, teacher libraries, puzzles and requirements
are unchanged. Neither main nor current-assignment is modified.

- Retain the teacher-style example query (1, 1, 1), and comment the expensive
  model-checking call again so Run All completes. Manual bounded experiments
  remain explicitly documented; no manual run or timing is invented.
- Fill Q1–Q5 with English explanations matched to the received implementation;
  Q3 explicitly identifies outstanding correctness issues rather than claiming
  they are fixed.
- Preserve the three known student IDs and record CHOOG SHENG HONG's confirmed
  non-participation, inability to contact him, and notification to the instructor.
  Contributions of the three participating members still await confirmation.
- FANG XUYI's ID uses the earlier user-supplied A0353826W. The branch originally
  supplied A0353836W; this discrepancy is explicitly marked for confirmation.
- Keep the teacher's first-puzzle validation and add validation of puzzles 2–5.
- Execute all eight code cells in a fresh Python 3.12 Jupyter kernel; save actual
  outputs. All five FC/BC grids and 3,645 BC candidate queries passed.
  Slow resolution/model-checking calls are commented out during this run.
- Add the real existing Streamlit URL, explicitly noting that it runs the earlier
  main version, not this proposed teammate-based integration.

## Outstanding work before merge/submission

- Correct BC duplicate-premise counting, stale tables after KB tell/retract,
  and recursive answer propagation on long dependency chains.
- Clear app results when switching puzzles, rather than only hiding them.
- Rerun tests and update Q3/timings after solver fixes.
- Confirm the student-ID discrepancy and actual contribution statements.
- Review together, then merge to main and verify the updated public app.

This is a review draft, not a final submission. No solver/app fix is claimed in
this commit. The existing live app is unaffected by this branch push.
