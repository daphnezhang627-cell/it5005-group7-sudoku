from pathlib import Path
import os,sys,json
from streamlit.testing.v1 import AppTest
p=Path(__file__).resolve().parents[1];os.chdir(p);sys.path.insert(0,str(p))
pool=json.load(open('puzzles.json'));report={'checks':[]}
at=AppTest.from_file(str(p/'sudoku_app.py'),default_timeout=90).run();assert not at.exception
for i,item in enumerate(pool['puzzles']):
 at.selectbox[0].set_value(i).run();assert not at.exception
 assert 'solve_result' not in at.session_state and 'query_result' not in at.session_state
 for method in ['Forward chaining','Backward chaining']:
  at.radio[0].set_value(method).run();at.button[0].click().run();assert not at.exception and not at.error
  result=at.session_state['solve_result'];assert result[1]==method
  assert result[2]=={tuple(map(int,k.split('_'))):v for k,v in item['solution'].items()}
  assert result[3]>=0
 key=next(k for k in item['solution'] if k not in item['givens']);r,c=map(int,key.split('_'));v=item['solution'][key]
 for value in [v,v%9+1]:
  at.number_input[0].set_value(r);at.number_input[1].set_value(c);at.number_input[2].set_value(value);at.button[1].click().run();assert not at.exception
  result=at.session_state['query_result'];assert result[4]==(value==v);assert result[5]==(value!=v);assert result[6]
 report['checks'].append(f'Puzzle {i+1}: FC/BC exact grids, query True/False, nonempty trace, switch clearing PASS');print(report['checks'][-1],flush=True)
at.selectbox[0].set_value(0).run();assert 'solve_result' not in at.session_state and 'query_result' not in at.session_state
at.selectbox[0].set_value(4).run();assert 'solve_result' not in at.session_state and 'query_result' not in at.session_state
# An underdetermined puzzle distinguishes no proof from explicit exclusion.
from unittest.mock import patch
fixture={'n':4,'box_h':2,'box_w':2,'puzzles':[{'givens':{},'given_count':0,'solution':{}}]}
with patch('json.load',return_value=fixture):
 unknown=AppTest.from_file(str(p/'sudoku_app.py'),default_timeout=90).run();unknown.button[1].click().run()
 assert not unknown.exception and unknown.warning
 result=unknown.session_state['query_result'];assert result[4:6]==(False,False) and result[6]==[]
report['unknown_vs_excluded']='PASS';report['return_to_previous_clears_results']='PASS';report['status']='PASS'
(p/'validation_outputs/streamlit_tests.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
