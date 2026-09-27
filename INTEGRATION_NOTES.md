# Group 7 integration record

Work branch: `group7-integration`. Teammate baseline: `current-assignment` at
`be772cc` (28 September review). This incorporates the teammate's latest three
commits: iterative BC proof propagation, Q3 and responsibility updates, and Q1.
The downloaded `Sudoku_Assignment (3).ipynb` matches this remote notebook's cells.
Neither `main` nor `current-assignment` is modified by this work.

## Necessary changes from the teammate baseline

- BC: invalidate cached inference records when the KB clauses change, and count
  distinct premises consistently with the waiting sets. These fix demonstrated
  incorrect answers after tell/retract and for duplicate premises. The teammate's
  iterative proof propagation and existing algorithm structure are retained.
- FC: report an unresolved cell instead of returning an incomplete grid as a full
  solution. Provided puzzles still solve with the supplied `pl_fc_entails`.
- App: clear old results on puzzle changes, including when returning to a prior
  puzzle. The existing ProofSet instrumentation and reasoning display are retained.
- Notebook: preserve Q1/Q3, latest planned allocation, teacher example and the
  teammate's Observation. Add the Horn expressive-limit clarification to Q1;
  update Q3 only for cache invalidation, distinct premises and correctness.
  Complete Q2/Q4/Q5 and execute all normal cells in an independent kernel.
- Additional tests and records are for review only, not the three-file submission.

No optimization rewrite, new solver abstraction, or teacher library modification
is introduced. No answers are read to solve: solutions are used only by tests.
The original example's slow calls stay commented after its recorded interruptions.
The reported ~0.2 seconds describes KB construction, not inference.

## Requirement mapping

| Requirement | Implementation/evidence | Status |
|---|---|---|
| General CNF KB | sudoku_solver.py build_general_kb; Q1 | Implemented |
| Definite KB | build_definite_kb; Q1 | Implemented |
| Library FC full grid | solve_full_grid_fc; Notebook tests | Verification in validation_outputs |
| Student BC, cycles, full grid | pl_bc_entails, solve_full_grid_bc; regression tests | Verification in validation_outputs |
| Bounded resolution/model checking | Teacher example and preserved Observation | Teammate's reported interruptions preserved; not rerun |
| All five puzzles, candidates, timings | Notebook validation cells | Fresh-kernel output in Notebook |
| Q1–Q5 | Part B | Filled, matched to current code |
| Select puzzle, display givens, FC/BC/time | sudoku_app.py | PASS: AppTest and real Edge, all five puzzles |
| BC query and actual reasoning | ProofSet, build_proof, query UI | Proof DAG and UI tests |
| Protected files/functions/imports | tests/test_regressions.py | Byte/AST comparison |
| Community Cloud integration branch | share.streamlit.io | Pending account-side deployment and public verification |
| Member information | Notebook group section | FANG XUYI ID conflict and actual contributions pending |
| Exactly three files under Group7 | packaging check | Draft only until remaining requirements resolved |

## Deployment

Required source: repository `daphnezhang627-cell/it5005-group7-sudoku`, branch
`group7-integration`, entry `sudoku_app.py`. Six runtime files remain together.
Do not confuse the earlier main deployment with verified integration deployment.
Keep the older app if a new deployment is necessary; do not delete it.
