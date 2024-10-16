# This program is the implementation for GSAT Solver



import random
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

def parseCnf(cnf_files):
    for file_name in cnf_files:
        cnf = CNFFormula()

        if cnf.parse_dimacs(file_name):
            print(f"Successfully parsed {file_name}")
        else: print(f"Error parsing file: {file_name}")

    return cnf.num_variables, len(cnf.clauses), cnf.clauses

def main():

    maxFlips = 100
    maxRestarts = 10
    cnf_files = ["CNF_Formulas/uf20-0156.cnf"]
    #cnf_files = ["CNF_Formulas/uf50-01.cnf"]
    numVariables, noOfClauses, listofClauses= parseCnf(cnf_files)

    bestAssignment, bestFitness = gsat(listofClauses, maxFlips, maxRestarts, numVariables)

    print(f"Best assignment:  {bestAssignment}")
    print(f"Best fitness:  {bestFitness} clauses satisfied, out of {noOfClauses}")

# Assign random true/false values to each variable
def randomAssignment(numVariables):

    # Return the assignment as a dictionary
    return {i: random.choice([True, False]) for i in range(1, numVariables + 1)}

# Check how many clauses are satisfied by the current assignment
def evaluateFitness(clauses, assignment):

    satisfied = 0 # Holds # of satisifed clauses

    # iterate through each clause in assignment
    for clause in clauses:
        clauseSatisfied = False # false unless proven o/w

        # iterate through each literal in the clause
        for literal in clause:
            var = abs(literal)

            # if the literal is positive and true, or if literal is negative and false
            if (literal > 0 and assignment[var]) or (literal < 0 and not assignment[var]):
                clauseSatisfied = True
                break
        if clauseSatisfied:
            satisfied += 1
    return satisfied

# Greedy SAT Algorithm
def gsat(clauses, max_flips, max_restarts, numVariables):

    # Store best assignment and fitness we come across
    bestAssignment = None
    bestFitness = 0

    # Restart up to 10 times, per project parameter
    for restart in range(max_restarts):

        # Randomnly assign true/false values to variables
        assignment = randomAssignment(numVariables)

        # Flip truth assignments around to see if we can find a better assignment
        for flip in range(max_flips):
            currentFitness = evaluateFitness(clauses, assignment)

            # If all clauses satisfied, go home, we won
            if currentFitness == len(clauses):
                return assignment, currentFitness

            # Find the best variable to flip
            bestVarToFlip = None
            longTermFAF = currentFitness #long term best fitness after a flip

            for literal in range(1, numVariables + 1):
                # Flip the literal
                assignment[literal] = not assignment[literal]
                shortTermFAF = evaluateFitness(clauses, assignment) #short term best fitness after a flip

                # If the fitness improves, track the flip that caused improvement
                if shortTermFAF > longTermFAF:
                    longTermFAF = shortTermFAF
                    bestVarToFlip = literal

                # Flip variable back to what it was
                assignment[literal] = not assignment[literal]

            # If no improvement, stop flipping
            if bestVarToFlip is None:
                break

            # Otherwise, flip the literal that causes most improvement
            assignment[bestVarToFlip] = not assignment[bestVarToFlip]

            # Track the best overall assignment
            if longTermFAF > bestFitness:
                bestFitness = longTermFAF
                bestAssignment = assignment.copy()

    return bestAssignment, bestFitness




















if __name__ == "__main__":
    main()