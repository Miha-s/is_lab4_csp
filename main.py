from collections import defaultdict
from typing import List, Dict, Tuple, Optional

class CSP:
    def __init__(self, variables: List[str], domains: Dict[str, List[int]], constraints: List[Tuple[Tuple[str, ...], callable]]):
        """
        Initialize the CSP problem.
        :param variables: List of variable names.
        :param domains: Possible values for each variable.
        :param constraints: List of constraints as tuples of variables and a condition function.
        """
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.neighbors = defaultdict(list)
        self._create_constraint_graph()

    def _create_constraint_graph(self):
        """
        Build a graph where each variable connects to others it shares constraints with.
        """
        for vars_, _ in self.constraints:
            for var in vars_:
                self.neighbors[var].extend([v for v in vars_ if v != var])

    def _is_assignment_valid(self, variable, value, assignment):
        """
        Check if assigning a value to a variable is consistent with the constraints.
        """
        assignment[variable] = value
        for vars_, condition in self.constraints:
            if variable in vars_:
                values = [assignment.get(v, None) for v in vars_]
                if None not in values and not condition(*values):
                    del assignment[variable]
                    return False
        del assignment[variable]
        return True

    def _select_next_variable(self, assignment):
        """
        Choose the next unassigned variable using MRV and Degree heuristics.
        MRV: Minimum Remaining Values (fewest legal values).
        Degree: Most constraints on neighbors.
        """
        unassigned = [v for v in self.variables if v not in assignment]
        # Minimum Remaining Values heuristic
        min_domain_vars = sorted(unassigned, key=lambda v: len(self.domains[v]))
        # Degree heuristic
        return max(min_domain_vars, key=lambda v: len(self.neighbors[v]))

    def _order_values_by_least_conflicts(self, variable, assignment):
        """
        Order the values for a variable by the least conflict heuristic.
        """
        def count_conflicts(value):
            assignment[variable] = value
            conflict_count = 0
            for neighbor in self.neighbors[variable]:
                if neighbor not in assignment:
                    conflict_count += sum(
                        not self._is_assignment_valid(neighbor, val, assignment)
                        for val in self.domains[neighbor]
                    )
            del assignment[variable]
            return conflict_count

        return sorted(self.domains[variable], key=count_conflicts)

    def _recursive_backtracking(self, assignment):
        """
        Perform backtracking search to find a valid assignment.
        """
        if len(assignment) == len(self.variables):
            return assignment

        variable = self._select_next_variable(assignment)

        for value in self._order_values_by_least_conflicts(variable, assignment):
            if self._is_assignment_valid(variable, value, assignment):
                assignment[variable] = value
                result = self._recursive_backtracking(assignment)
                if result:
                    return result
                del assignment[variable]

        return None

    def solve(self):
        """
        Solve the CSP using backtracking search.
        :return: A valid assignment or None if no solution exists.
        """
        return self._recursive_backtracking({})



variables = ["A", "B", "C", "D", "E"]

domains = {
    "A": [1, 2, 3],
    "B": [1, 2, 3],
    "C": [1, 2, 3],
    "D": [1, 2, 3],
    "E": [1, 2, 3],
}

constraints = [
    (("A", "B"), lambda a, b: a != b),  # A і B повинні мати різні кольори
    (("C", "E"), lambda c, e: c == e),  # C і E мають однаковий колір
    (("A", "B", "C"), lambda a, b, c: len(set([a, b, c])) == 3),  # A, B і C мають різні кольори
    (("B", "D"), lambda b, d: b != 1 or d == 2),  # Якщо B = 1, тоді D = 2
    (("B", "C"), lambda b, c: b != c),  # B і C повинні мати різні кольори
    (("D", "E"), lambda d, e: d != e),  # D і E мають різні кольори
]

csp = CSP(variables, domains, constraints)
solution = csp.solve()
print("Розв’язок CSP:", solution)

