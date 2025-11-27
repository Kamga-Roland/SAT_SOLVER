INPUT_FILE = 'wikiGrid.txt'
OUTPUT_FILE = 'grille.txt'
VARIABLE_FILE = 'variables.txt'
CNF_FORMAT = 'cnf_format.txt'

def read_and_process_file():
    """Read wikiGrid.txt, replace dots with zeros, and save to output file"""
    try:
        # Read the input file
        with open(INPUT_FILE, 'r') as file:
            content = file.read()
        
        # Replace dots with zeros
        output_content = content.replace('.', '0')
        
        # Save to output file
        with open(OUTPUT_FILE, 'w') as file:
            file.write(output_content)
        
        print(f"\nModified content saved to {OUTPUT_FILE}")
        return output_content
    
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None



def generate_variables():
    variables = []
    
    # Generate 9 lists
    for i in range(1, 10):  # i from 1 to 9 (list index)
        inner_list = []
        
        # Generate variables from i11 to i99 (89 variables per list)
        for var in range(i * 100 + 11, i * 100 + 100):  # e.g., 111 to 199, 211 to 299, etc.
            inner_list.append(var)
        
        variables.append(inner_list)
    
    # Save to variables.txt
    try:
        with open(VARIABLE_FILE, 'w') as file:
            file.write(str(variables))
        print("Variables saved to variables.txt")
    except Exception as e:
        print(f"Error saving to variables.txt: {e}")
    
    return variables


def cnf_format():
    """Convert from grille.txt into CNF format string and save to cnf_format.txt"""
    try:
        with open(VARIABLE_FILE, 'r') as file:
            content = file.read()
            variables = eval(content)

        cnf_lines = []
        all_vars = [var for sublist in variables for var in sublist]
        num_vars = max(all_vars)
        num_clauses = len(all_vars)

        # Header line
        cnf_lines.append(f"p cnf {num_vars} {num_clauses}")

        # Each variable as a clause
        for var in all_vars:
            cnf_lines.append(f"{var} 0")

        cnf_string = '\n'.join(cnf_lines)

        # Save CNF to file
        with open(CNF_FORMAT, 'w') as file:
            file.write(cnf_string)

        print(f"CNF format saved to {CNF_FORMAT}")
        return cnf_string

    except FileNotFoundError:
        print("Error: variables.txt not found")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    """Main workflow: process grid, generate variables, convert to CNF"""
    read_and_process_file()
    generate_variables()
    cnf_format()