"""IT5005 Assignment 1: student implementation file.

Implement the functions marked below. Do not modify utils.py or logic_.py.
"""

from utils import *
from logic_ import *


# Do not change this function; it is used to create atomic propositions.
def atom(prefix, r, c, v):
    """prefix is 'Is' or 'Not'. Returns the Expr for e.g. Is3_2_4."""
    return expr(f'{prefix}{r}_{c}_{v}')


def build_general_kb(n, box_h, box_w, givens):
    """Return a PropKB encoding this n x n Sudoku's constraints plus the given
    cells, as general clauses.

    Parameters
    ----------
    n, box_h, box_w : int
    givens : dict[(int, int), int]

    Returns
    -------
    PropKB
    """

    kb = PropKB()

    # Every cell has at least one value.
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            clause = atom('Is', r, c, 1)
            for v in range(2, n + 1):
                clause |= atom('Is', r, c, v)
            kb.tell(clause)

    # A cell cannot have two different values.
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            for v in range(1, n + 1):
                for vx in range(v + 1, n + 1):
                    kb.tell(
                        ~atom('Is', r, c, v)
                        | ~atom('Is', r, c, vx)
                    )

    # Two cells in the same row, column, or box cannot have the same value.
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            for rx in range(r, n + 1):
                for cx in range(1, n + 1):
                    # Skip the current cell and pairs already considered.
                    if rx == r and cx <= c:
                        continue

                    same_box = (
                        (r - 1) // box_h == (rx - 1) // box_h
                        and (c - 1) // box_w == (cx - 1) // box_w
                    )

                    if r == rx or c == cx or same_box:
                        for v in range(1, n + 1):
                            kb.tell(
                                ~atom('Is', r, c, v)
                                | ~atom('Is', rx, cx, v)
                            )

    # Add the given values.
    for (r, c), v in givens.items():
        kb.tell(atom('Is', r, c, v))

    return kb

