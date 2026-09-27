from pathlib import Path
import os,sys,json,random,ast,hashlib
p=Path(__file__).resolve().parents[1];os.chdir(p);sys.path.insert(0,str(p))
from sudoku_solver import *
from logic_ import *
r={}
def check(clauses,q,wanted):
 k=PropDefiniteKB()
 for c in clauses:k.tell(expr(c))
 assert pl_bc_entails(k,expr(q))==wanted
check(['A ==> B','B ==> A'],'A',False)
check(['(A & B) ==> Q','B ==> A','A ==> B','C ==> A','C'],'Q',True)
check(['(A & A) ==> Q','B ==> A','B'],'Q',True)
check([f'P{i+1} ==> P{i}' for i in range(3000)]+['P3000'],'P0',True)
k=PropDefiniteKB();k.tell(expr('A ==> B'));assert not pl_bc_entails(k,expr('B'));k.tell(expr('A'));assert pl_bc_entails(k,expr('B'));k.retract(expr('A'));assert not pl_bc_entails(k,expr('B'))
r['cycle_duplicate_long_chain_cache']='PASS'
g=random.Random(7);count=0
for _ in range(100):
 k=PropDefiniteKB();names=[expr('P'+str(i)) for i in range(10)]
 for name in names:
  if g.random()<.2:k.tell(name)
 for _ in range(25):
  premises=[g.choice(names) for _ in range(g.randint(1,3))];k.tell(associate('&',premises)|'==>'|g.choice(names))
 # Compare to a distinct-premise rule KB because the teacher FC counter also counts duplicates.
 ref=PropDefiniteKB()
 for c in k.clauses:
  normalized=(associate('&',list(dict.fromkeys(conjuncts(c.args[0]))))|'==>'|c.args[1]) if c.op=='==>' else c
  if normalized not in ref.clauses:
   ref.tell(normalized)
 for q in names:
  actual=pl_bc_entails(k,q);expected=pl_fc_entails(ref,q)
  if actual!=expected:
   print('MISMATCH',q,actual,expected,[str(c) for c in k.clauses],flush=True)
   raise AssertionError('Horn mismatch')
  count+=1
r['random_horn_queries']=count
for solve in [solve_full_grid_fc,solve_full_grid_bc]:
 try:solve(4,2,2,{})
 except ValueError:pass
 else:raise AssertionError('Must not report partial grid as a solution')
# Load app-specific proof utilities without running the UI.
module=ast.parse((p/'sudoku_app.py').read_text());defs=[x for x in module.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name in ['ProofSet','build_proof','decode_symbol','describe_step']];ns={'conjuncts':conjuncts};exec(compile(ast.Module(body=defs,type_ignores=[]),'app_helpers','exec'),ns)
pool=json.load(open('puzzles.json'));proofs=0;fc_checks=0
for item in pool['puzzles']:
 givens={tuple(map(int,k.split('_'))):v for k,v in item['givens'].items()};sol={tuple(map(int,k.split('_'))):v for k,v in item['solution'].items()};kb=build_definite_kb(9,3,3,givens);kb.proven=ns['ProofSet'](kb)
 # Verify both positive and explicit negative proof DAGs for all 81 cells.
 for (row,col),value in sol.items():
  for kind,v in [('Is',value),('Not',value%9+1)]:
   q=atom(kind,row,col,v);assert pl_bc_entails(kb,q);steps=ns['build_proof'](kb,q);assert steps
   known=set()
   for tag,head,body in steps:
    if tag=='given':assert head in kb.facts
    else:assert all(x in known for x in body) and any(tuple(conjuncts(b))==body for b in kb.rules[head])
    known.add(head);assert ns['describe_step']((tag,head,body))
   assert q in known;proofs+=1
 # Direct FC/BC comparisons with teacher FC and the same index supplied by the solver.
 index={}
 for c in kb.clauses:
  if c.op=='==>':
   for a in conjuncts(c.args[0]):index.setdefault(a,[]).append(c)
 kb.clauses_with_premise=lambda a:index.get(a,[])
 for (row,col),value in list(sol.items())[:5]:
  for v in [value,value%9+1]:assert pl_fc_entails(kb,atom('Is',row,col,v))==pl_bc_entails(kb,atom('Is',row,col,v))==(v==value);fc_checks+=1
r['verified_proof_dags']=proofs;r['direct_fc_bc_queries']=fc_checks
for name in ['logic_.py','utils.py','puzzles.json']:assert (p/name).read_bytes()==(p.parent/name).read_bytes()
def getfun(src,name):return ast.dump(next(x for x in ast.parse(src).body if isinstance(x,ast.FunctionDef) and x.name==name))
assert getfun((p/'sudoku_solver.py').read_text(),'atom')==getfun((p.parent/'sudoku_solver.py').read_text(),'atom')
nb=json.load(open('Sudoku_Assignment.ipynb'));orig=json.load(open(p.parent/'Sudoku_Assignment.ipynb'))
find=lambda n:next(''.join(c['source']) for c in n['cells'] if 'def load_pool(' in ''.join(c['source']))
assert getfun(find(nb),'load_pool')==getfun(find(orig),'load_pool')
assert all(x.module in ['utils','logic_'] for x in ast.parse((p/'sudoku_solver.py').read_text()).body if isinstance(x,ast.ImportFrom))
assert not any(isinstance(x,ast.Import) for x in ast.parse((p/'sudoku_solver.py').read_text()).body)
r['protected_files_functions_imports']='PASS';r['status']='PASS'
(p/'validation_outputs/regressions.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
