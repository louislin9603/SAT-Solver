
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
                    print(f"Reading line: {line}")

                    # Skip comments and last line with '%'
                    if line.startswith('c') or line.startswith('%'):
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




def main():
    print("Main ran")

    cnf_files = ["CNF Formulas\\uf20-0156.cnf"]

    for file_name in cnf_files:

        cnf = CNFFormula()

        if cnf.parse_dimacs(file_name):
            print(f"Successfully parsed {file_name}")
            print(f"Numbeer of variables: {cnf.num_variables}")
            print(f"Number of clauses: {cnf.num_clauses}")
            for clause in cnf.clauses:
                print(clause)
            print(f"Distinct variables: {cnf.variables}")




















if __name__ == "__main__":
    main()