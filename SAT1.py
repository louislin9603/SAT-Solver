# This program is the implementation for DPLL Solver and WalkSAT

import os       # For getting every file in directory (CNF Formulas)
import random 
import time

# CNF Class to Represent CNF Formulas
class CNFFormula:

    def __init__(self):
        self.num_variables = 0
        self.num_clauses = 0

        self.clauses = []        # List to hold clauses 
        self.variables = set()   # Set to hold variables (x1, x2, x3, ...)        
    

    # Parse .cnf files
    def parse_dimacs(self, file_name):
        
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    
                    line = line.strip()
                    #print(f"Reading line: {line}")

                    # Skip comments and last line with '%'
                    if line.startswith('c') or line.startswith('%') or line.startswith('0'):
                        continue 
                    
                    # Gets the numbers of variables and clauses from problem line
                    elif line.startswith('p'):
                        _, _, self.num_variables, self.num_clauses = line.split()  # Looks at line "p cnf x y" and ignores whitspace words
                        
                        # String to Int
                        self.num_variables = int(self.num_variables)
                        self.num_clauses = int(self.num_clauses)
                    
                    # Gets the variables and clauses from 
                    elif line.strip():      # Removes whitespace at beginning and end of the string

                        # Convert string to a list integers and remove trailing 0
                        clause = [int(x) for x in line.split()][:-1]
                        self.clauses.append(clause)

                        # Add int variables to set
                        self.variables.update(abs(x) for x in clause)    

            return True 
        
        # File Not Found
        except FileNotFoundError:
            print(f"Error: File {file_name} not found")
            return False 
        
        # Error Parsing
        except Exception as e:
            print(f"Error parsing file: {e}")
            return False

# DPLL Sat Solver Implementation
class DPLLSolver:

    # Initialize 
    def __init__(self):
        self.formula = None
        self.assignment = {}
        self.statistics = {
            'decisions': 0,             # Number of branching decisions
            'unit_propagations': 0,     # Number of lonely variables
            'backtracks': 0             # Number of backtracking steps
        }

    def solve(self, formula):
        self.formula = formula          # Stores the .CNF formula to be solved
        self.assignment = {}            # Empty assignment
        if self._dpll({}):              # Perform DPLL with an empty assignment
             # Ensure all variables are assigned (default to False if unassigned)
            for var in self.formula.variables:
                if var not in self.assignment:
                    self.assignment[var] = False
            return True
        return False
    # Main Recursive Algorithm
    def _dpll(self, assignment):
        
        # Create a copy of the current assignment
        assignment = assignment.copy()

        # Apply unit propagation to current assignment simplify the formula
        if not self._unit_propagation(assignment):

            # If conflcit is found, return False (unsatisfiable)
            return False 
        
        # Check if all clauses are satisfied
        if self._all_clauses_satisfied(assignment):
            self.assignment = assignment    # Stores the satisfying assignment
            # If all clauses are satisfied, we are done
            return True

        # Choose an unassigned variable for branching
        var = self._choose_next_variable(assignment)
        if var is None:
            return False    # No unassigned variables left
        
        self.statistics['decisions'] += 1   # Increment decision(s) made
        assignment[var] = True         # Try var = True first

        if self._dpll(assignment):    # Recursive
            return True
        
        # Backtracking and try var = False, if var = True didn't work
        self.statistics['backtracks'] += 1  # Increment backtracking step
        assignment[var] = False 

        if self._dpll(assignment):    # Recursive
            return True
        
        # Recursive call again
        return self._dpll(assignment)




    # Looks for lonely literals and eliminate them
    def _unit_propagation(self, assignment):

        while True:
            unit_clause = None 

            # Check each clause to see if there's a lonely unit clause
            for clause in self.formula.clauses:
                unassigned = []                 # List to store unassigned literals
                is_satifised = False            # Flag to check if clause is satisfied

                for lit in clause:
                    var = abs(lit)      # Gets the abs value from the literal

                    # Check if variable is already assigned
                    if var in assignment:

                        # Check if the assignment satisfies the clause. If so, we are good, just skip and go to next one
                        if (lit > 0) == assignment[var]:
                            is_satifised = True 
                            break
                    
                    # Variable is unassigned (no value)
                    else:
                        unassigned.append(lit)      # Add to list
                
                # Assign unit clause only if exactly one literal is unassigned
                if not is_satifised and len(unassigned) == 1:
                    unit_clause = unassigned[0]
                    break
            
            # No more unit clauses 
            if unit_clause is None:
                return True
            
            self.statistics['unit_propagations'] += 1   # Increment unit propagatation
            
            var = abs(unit_clause)    # Get literal value from unit clause
            value = unit_clause > 0              # Check if value is positive (True)

            assignment[var] = value     # Assignment to variable

            # Check if assignment leads to conflict
            if not self._is_consistent(assignment):
                return False 
    
    # Check if current assignment is consistent with the formula
    def _is_consistent(self, assignment):

        # Check each clause to see if any clause is falsified
        for clause in self.formula.clauses:
            # If clause is falsified, assignment is inconsistent
            if self._is_clause_falsified(clause, assignment):
                return False
        
        # No conflicts, we are good!
        return True
    
    # Check if a clause is falsified under the current assignment
    def _is_clause_falsified(self, clause, assignment):

        # Check each literal in clause
        for literal in clause:
            var = abs(literal)      # Gets the variable from literal

            # Not falsified (Okay for now):
            if var not in assignment:      # If variable is not assigned
                return False
            
            if (literal > 0) == assignment[var]:   # If any literal in the clause is satisfied
                return False
            
        return True

    # Check if all clauses are satisfied under current assignment
    def _all_clauses_satisfied(self, assignment):

        for clause in self.formula.clauses:
            if not any((lit > 0) == assignment.get(abs(lit), None) for lit in clause):
                return False    # If any clause is not satisfied
            
        return True     # All clauses are satisfied
                        
    # Choose next unassigned variable for branching
    def _choose_next_variable(self, assignment):

        # Go through all variables and finds the first unassigned variable 
        for var in self.formula.variables:
            if var not in assignment:
                return var
        
        return None     # No unassigned variables

    # Return solver stats (decisions, unit props, backtracks)
    def get_statistics(self):
        return self.statistics

