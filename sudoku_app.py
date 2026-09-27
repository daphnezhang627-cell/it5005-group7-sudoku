"""Interactive Sudoku solver and backward-chaining tutor."""

import json
import time
from pathlib import Path

import streamlit as st

from logic_ import conjuncts
from sudoku_solver import (
    atom,
    build_definite_kb,
    build_general_kb,
    solve_full_grid_fc,
    solve_full_grid_bc,
    pl_bc_entails,
)


def decode_symbol(symbol):
    """Return a symbol's kind, row, column, and value."""
    name = str(symbol)
    kind = 'Not' if name.startswith('Not') else 'Is'
    row, col, value = map(int, name[len(kind):].split('_'))
    return kind, row, col, value


def describe_step(step):
    """Turn a proved rule and its premises into a readable sentence."""
    kind, conclusion, premises = step
    conclusion_kind, row, col, value = decode_symbol(conclusion)

    if kind == 'given':
        return f'Cell ({row}, {col}) contains {value}; this is a given.'

    if conclusion_kind == 'Is':
        excluded = sorted(decode_symbol(premise)[3] for premise in premises)
        values = ', '.join(map(str, excluded))
        return (
            f'Cell ({row}, {col}) cannot contain {values}. '
            f'{value} is its last remaining candidate.'
        )

    _, source_row, source_col, source_value = decode_symbol(premises[0])
    if (source_row, source_col) == (row, col):
        return (
            f'Cell ({row}, {col}) already contains {source_value}, '
            f'so it cannot contain {value}.'
        )

    if source_row == row:
        unit = 'row'
    elif source_col == col:
        unit = 'column'
    else:
        unit = 'box'
    return (
        f'Cell ({source_row}, {source_col}) contains {value}. '
        f'Cell ({row}, {col}) shares its {unit}, so {value} is eliminated there.'
    )


class ProofSet(set):
    """Keep the premises that were already true when BC proved a symbol."""
    def __init__(self, kb):
        super().__init__()
        self.kb = kb
        self.reasons = {}

    def add(self, symbol):
        if symbol in self:
            return
        for premise in self.kb.rules.get(symbol, []):
            symbols = tuple(conjuncts(premise))
            if all(s in self.kb.facts or s in self for s in symbols):
                self.reasons[symbol] = symbols
                break
        super().add(symbol)


def build_proof(kb, query):
    """List the recorded steps leading from givens to the query."""
    steps = []
    shown = set()

    def add_steps(symbol):
        if symbol in shown:
            return True
        if symbol in kb.facts:
            steps.append(('given', symbol, ()))
        else:
            premises = kb.proven.reasons.get(symbol)
            if premises is None or not all(add_steps(s) for s in premises):
                return False
            steps.append(('inferred', symbol, premises))
        shown.add(symbol)
        return True

    if not add_steps(query):
        return []
    return steps


def render_board(values, givens, n, box_h, box_w):
    """Draw a board with visible box boundaries and highlighted givens."""
    cells = [
        '<div role="grid" aria-label="Sudoku board" style="display:grid;grid-template-columns:repeat('
        f'{n},minmax(0,1fr));max-width:520px;margin:0.5rem 0 1rem 0;">'
    ]
    for row in range(1, n + 1):
        for col in range(1, n + 1):
            value = values.get((row, col), '')
            given = (row, col) in givens
            background = '#dbeafe' if given else ('#dcfce7' if value else '#f8fafc')
            weight = '700' if given else '500'
            top = '3px solid #334155' if (row - 1) % box_h == 0 else '1px solid #94a3b8'
            left = '3px solid #334155' if (col - 1) % box_w == 0 else '1px solid #94a3b8'
            right = '3px solid #334155' if col == n else '0'
            bottom = '3px solid #334155' if row == n else '0'
            label = 'given' if given else ('solved' if value else 'empty')
            style = (
                'aspect-ratio:1;display:flex;align-items:center;justify-content:center;'
                'min-width:0;font-size:1.2rem;color:#0f172a;'
                f'background:{background};font-weight:{weight};'
                f'border-top:{top};border-left:{left};'
                f'border-right:{right};border-bottom:{bottom};'
            )
            cells.append(
                f'<div role="gridcell" aria-label="{label} cell {row}, {col}: '
                f'{value if value else "blank"}" style="{style}">{value or "&nbsp;"}</div>'
            )
    cells.append('</div>')
    st.markdown(''.join(cells), unsafe_allow_html=True)


