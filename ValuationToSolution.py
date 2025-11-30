VALUATION_FILE = "valuation.txt"

def parse_minisat_output(output_text):
    """
    Parse MiniSat output and extract the valuation.
    
    Args:
        output_text (str): The output from MiniSat
        
    Returns:
        list: List of integers representing the valuation
    """
    lines = output_text.strip().split('\n')
    
    # Find the line starting with SAT
    valuation = []
    found_sat = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith('SAT'):
            found_sat = True
            # Get all remaining lines starting from this one
            remaining_text = ' '.join(lines[i:])
            parts = remaining_text.split()
            # Skip 'SAT' and '0' at the end if present, keep the numbers
            valuation = [int(x) for x in parts[1:] if x != '0' and x.lstrip('-').isdigit()]
            break
    
    return valuation if found_sat else []


def valuation_to_sudoku_grid(valuation):
    """
    Convert a valuation from MiniSat to a Sudoku grid.
    
    Args:
        valuation (list): List of integers (positive means true, negative means false)
        
    Returns:
        list: 9x9 grid with the Sudoku solution
    """
    # Initialize a 9x9 grid with zeros
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    # Process positive literals (true variables)
    for literal in valuation:
        if literal > 0:
            # Variable encoding: ijk where i=row, j=col, k=value
            var_str = str(literal)
            if len(var_str) == 3:
                row = int(var_str[0]) - 1  # Convert to 0-indexed
                col = int(var_str[1]) - 1  # Convert to 0-indexed
                value = int(var_str[2])
                grid[row][col] = value
    
    return grid


def print_sudoku_grid(grid):
    """
    Print the Sudoku grid in a readable format.
    
    Args:
        grid (list): 9x9 grid with the Sudoku solution
    """
    print("\nSudoku Solution:")
    print("+" + "-------+" * 3)
    
    for i in range(9):
        if i > 0 and i % 3 == 0:
            print("+" + "-------+" * 3)
        
        row_str = "|"
        for j in range(9):
            if j % 3 == 0 and j > 0:
                row_str += " |"
            row_str += f" {grid[i][j]}"
        row_str += " |"
        print(row_str)
    
    print("+" + "-------+" * 3)


def main():
    """
    Main function to read MiniSat output and display the Sudoku solution.
    """
    import sys
    
    # Read the valuation.txt file
    try:
        with open(VALUATION_FILE, 'r') as f:
            output_text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{VALUATION_FILE}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Parse the output
    valuation = parse_minisat_output(output_text)
    
    if not valuation:
        print("Error: Could not parse MiniSat output.")
        sys.exit(1)
    
    # Convert to Sudoku grid
    grid = valuation_to_sudoku_grid(valuation)
    
    # Print the solution
    print_sudoku_grid(grid)


if __name__ == "__main__":
    main()