# WalkSAT Solver Implementation
class WalkSAT:
    def __init__(self):
        self.formula = None
        self.assignment = {}
        self.p = 0.5          # Probability of random walk (0.5 by default)
        self.max_flips = 1000 # Maximum number of flips
        self.statistics = {
            'flips': 0,           # Number of flips made
            'satisfied_clauses': 0  # Number of satisfied clauses
        }

    def solve(self, formula, p=0.5, max_flips=1000):
        self.formula = formula
        self.p = p
        self.max_flips = max_flips

        # Initialize a random assignment
        self.assignment = {var: random.choice([True, False]) for var in self.formula.variables}

        for flip in range(self.max_flips):
            self.statistics['flips'] += 1

            # Count and update satisfied clauses
            self.statistics['satisfied_clauses'] = self._count_satisfied_clauses()

            if self._all_clauses_satisfied(self.assignment):
                return True

            # Choose a random unsatisfied clause
            unsatisfied_clause = self._choose_unsatisfied_clause()
            if unsatisfied_clause is None:
                continue

            # Decide whether to flip a variable in the clause or randomly select one
            if random.random() < self.p:
                # Choose a variable randomly from the unsatisfied clause
                var_to_flip = random.choice(unsatisfied_clause)
            else:
                # Choose the variable that, when flipped, maximizes the number of satisfied clauses
                var_to_flip = self._choose_variable_to_flip(unsatisfied_clause)

            # Flip the chosen variable
            self.assignment[abs(var_to_flip)] = not self.assignment[abs(var_to_flip)]

        return False  # Max flips reached without satisfying all clauses

    # Check if all clauses are satisfied
    def _all_clauses_satisfied(self, assignment):
        
        return all(any((lit > 0) == assignment.get(abs(lit), None) for lit in clause)
                   for clause in self.formula.clauses)

    # Count how many clauses are satisfied by the current assignment
    def _count_satisfied_clauses(self):
        return sum(1 for clause in self.formula.clauses if any((lit > 0) == self.assignment.get(abs(lit), None) for lit in clause))
    
    # Choose a random unsatisfied clause
    def _choose_unsatisfied_clause(self):
        unsatisfied_clauses = [clause for clause in self.formula.clauses if not any((lit > 0) == self.assignment.get(abs(lit), None) for lit in clause)]
        return random.choice(unsatisfied_clauses) if unsatisfied_clauses else None

    # Choose the variable to flip that maximizes the number of satisfied clauses
    def _choose_variable_to_flip(self, clause):
        
        best_var = None
        best_satisfied_count = -1

        for var in clause:
            # Flip the variable temporarily
            temp_assignment = self.assignment.copy()
            temp_assignment[abs(var)] = not temp_assignment[abs(var)]
            satisfied_count = sum(1 for c in self.formula.clauses if any((lit > 0) == temp_assignment.get(abs(lit), None) for lit in c))

            if satisfied_count > best_satisfied_count:
                best_satisfied_count = satisfied_count
                best_var = var

        return best_var

    def get_statistics(self):
        return self.statistics

# Main
def main():
    print("Main ran")

    cnf_files = "CNF Formulas\\"

    for file_name in os.listdir(cnf_files):

        file_path = os.path.join(cnf_files, file_name)

        if file_name.endswith(".cnf"):
            cnf = CNFFormula()

            if cnf.parse_dimacs(file_path):
                print(f"\nSuccessfully parsed {file_name}")
                #print(f"Number of variables: {cnf.num_variables}")
                print(f"Distinct variables: {cnf.variables}")

                #solver = DPLLSolver()
                solver = WalkSAT() 

                if solver.solve(cnf):
                    print("Formula satisfied")
                    #print("Assignment: ", solver.assignment)
                    for var, value in sorted(solver.assignment.items()):
                        print(f"{var}: {'True' if value else 'False'}", end=" ")
                else:
                    print("Formula is not satisfiable")
                print("\nStatistics: ", solver.get_statistics())

if __name__ == "__main__":
    main()