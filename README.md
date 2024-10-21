# SAT-Solver
 Implementation of three SAT Solver algorithms: DPLL, WalkSAT, and GSAT. Included is a file of Conjutive Normal Form (CNF) formulas that are solved using the algorithms.


## DPLL (Davis-Putnam-Logemann-Loveland)
 DPLL is a backtracking-based algorithm that combines unit propagationand pure literal elimination. It explores all possible variable assignments until it finds a solution or proves the formula is unsatisfiable.

## WalkSAT
 WalkSAT is a local search algorithm that iteratively flips variables choosing between greedily minimizing the number of unsatisfied clauses and randomization.

## GSAT (Greedy SAT)
 GSAT is also a local search algorithm that iteratively flips variables that results in the greatest decrease in the number of unsatifised clauses, creating a "greedy" approach. Unlike WalkSAT, there is no randomization.

### Running the Code
**SAT1.py** contains class functions for DPLL and WalkSAT. Choose which SAT Solver to run (or both) in main().
**SAT2.py** contains GSAT.

Both are standalone code that can be ran with just the file. Note that **CNF Formulas** should be in the same directory as the python files.
