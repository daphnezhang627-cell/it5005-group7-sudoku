"""Sudoku knowledge representation and propositional inference.

Only the two supplied modules are imported. Neither module is modified.
The Horn encoding uses peer elimination and the last candidate in a cell;
it does not guess, backtrack over Sudoku assignments, or read an answer key.
"""

from utils import *
from logic_ import *


# Do not change this function; it is used to create atomic propositions.
def atom(prefix, r, c, v):
    """prefix is 'Is' or 'Not'. Returns the Expr for e.g. Is3_2_4."""
    return expr(f'{prefix}{r}_{c}_{v}')


def _validate(n, box_h, box_w, givens):
    """Reject malformed grids and directly conflicting givens."""
    if any(type(x) is not int or x < 1 for x in (n, box_h, box_w)):
        raise ValueError('Grid and box dimensions must be positive integers.')
    if box_h * box_w != n or n % box_h or n % box_w:
        raise ValueError('Each box must contain n cells and tile the grid.')
    for cell, value in givens.items():
        if (not isinstance(cell, tuple) or len(cell) != 2
                or any(type(x) is not int or not 1 <= x <= n for x in cell)
                or type(value) is not int or not 1 <= value <= n):
            raise ValueError('Givens must map (row, column) to values in 1..n.')
    for a, b in combinations(sorted(givens), 2):
        if givens[a] == givens[b] and _peer_reason(a, b, box_h, box_w):
            raise ValueError('Two givens conflict in a row, column, or box.')


