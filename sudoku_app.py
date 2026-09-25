"""Interactive Sudoku solver and proof viewer for IT5005.

All KB construction and inference are imported from sudoku_solver.py.
This file only loads givens, manages the interface, and presents proof steps.
"""

import json
import time
from pathlib import Path

import streamlit as st

from sudoku_solver import (
    atom, build_definite_kb, build_general_kb,
    solve_full_grid_fc, solve_full_grid_bc, pl_bc_entails, explain_bc,
)


def read_puzzles():
    """Load only input givens; never expose the supplied solutions to a solver."""
    with Path(__file__).with_name('puzzles.json').open(encoding='utf-8') as f:
        raw = json.load(f)
    puzzles = [{tuple(map(int, k.split('_'))): v for k, v in p['givens'].items()}
               for p in raw['puzzles']]
    return raw['n'], raw['box_h'], raw['box_w'], puzzles


def board_html(n, box_h, box_w, givens, grid, highlight=None):
    """Generate an accessible board with row/column labels and box borders."""
    rows = ['<table class="sudoku" aria-label="Sudoku board"><thead><tr><th></th>']
    rows += [f'<th scope="col">{c}</th>' for c in range(1, n + 1)]
    rows.append('</tr></thead><tbody>')
    for r in range(1, n + 1):
        rows.append(f'<tr><th scope="row">{r}</th>')
        for c in range(1, n + 1):
            value = grid.get((r, c), '')
            kind = 'given' if (r, c) in givens else 'deduced' if value else 'empty'
            classes = [kind]
            if highlight == (r, c):
                classes.append('focus')
            styles = []
            if (r - 1) % box_h == 0:
                styles.append('border-top:2px solid #64748b')
            if r % box_h == 0:
                styles.append('border-bottom:2px solid #64748b')
            if (c - 1) % box_w == 0:
                styles.append('border-left:2px solid #64748b')
            if c % box_w == 0:
                styles.append('border-right:2px solid #64748b')
            rows.append(f'<td class="{" ".join(classes)}" style="{";".join(styles)}" '
                        f'aria-label="Row {r}, column {c}, {value or "empty"}, {kind}">'
                        f'{value}</td>')
        rows.append('</tr>')
    rows.append('</tbody></table>')
    return ''.join(rows)


def unpack(symbol):
    prefix = 'Not' if symbol.op.startswith('Not') else 'Is'
    r, c, v = map(int, symbol.op[len(prefix):].split('_'))
    return prefix, r, c, v


def statement(symbol):
    prefix, r, c, v = unpack(symbol)
    return f'Row {r}, column {c} {"cannot be" if prefix == "Not" else "is"} {v}'


def describe(step):
    """Translate the actual rule and its premises into a short explanation."""
    conclusion, premises, kind = step['conclusion'], step['premises'], step['kind']
    prefix, r, c, v = unpack(conclusion)
    if kind == 'given':
        return f'{statement(conclusion)}. This number is given in the puzzle.'
    if kind == 'last candidate':
        excluded = ', '.join(str(unpack(p)[3]) for p in premises)
        return (f'Row {r}, column {c} must be {v}: values {excluded} have all '
                'been excluded, leaving this as the only candidate.')
    if kind == 'cell':
        return f'{statement(conclusion)} because this cell is already {unpack(premises[0])[3]}.'
    if kind in ('row', 'column', 'box'):
        _, pr, pc, pv = unpack(premises[0])
        return (f'{statement(conclusion)} because row {pr}, column {pc} is {pv}. '
                f'The two cells share a {kind}, which cannot repeat a number.')
    return statement(conclusion) + '.'


