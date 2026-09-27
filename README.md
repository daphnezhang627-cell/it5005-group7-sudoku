# Group 7 Sudoku — integration branch

This branch integrates `current-assignment` at `be772cc` and is the current work
version. See `INTEGRATION_NOTES.md` for requirements, minimal changes and status.
Do not substitute files from the older Codex project or deploy main as this version.

Use Python 3.12 and install `requirements-notebook.txt` to execute the Notebook.
Run `streamlit run sudoku_app.py` from this directory for the local app.
Only `Sudoku_Assignment.ipynb`, `sudoku_solver.py` and `sudoku_app.py` go in the
student submission. Keep the supplied libraries, puzzles and requirements here
for local execution and Streamlit Community Cloud deployment.

Verification commands (from this directory):

```
python tests/run_notebook.py
python tests/test_regressions.py
python tests/test_app.py
```

The Notebook's two slow general-KB experiment calls are deliberately commented
out after the teammate's recorded interrupted attempts; Run All executes the normal
validation cells. Q1 and Q3 preserve the teammate's latest explanations.

Member IDs and Part B responsibilities are confirmed and recorded. The unreachable
fourth member's unknown information is documented without invented contributions.
Public app (verified): https://daphnezhang627-cell-it5005-group7-sudoku-sudoku-app-grou-s9qpys.streamlit.app/
Deployment uses this integration branch and sudoku_app.py with Python 3.12.
The final submission archive is Group7.zip, containing only the required three files.