def _peer_reason(a, b, box_h, box_w):
    """Return one reason why distinct cells constrain each other."""
    if a == b:
        return None
    if a[0] == b[0]:
        return 'row'
    if a[1] == b[1]:
        return 'column'
    if ((a[0] - 1) // box_h, (a[1] - 1) // box_w) == (
            (b[0] - 1) // box_h, (b[1] - 1) // box_w):
        return 'box'
    return None


class _IndexedDefiniteKB(PropDefiniteKB):
    """The supplied KB with premise/head indices, not a new inference engine.

    The library's pl_fc_entails calls clauses_with_premise. Indexing that
    lookup avoids repeatedly scanning all rules without changing its logic.
    Use tell/retract to edit this KB so indices and proof caches stay valid.
    """

    def __init__(self):
        super().__init__()
        self.by_premise = defaultdict(list)
        self.by_head = defaultdict(list)
        self.facts = set()
        self.rule_info = {}
        self.version = 0

    def tell(self, sentence):
        super().tell(sentence)
        premises, head = parse_definite_clause(sentence)
        if premises:
            self.by_head[head].append(sentence)
            for premise in set(premises):
                self.by_premise[premise].append(sentence)
        else:
            self.facts.add(head)
        self.version += 1

    def retract(self, sentence):
        super().retract(sentence)
        self.by_premise.clear()
        self.by_head.clear()
        self.facts.clear()
        for clause in self.clauses:
            premises, head = parse_definite_clause(clause)
            if premises:
                self.by_head[head].append(clause)
                for premise in set(premises):
                    self.by_premise[premise].append(clause)
            else:
                self.facts.add(head)
        self.version += 1

    def clauses_with_premise(self, p):
        return self.by_premise.get(p, ())


def build_general_kb(n, box_h, box_w, givens):
    """Return a PropKB containing the six Sudoku constraints in CNF.

    Is(r,c,v) is sufficient here: logical negation is directly available.
    A pair of cells that shares both a row/column and a box needs just one
    exclusion clause per value; duplicates do not add any information.
    """
    _validate(n, box_h, box_w, givens)
    kb = PropKB()
    cells = [(r, c) for r in range(1, n + 1) for c in range(1, n + 1)]
    symbols = {(r, c, v): atom('Is', r, c, v)
               for r, c in cells for v in range(1, n + 1)}
    for r, c in cells:
        values = [symbols[r, c, v] for v in range(1, n + 1)]
        kb.tell(associate('|', values))  # At least one value per cell.
        for a, b in combinations(values, 2):
            kb.tell(~a | ~b)  # At most one value per cell.
    for a, b in combinations(cells, 2):
        if _peer_reason(a, b, box_h, box_w):
            for v in range(1, n + 1):
                kb.tell(~symbols[a + (v,)] | ~symbols[b + (v,)])
    for (r, c), v in sorted(givens.items()):
        kb.tell(symbols[r, c, v])
    return kb


def build_definite_kb(n, box_h, box_w, givens):
    """Return a PropDefiniteKB for elimination + last-candidate reasoning.

    Not(r,c,v) is a positive atom meaning 'value v has been excluded'.
    It is NOT Python negation and is not inferred from a failed Is query.
    This sound rule encoding is intentionally weaker than the general CNF
    encoding: puzzles requiring stronger techniques can remain unresolved.
    """
    _validate(n, box_h, box_w, givens)
    kb = _IndexedDefiniteKB()
    cells = [(r, c) for r in range(1, n + 1) for c in range(1, n + 1)]
    yes = {(r, c, v): atom('Is', r, c, v)
           for r, c in cells for v in range(1, n + 1)}
    no = {(r, c, v): atom('Not', r, c, v)
          for r, c in cells for v in range(1, n + 1)}

    def rule(premises, head, kind):
        clause = Expr('==>', associate('&', premises), head) if premises else head
        kb.tell(clause)
        kb.rule_info[clause] = kind

    for r, c in cells:
        for v in range(1, n + 1):
            for other in range(1, n + 1):
                if other != v:
                    rule([yes[r, c, v]], no[r, c, other], 'cell')
            rule([no[r, c, other] for other in range(1, n + 1) if other != v],
                 yes[r, c, v], 'last candidate')
    for a, b in combinations(cells, 2):
        reason = _peer_reason(a, b, box_h, box_w)
        if reason:
            for v in range(1, n + 1):
                rule([yes[a + (v,)]], no[b + (v,)], reason)
                rule([yes[b + (v,)]], no[a + (v,)], reason)
    for (r, c), v in sorted(givens.items()):
        rule([], yes[r, c, v], 'given')
    return kb


class _BackwardProof:
    """Goal-directed backward chaining with tabling and cycle completion.

    Expansion starts at the requested head and recursively requests its rule
    premises (AND), considering all alternative rules (OR). A repeated goal
    is suspended, never assumed true or cached as false. Waiting rules are
    resumed when premises receive proofs. This reaches the least fixed point
    of the demanded subgraph, including cycles with an external fact.

    Recursive expansion is split into chunks of 64 levels. Deferred goals
    resume on an explicit stack, avoiding Python recursion-limit failures.
    A proof is recorded only after all its premises have actual proofs.
    """

    def __init__(self, kb):
        self.rules = defaultdict(list)
        self.proofs = {}
        seen = set()
        for clause in kb.clauses:
            if clause in seen:
                continue
            seen.add(clause)
            premises, head = parse_definite_clause(clause)
            if premises:
                self.rules[head].append((clause, tuple(dict.fromkeys(premises))))
            else:
                self.proofs[head] = (None, ())
        self.expanded = set()
        self.waiting = defaultdict(list)
        self.remaining = {}
        self.agenda = []
        self.deferred = []

    def _record(self, head, rule, premises):
        if head not in self.proofs:
            self.proofs[head] = (rule, premises)
            self.agenda.append(head)

    def _resume(self):
        while self.agenda:
            proven = self.agenda.pop()
            for rule, head, premises in self.waiting.pop(proven, ()):
                self.remaining[rule] -= 1
                if self.remaining[rule] == 0:
                    self._record(head, rule, premises)

    def _expand(self, goal, depth=0):
        if goal in self.proofs or goal in self.expanded:
            return
        if depth >= 64:
            self.deferred.append(goal)
            return
        self.expanded.add(goal)  # Tabling suspends recursive cycles.
        for rule, premises in self.rules.get(goal, ()):
            missing = [p for p in premises if p not in self.proofs]
            self.remaining[rule] = len(missing)
            if not missing:
                self._record(goal, rule, premises)
                self._resume()
                break
            # Install all dependencies BEFORE recursing into a premise.
            for premise in missing:
                self.waiting[premise].append((rule, goal, premises))
            for premise in missing:
                self._expand(premise, depth + 1)
                self._resume()
            if goal in self.proofs:
                break

    def prove(self, query):
        if query in self.proofs:
            return True
        self.deferred.append(query)
        while self.deferred:
            self._expand(self.deferred.pop())
            self._resume()
        # No expansion or proof propagation remains: failure is now final.
        return query in self.proofs


def _proof_engine(kb):
    """Reuse tables on an unchanged KB; invalidate after tell/retract.

    Generic supplied PropDefiniteKB instances also work. Their clause
    snapshot detects edits because the supplied class has no version field.
    """
    stamp = kb.version if isinstance(kb, _IndexedDefiniteKB) else tuple(kb.clauses)
    if getattr(kb, '_bc_stamp', None) != stamp:
        kb._bc_engine = _BackwardProof(kb)
        kb._bc_stamp = stamp
    return kb._bc_engine


def pl_bc_entails(kb, query):
    """Prove a positive atomic query by goal-directed backward chaining.

    Return False for 'not entailed', not for classical negation. No truth is
    obtained from a cyclic assumption. The proof tables belong to this KB.
    """
    if not isinstance(query, Expr) or query.args or not is_prop_symbol(query.op):
        raise ValueError('The query must be a positive propositional atom.')
    return _proof_engine(kb).prove(query)


def explain_bc(kb, query):
    """Return (entailed, steps) using actual, successful backward proofs.

    Steps form a dependency-ordered proof DAG, with shared subproofs shown
    once. Each contains an Expr conclusion, its premises, and a rule kind.
    The app translates these into natural language; no inference is copied.
    """
    if not pl_bc_entails(kb, query):
        return False, []
    engine = _proof_engine(kb)
    seen, steps = set(), []
    stack = [(query, False)]
    while stack:
        goal, after = stack.pop()
        if goal in seen:
            continue
        rule, premises = engine.proofs[goal]
        if after:
            seen.add(goal)
            steps.append({'conclusion': goal, 'premises': premises,
                          'kind': getattr(kb, 'rule_info', {}).get(rule, 'rule')
                          if rule is not None else 'given'})
        else:
            stack.append((goal, True))
            stack.extend((p, False) for p in reversed(premises) if p not in seen)
    return True, steps


def _solve(n, box_h, box_w, givens, entails):
    kb = build_definite_kb(n, box_h, box_w, givens)
    grid = {}
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            # Givens are already positive facts; query only missing cells.
            if (r, c) in givens:
                grid[r, c] = givens[r, c]
                continue
            for v in range(1, n + 1):
                if entails(kb, atom('Is', r, c, v)):
                    grid[r, c] = v
                    break
            else:
                raise ValueError(f'Cell ({r}, {c}) is unresolved by elimination '
                                 'and last-candidate rules; no value was guessed.')
    _validate(n, box_h, box_w, grid)
    return grid


def solve_full_grid_fc(n, box_h, box_w, givens):
    """Solve every empty cell by calling the supplied pl_fc_entails.

    A fresh indexed KB is built per full-grid solve. The library resets its
    agenda and counters on every candidate query; no FC result is cached.
    """
    return _solve(n, box_h, box_w, givens, pl_fc_entails)


def solve_full_grid_bc(n, box_h, box_w, givens):
    """Solve every empty cell using our tabled pl_bc_entails.

    A fresh KB is built per solve. Proven premises are reused across cell
    queries in that solve, a documented implementation difference from FC.
    """
    return _solve(n, box_h, box_w, givens, pl_bc_entails)