st.set_page_config(page_title='Sudoku Logic Tutor', layout='centered')
st.title('Sudoku Logic Tutor')
st.caption('Solve with propositional logic and inspect a backward-chaining proof.')

with Path(__file__).with_name('puzzles.json').open(encoding='utf-8') as puzzle_file:
    pool = json.load(puzzle_file)

n, box_h, box_w = pool['n'], pool['box_h'], pool['box_w']
puzzles = pool['puzzles']
selected_index = st.selectbox(
    'Choose a puzzle',
    range(len(puzzles)),
    format_func=lambda i: f'Puzzle {i + 1} — {puzzles[i]["given_count"]} givens',
)
selected = puzzles[selected_index]
givens = {
    tuple(map(int, key.split('_'))): value
    for key, value in selected['givens'].items()
}

st.subheader('Starting board')
render_board(givens, givens, n, box_h, box_w)
st.caption('Blue cells are givens; blank cells still need a value.')

st.subheader('Solve the full grid')
algorithm = st.radio(
    'Inference algorithm',
    ('Forward chaining', 'Backward chaining'),
    horizontal=True,
)
if st.button('Solve selected puzzle', type='primary'):
    solver = solve_full_grid_fc if algorithm == 'Forward chaining' else solve_full_grid_bc
    with st.spinner('Solving the grid...'):
        started = time.perf_counter()
        try:
            solved = solver(n, box_h, box_w, givens)
            elapsed = time.perf_counter() - started
            if len(solved) != n * n:
                raise ValueError(f'Only {len(solved)} of {n * n} cells were proved.')
            st.session_state['solve_result'] = (selected_index, algorithm, solved, elapsed)
        except Exception as exc:
            st.session_state.pop('solve_result', None)
            st.error(f'The solver could not complete this puzzle: {exc}')

solve_result = st.session_state.get('solve_result')
if solve_result is not None and solve_result[0] == selected_index:
    _, used_algorithm, solved, elapsed = solve_result
    st.success(f'{used_algorithm} solved the grid in {elapsed:.2f} seconds.')
    render_board(solved, givens, n, box_h, box_w)
    st.caption('Blue cells were givens; green cells were inferred.')

st.subheader('Ask about a cell')
row_col, col_col, value_col = st.columns(3)
with row_col:
    query_row = st.number_input('Row', min_value=1, max_value=n, value=1, step=1)
with col_col:
    query_col = st.number_input('Column', min_value=1, max_value=n, value=1, step=1)
with value_col:
    query_value = st.number_input('Value', min_value=1, max_value=n, value=1, step=1)

if st.button('Check entailment'):
    with st.spinner('Tracing the proof...'):
        try:
            kb = build_definite_kb(n, box_h, box_w, givens)
            kb.proven = ProofSet(kb)
            query = atom('Is', query_row, query_col, query_value)
            entailed = pl_bc_entails(kb, query)

            eliminated = False
            proved_query = query
            if not entailed:
                proved_query = atom('Not', query_row, query_col, query_value)
                eliminated = pl_bc_entails(kb, proved_query)

            proof = build_proof(kb, proved_query) if entailed or eliminated else []
            if (entailed or eliminated) and not proof:
                raise ValueError('The result was proved, but its reasoning trace could not be reconstructed.')

            st.session_state['query_result'] = (
                selected_index,
                query_row,
                query_col,
                query_value,
                entailed,
                eliminated,
                [describe_step(step) for step in proof],
            )
        except Exception as exc:
            st.session_state.pop('query_result', None)
            st.error(f'The query could not be evaluated: {exc}')

query_result = st.session_state.get('query_result')
if query_result is not None and query_result[0] == selected_index:
    _, row, col, value, entailed, eliminated, steps = query_result
    if entailed:
        st.success(f'True — cell ({row}, {col}) must contain {value}.')
    elif eliminated:
        st.error(f'False — value {value} is eliminated from cell ({row}, {col}).')
    else:
        st.warning(f'False — the current rules do not prove Is({row}, {col}, {value}).')

    with st.expander(f'Reasoning trace ({len(steps)} steps)'):
        if steps:
            for number, sentence in enumerate(steps, start=1):
                st.write(f'{number}. {sentence}')
        else:
            st.write('No proof was derived from the given facts and rules.')

st.caption("Queries use only the selected puzzle's givens, never its stored solution.")