def build_definite_kb(n, box_h, box_w, givens):
    """Return a PropDefiniteKB encoding this n x n Sudoku's constraints plus
    the given cells, using elimination + last-candidate reasoning.

    Parameters
    ----------
    n, box_h, box_w : int
    givens : dict[(int, int), int] -- {(row, col): value}, 1-indexed

    Returns
    -------
    PropDefiniteKB
    """
    kb=PropDefiniteKB()

    #Each cell is assigned **at most/least one** value from $\{1, \dots, n\}$, i.e., it cannot hold two different values at once.
    for r in range(1,n+1):
        for c in range(1,n+1):
            for v in range(1,n+1):
                for vx in range(1,n+1):
                    if vx!=v:
                        kb.tell(atom('Is',r,c,v)|'==>'|atom('Not',r,c,vx))

    #No two cells in the same row/column/box hold the same value.
    for r in range(1,n+1):
        for c in range(1,n+1):
            for rx in range(1,n+1):
                for cx in range(1,n+1):
                    same_box=((r-1)//box_h)==((rx-1)//box_h) and ((c-1)//box_w)==((cx-1)//box_w)
                    if (r==rx or c==cx or same_box) and((r,c)!=(rx,cx)):
                        for v in range(1,n+1):
                            kb.tell(atom('Is',r,c,v)|'==>'|atom('Not',rx,cx,v))

    #If other values are eliminated, then the last value is the right one to fill.
    for r in range(1,n+1):
        for c in range(1,n+1):
            for v in range(1,n+1):
                vxs=[vx for vx in range(1,n+1) if vx!=v]
                clause=atom('Not',r,c,vxs[0])
                for vx in vxs[1:]:
                    if v!=vx:
                        clause&=atom('Not',r,c,vx)
                clause=clause|'==>'|atom('Is',r,c,v)
                kb.tell(clause)


    #The **givens** cells hold their stated values.
    for (r,c),v in givens.items():
        kb.tell(atom('Is',r,c,v))

    return kb


def solve_full_grid_fc(n, box_h, box_w, givens):
    """Solve the whole puzzle using build_definite_kb + pl_fc_entails.

    Returns
    -------
    dict[(int, int), int] -- {(row, col): value} for every cell
    """

    kb=build_definite_kb(n, box_h, box_w, givens)

    # Index rules by premise for faster forward chaining.
    premise_index = {}
    for clause in kb.clauses:
        if clause.op == '==>':
            for premise in conjuncts(clause.args[0]):
                premise_index.setdefault(premise, []).append(clause)

    kb.clauses_with_premise=lambda p: premise_index.get(p,[])

    solved=dict(givens)

    for r in range(1,n+1):
        for c in range(1,n+1):
            if (r, c) in givens:
                continue
            for v in range(1,n+1):
                q=atom('Is',r,c,v)
                if pl_fc_entails(kb,q):
                    solved[(r,c)]=v
                    break
    return solved


def pl_bc_entails(kb, query):
    """Backward-chain a query, optionally recording its successful proof.

    Parameters
    ----------
    kb : PropDefiniteKB
    query : Expr
    Returns
    -------
    bool
    """
    if not hasattr(kb, 'rules'):
        kb.rules = {}
        for clause in kb.clauses:
            if clause.op == '==>':
                if clause.args[1] in kb.rules:
                    kb.rules[clause.args[1]].append(clause.args[0])
                else:
                    kb.rules[clause.args[1]] = [clause.args[0]]

    if not hasattr(kb, 'facts'):
        kb.facts = set()
        for clause in kb.clauses:
            if clause.op != '==>':
                kb.facts.add(clause)

    if not hasattr(kb, 'proven'):
        kb.proven = set()

    if not hasattr(kb, 'waiting'):
        kb.waiting = {}

    if not hasattr(kb, 'remaining'):
        kb.remaining = {}

    if not hasattr(kb, 'expanded'):
        kb.expanded = set()

    deferred = []

    def mark_proven(symbol):
        if symbol not in kb.facts and symbol not in kb.proven:
            kb.proven.add(symbol)

            for rule in kb.waiting.pop(symbol, set()):
                kb.remaining[rule] -= 1

                if kb.remaining[rule] == 0:
                    mark_proven(rule[0])

    def prove(q, depth=0):
        if q in kb.facts or q in kb.proven:
            return True

        if q in kb.expanded:
            return False

        if depth >= 64:
            deferred.append(q)
            return False

        kb.expanded.add(q)

        for premise in kb.rules.get(q, []):
            symbols = conjuncts(premise)
            to_prove = [
                symbol for symbol in symbols
                if symbol not in kb.facts and symbol not in kb.proven
            ]
            #remaining={rule: amount of symbols to be proven}
            rule = (q, premise)
            kb.remaining[rule] = len(to_prove)

            if not to_prove:
                mark_proven(q)
                return True

            #waiting={symbol (that haven't been proven) : set of {premise containing the symbol} }
            for symbol in to_prove:
                kb.waiting.setdefault(symbol, set()).add(rule)

            for symbol in to_prove:
                prove(symbol, depth + 1)

            if q in kb.proven:
                return True

        if q in kb.proven:
            return True

    prove(query)

    while len(deferred) > 0:
        next_query = deferred.pop()
        prove(next_query)

    if query in kb.facts:
        return True

    if query in kb.proven:
        return True

    return False


def solve_full_grid_bc(n, box_h, box_w, givens):
    """Solve the whole puzzle using build_definite_kb + your own pl_bc_entails.

    For each cell, try each candidate value until pl_bc_entails confirms one
    -- the same per-cell strategy as solve_full_grid_fc, but backed by
    backward chaining instead of a single shared forward-chaining pass.

    Returns
    -------
    dict[(int, int), int] -- {(row, col): value} for every cell
    """

    kb = build_definite_kb(n, box_h, box_w, givens)
    solved = dict(givens)

    for r in range(1, n + 1):
        for c in range(1, n + 1):
            if (r, c) in solved:
                continue

            for v in range(1, n + 1):
                if pl_bc_entails(kb, atom('Is', r, c, v)):
                    solved[(r, c)] = v
                    break

            if (r, c) not in solved:
                raise ValueError(f'No value could be proved for cell ({r}, {c})')

    return solved
