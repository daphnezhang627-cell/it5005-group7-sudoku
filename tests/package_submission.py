"""Package the three required files; refuse final status if metadata/deployment is pending."""
from pathlib import Path
import json,zipfile,hashlib,argparse
p=Path(__file__).resolve().parents[1];args=argparse.ArgumentParser();args.add_argument('--draft',action='store_true');draft=args.parse_args().draft
names=['Sudoku_Assignment.ipynb','sudoku_solver.py','sudoku_app.py'];n=json.loads((p/names[0]).read_text(encoding='utf-8'));s='\n'.join(''.join(c['source']) for c in n['cells']);code=[c for c in n['cells'] if c['cell_type']=='code']
assert [c['execution_count'] for c in code]==list(range(1,len(code)+1));assert not any(o['output_type']=='error' for c in code for o in c['outputs'])
assert 'https://...' not in s and 'NotImplementedError' not in s
assert not any(''.join(c['source']).strip()=='**Your answer:**' for c in n['cells'])
for name in ['notebook_execution.json','regressions.json','streamlit_tests.json','browser_tests.json']:
 report=json.loads((p/'validation_outputs'/name).read_text());assert report['status'].startswith('PASS'),name
status=json.loads((p/'validation_outputs/status.json').read_text());missing=list(status['missing'])
public=p/'validation_outputs/public_deployment.json'
if not public.exists() or json.loads(public.read_text()).get('status')!='PASS':
 if 'Integration-branch deployment and verification' not in missing:missing.append('Integration-branch deployment and verification')
if not draft and missing:raise SystemExit('Cannot produce submission-ready ZIP: '+ '; '.join(missing))
output=p.parent/('Group7_Integration_DRAFT.zip' if draft else 'Group7.zip')
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
 for name in names:z.write(p/name,'Group7/'+name)
with zipfile.ZipFile(output) as z:
 assert z.namelist()==['Group7/'+name for name in names] and z.testzip() is None
 for name in names:assert z.read('Group7/'+name)==(p/name).read_bytes()
report={'archive':str(output),'status':'DRAFT' if missing or draft else 'READY','missing':missing,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'files':{name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in names}}
(p/'validation_outputs/packaging.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
