# Solveur de Sudoku avec SAT

## Instructions d'utilisation

1. GrilleToFormular.py
Placez le fichier wikiGrid.txt dans le même dossier que le script.
Executer : python GrilleToFormular.py
Génère automatiquement : `grille.txt`, `variables.txt`, `formular.cnf`

2. Résolution avec MiniSat où un logiciel SAT
Lancez la formule formular.cnf dans un solveur SAT (ex. MiniSat).
Sauvegardez le résultat dans un fichier example: <sat_output.txt>.

3. ValuationToSolution.py
Passez le fichier de sortie du solveur en argument lors de l’exécution :
python ValuationToSolution.py sat_output.txt
 La solution du Sudoku s’affichera directement dans la console.
