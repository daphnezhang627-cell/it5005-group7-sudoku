"""Execute the deliverable in a fresh project Jupyter kernel; save real outputs."""
from pathlib import Path
import os
import sys
import json
import time
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpec

project = Path(__file__).resolve().parents[1]
os.chdir(project)
artifacts = project / 'validation_outputs'
artifacts.mkdir(exist_ok=True)
for name, folder in [('JUPYTER_RUNTIME_DIR', 'jupyter_runtime'),
                     ('IPYTHONDIR', 'ipython'), ('JUPYTER_CONFIG_DIR', 'jupyter_config')]:
    directory = artifacts / folder
    directory.mkdir(exist_ok=True)
    os.environ[name] = str(directory)
km = KernelManager(kernel_name='python3')
km._kernel_spec = KernelSpec(argv=[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
                             display_name='Group 7 project Python', language='python')
nb_path = project / 'Sudoku_Assignment.ipynb'
notebook = nbformat.read(nb_path, as_version=4)
nbformat.validate(notebook)

class ReportingClient(NotebookClient):
    def process_message(self, msg, cell, cell_index):
        if msg['msg_type'] == 'stream':
            print(msg['content']['text'], end='', flush=True)
        return super().process_message(msg, cell, cell_index)

client = ReportingClient(notebook, km=km, timeout=1200, allow_errors=False,
                         resources={'metadata': {'path': str(project)}})
start = time.perf_counter()
try:
    client.execute()
finally:
    nbformat.write(notebook, nb_path)
    nbformat.write(notebook, artifacts / 'executed_notebook.ipynb')
counts = [c.execution_count for c in notebook.cells if c.cell_type == 'code']
assert counts == list(range(1, len(counts) + 1))
assert not [o for c in notebook.cells for o in c.get('outputs', []) if o.output_type == 'error']
# The notebook outputs are the primary evidence; this report records execution status.
report = {'python': sys.version, 'interpreter': sys.executable,
          'execution_counts': counts, 'code_cells': len(counts),
          'wall_seconds': time.perf_counter() - start,
          'status': 'PASS: all code cells ran in a fresh independent Jupyter kernel'}
(artifacts / 'notebook_execution.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2), flush=True)