def main():
    st.set_page_config(page_title='Sudoku | Reasoning Lab', page_icon='🧩', layout='wide')
    st.markdown('''<style>
    .block-container {max-width:1160px; padding-top:4.5rem;}
    .eyebrow {color:#087f8c; font-size:.82rem; font-weight:700; letter-spacing:.16em;}
    .sudoku {border-collapse:collapse; width:min(100%,520px); table-layout:fixed;
             margin:0 auto 1rem; font-family:system-ui,sans-serif;}
    .sudoku th {height:27px; width:27px; color:#64748b; font-size:12px; font-weight:500;}
    .sudoku td {height:46px; text-align:center; border:1px solid #dbe4eb;
                font-size:22px; background:#fff; color:#152f48;}
    .sudoku td.given {font-weight:750; background:#edf2f7;}
    .sudoku td.deduced {font-weight:500; color:#087f8c;}
    .sudoku td.focus {background:#fff0b3; box-shadow:inset 0 0 0 2px #c48400;}
    @media(max-width:600px){.sudoku td{height:34px; font-size:18px;}}
    </style>''', unsafe_allow_html=True)
    st.markdown('<p class="eyebrow">IT5005 · GROUP 7 · LOGIC IN ACTION</p>', unsafe_allow_html=True)
    st.title('Sudoku Reasoning Lab')
    st.write('Solve a puzzle, test a claim, and follow the evidence one step at a time.')

    n, bh, bw, puzzles = read_puzzles()
    index = st.selectbox('Choose a puzzle', range(len(puzzles)),
                         format_func=lambda i: f'Puzzle {i + 1} · {len(puzzles[i])} given numbers',
                         key='puzzle_index')
    givens = puzzles[index]
    if st.session_state.get('active_puzzle') != index:
        for key in ('solved', 'solve_time', 'used_algorithm', 'query_result', 'proof_step', 'query_kb'):
            st.session_state.pop(key, None)
        st.session_state.active_puzzle = index
        first_empty = next((cell for cell in ((r, c) for r in range(1, n + 1)
                                             for c in range(1, n + 1)) if cell not in givens), (1, 1))
        st.session_state.query_row, st.session_state.query_col = first_empty
        st.session_state.query_value = 1

    board_col, controls = st.columns([1.25, 1], gap='large')
    with controls:
        st.subheader('Solve the whole grid')
        algorithm = st.radio('Inference method', ['Backward chaining', 'Forward chaining'], key='algorithm')
        st.caption('Forward: apply rules from known facts. Backward: start with a claim and seek its proof.')
        if st.button('Solve puzzle', type='primary', key='solve'):
            # A failed new attempt must not display an older successful result.
            for key in ('solved', 'solve_time', 'used_algorithm'):
                st.session_state.pop(key, None)
            solve = solve_full_grid_bc if algorithm == 'Backward chaining' else solve_full_grid_fc
            try:
                with st.spinner(f'Solving with {algorithm.lower()}…'):
                    start = time.perf_counter()
                    solved = solve(n, bh, bw, givens)
                    elapsed = time.perf_counter() - start
                st.session_state.solved = solved
                st.session_state.solve_time = elapsed
                st.session_state.used_algorithm = algorithm
            except ValueError as error:
                st.error(str(error))
        if 'solved' in st.session_state:
            st.success(f'Solved with {st.session_state.used_algorithm.lower()}.')
            st.metric('Solve time', f'{st.session_state.solve_time:.3f} s')
        st.divider()
        st.subheader('Test a cell')
        st.caption('Can the rules prove that this cell contains this number?')
        with st.form('cell_query'):
            x, y, z = st.columns(3)
            r = x.number_input('Row', min_value=1, max_value=n, step=1, key='query_row')
            c = y.number_input('Column', min_value=1, max_value=n, step=1, key='query_col')
            v = z.number_input('Value', min_value=1, max_value=n, step=1, key='query_value')
            submitted = st.form_submit_button('Check and explain')
        if submitted:
            with st.spinner('Looking for a proof…'):
                if 'query_kb' not in st.session_state:
                    st.session_state.query_kb = build_definite_kb(n, bh, bw, givens)
                kb = st.session_state.query_kb
                query = atom('Is', r, c, v)
                verdict = pl_bc_entails(kb, query)
                target = query if verdict else atom('Not', r, c, v)
                exclusion_proven, steps = explain_bc(kb, target)
                st.session_state.query_result = dict(
                    cell=(r, c), value=v, verdict=verdict, steps=steps,
                    excluded=(not verdict and exclusion_proven))
                st.session_state.pop('proof_step', None)
        result = st.session_state.get('query_result')
        if result:
            r0, c0 = result['cell']
            label = f'Row {r0}, column {c0} = {result["value"]}'
            if result['verdict']:
                st.success(f'True — {label} is entailed.')
            elif result['excluded']:
                st.warning(f'False — {label} is not entailed; this value is explicitly excluded.')
            else:
                st.info(f'False — no proof for {label} was found. Lack of a proof alone does not prove its negation.')
    with board_col:
        st.subheader('The board')
        grid = st.session_state.get('solved', givens)
        highlight = result['cell'] if result else None
        st.markdown(board_html(n, bh, bw, givens, grid, highlight), unsafe_allow_html=True)
        st.caption('Bold on grey = given · Teal = deduced · Amber = queried cell')

    st.divider()
    st.subheader('Follow the proof')
    if not result or not result['steps']:
        st.info('Use “Check and explain” to replay a proof for a cell or for an excluded value.')
        return
    steps = result['steps']
    st.caption('These are the actual successful inference steps. Shared supporting facts appear once.')
    if len(steps) > 1:
        selected = st.slider('Proof step', min_value=1, max_value=len(steps), value=len(steps), key='proof_step')
    else:
        selected = 1
        st.caption('1 step: the statement is already a given.')
    current = steps[selected - 1]
    replay = dict(givens)
    for step in steps[:selected]:
        prefix, rr, cc, vv = unpack(step['conclusion'])
        if prefix == 'Is':
            replay[rr, cc] = vv
    _, rr, cc, _ = unpack(current['conclusion'])
    left, right = st.columns([1.25, 1], gap='large')
    with left:
        st.markdown(board_html(n, bh, bw, givens, replay, (rr, cc)), unsafe_allow_html=True)
        st.caption('Replay shows givens and only the placements proved up to this step.')
    with right:
        st.markdown(f'**Step {selected} of {len(steps)} · {current["kind"].title()}**')
        st.write(describe(current))
        positions = {step['conclusion']: i + 1 for i, step in enumerate(steps)}
        if current['premises']:
            with st.expander('Supporting facts', expanded=True):
                for premise in current['premises']:
                    st.write(f'Step {positions[premise]}: {statement(premise)}.')
        with st.expander('All proof steps'):
            for i, step in enumerate(steps, 1):
                st.write(f'{i}. {describe(step)}')


if __name__ == '__main__':
    main()
