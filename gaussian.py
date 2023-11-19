import argparse
import sys
filename = sys.argv[1]
parser = argparse.ArgumentParser()

# Arg Flag for enabling Scaled Partial Pivoting
parser.add_argument('-spp', dest='isSPPEnabled', action='store_const',
                    const=True, default=False,
                    help='Adds Scaled Partial Pivoting to Gaussian Equation')
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

# Read data from input file and initialize variables and matricies
length = int(args.file.readline())
matrix = []
augmented_matrix = []
constants_vector = []
solution_vector = []

# Reading file one word/number at a time
for line in args.file:
    a = []
    for word in line.split():
        a.append(float(word))
    matrix.append(a)

# Sort into augmented matrix and initialize solution vector
for row in range(length):
    augmented_matrix.append(matrix[row])
constants_vector = matrix[length]
for x in range(length):
    augmented_matrix[x].append(constants_vector[x])

for i in range(length):
    solution_vector.append(0)

# Apply Scaled Partial Pivoting if flagged
if args.isSPPEnabled:
    l = [0 for x in range(length)]
    s = [0.0 for x in range(length)]
    for i in range(length):
        l[i] = i
        smax = 0.0
        for j in range(length):
            if abs(augmented_matrix[i][j]) > smax:
                smax = abs(augmented_matrix[i][j])
        s[i] = smax

# Apply Gaussian Elimination
for i in range(length):
    if augmented_matrix[i][i] == 0.0:
        quit('Divide by zero detected!')
        
    for j in range(i+1, length):
        ratio = augmented_matrix[j][i]/augmented_matrix[i][i]
        
        for k in range(length+1):
            augmented_matrix[j][k] = augmented_matrix[j][k] - ratio * augmented_matrix[i][k] 

# Back Substitution
solution_vector[length-1] = augmented_matrix[length-1][length]/augmented_matrix[length-1][length-1]

for i in range(length-2,-1,-1):
    solution_vector[i] = augmented_matrix[i][length]
    
    for j in range(i+1,length):
        solution_vector[i] = solution_vector[i] - augmented_matrix[i][j]*solution_vector[j]
    
    solution_vector[i] = solution_vector[i]/augmented_matrix[i][i]

# Print matrix solution and store solution into output file
output_file = open('./sys1.sol','a')
if args.isSPPEnabled:
    output_file.write("Solution with Scaled Partial Pivoting\n")
else:
    output_file.write("Solution with Naive Gaussian Elimination\n")

for i in range(length):
    output_file.write('X%d = %0.2f\n' %(i,solution_vector[i]))
output_file.write("\n")
output_file.close()
