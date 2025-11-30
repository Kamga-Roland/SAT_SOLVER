# CONFIGURATION
INPUT_FILE = 'wikiGrid.txt'
OUTPUT_FILE = 'grille.txt'
VARIABLE_FILE = 'variables.txt'
CNF_FORMULAR = 'formular.cnf'

GRID_SIZE = 9
DIGITS = range(1, 10)


# FILE I/O UTILITIES
def read_grid(filename):
    """Read grid from file and return as list of strings"""
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def save_to_file(filename, content):
    """Save content to file"""
    with open(filename, 'w') as file:
        file.write(content)


def normalize_grid(input_file, output_file):
    """Read grid, replace dots with zeros, and save to output file"""
    try:
        with open(input_file, 'r') as file:
            content = file.read()
        
        normalized = content.replace('.', '0')
        save_to_file(output_file, normalized)
        print(f"Normalized grid saved to {output_file}")
        return normalized
    
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# VARIABLE ENCODING
def var_id(row, col, digit):
    """Return variable ID for position (row, col) with digit
    """
    return row * 100 + col * 10 + digit


def generate_all_variables():
    """Generate all possible variables for 9x9 Sudoku grid
    Returns: List of lists where each inner list contains all variables for one cell
    """
    variables = []
    for row in DIGITS:
        for col in DIGITS:
            cell_vars = []
            for digit in DIGITS:
                cell_vars.append(var_id(row, col, digit))
            variables.append(cell_vars)
    return variables


def save_variables(variables, filename):
    """Save variables list to file"""
    try:
        save_to_file(filename, str(variables))
        print(f"Variables saved to {filename}")
    except Exception as e:
        print(f"Error saving variables: {e}")


# CNF CONSTRAINT GENERATORS
def at_least_one(vars_list):
    """Generate clause ensuring at least one variable is true"""
    return [vars_list]


def at_most_one(vars_list):
    """Generate clauses ensuring at most one variable is true (pairwise negation)"""
    clauses = []
    n = len(vars_list)
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([-vars_list[i], -vars_list[j]])
    return clauses


def exactly_one(vars_list):
    """Generate clauses to ensure exactly one variable in vars_list is true"""
    return at_least_one(vars_list) + at_most_one(vars_list)


def fix_value(var):
    """Generate clause to fix a variable as true"""
    return [[var]]


def exclude_value(var):
    """Generate clause to exclude a variable (set as false)"""
    return [[-var]]



# SUDOKU-SPECIFIC CONSTRAINT BUILDERS
def cell_constraints(grid_lines):
    """Generate constraints ensuring each cell has exactly one digit"""
    clauses = []
    
    for row_idx, line in enumerate(grid_lines, start=1):
        for col_idx, val in enumerate(line, start=1):
            cell_vars = [var_id(row_idx, col_idx, d) for d in DIGITS]
            
            if val != '0':
                # Fixed cell: enforce the given digit
                digit = int(val)
                clauses.extend(fix_value(var_id(row_idx, col_idx, digit)))
                
                # Exclude all other digits
                for d in DIGITS:
                    if d != digit:
                        clauses.extend(exclude_value(var_id(row_idx, col_idx, d)))
            else:
                # Empty cell: exactly one digit must be chosen
                clauses.extend(exactly_one(cell_vars))
    
    return clauses


def row_constraints():
    """Generate constraints ensuring each digit appears exactly once per row"""
    clauses = []
    for row in DIGITS:
        for digit in DIGITS:
            row_vars = [var_id(row, col, digit) for col in DIGITS]
            clauses.extend(exactly_one(row_vars))
    return clauses


def column_constraints():
    """Generate constraints ensuring each digit appears exactly once per column"""
    clauses = []
    for col in DIGITS:
        for digit in DIGITS:
            col_vars = [var_id(row, col, digit) for row in DIGITS]
            clauses.extend(exactly_one(col_vars))
    return clauses


def block_constraints():
    """Generate constraints ensuring each digit appears exactly once per 3x3 block"""
    clauses = []
    for block_row in range(3):
        for block_col in range(3):
            for digit in DIGITS:
                block_vars = []
                for row in range(block_row * 3 + 1, block_row * 3 + 4):
                    for col in range(block_col * 3 + 1, block_col * 3 + 4):
                        block_vars.append(var_id(row, col, digit))
                clauses.extend(exactly_one(block_vars))
    return clauses



# MAIN SUDOKU ENCODING
def generate_sudoku_clauses(grid_lines):
    """Generate all CNF clauses for Sudoku puzzle"""
    clauses = []
    clauses.extend(cell_constraints(grid_lines))
    clauses.extend(row_constraints())
    clauses.extend(column_constraints())
    clauses.extend(block_constraints())
    return clauses



# CNF FORMAT CONVERSION
def clauses_to_dimacs(clauses_list):
    """Convert clauses to DIMACS CNF format string"""
    all_vars = [abs(var) for clause in clauses_list for var in clause]
    num_vars = max(all_vars) if all_vars else 0
    num_clauses = len(clauses_list)
    
    lines = [f"p cnf {num_vars} {num_clauses}"]
    
    for clause in clauses_list:
        lines.append(" ".join(str(v) for v in clause) + " 0")
    
    return "\n".join(lines)


def generate_cnf_file(output_file):
    """Generate CNF file from processed grid"""
    try:
        grid_lines = read_grid(OUTPUT_FILE)
        clauses_list = generate_sudoku_clauses(grid_lines)
        cnf_string = clauses_to_dimacs(clauses_list)
        
        save_to_file(output_file, cnf_string)
        print(f"CNF file saved to {output_file}")
        return cnf_string
    except Exception as e:
        print(f"Error generating CNF: {e}")
        return None


# MAIN EXECUTION
if __name__ == "__main__":
    """Main workflow: normalize grid, generate variables, create CNF"""
    # Step 1: Normalize input grid
    normalize_grid(INPUT_FILE, OUTPUT_FILE)
    
    # Step 2: Generate and save all variables
    variables = generate_all_variables()
    save_variables(variables, VARIABLE_FILE)
    
    # Step 3: Generate CNF formula
    generate_cnf_file(CNF_FORMULAR)