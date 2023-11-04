"""
SLPPY
Simplex LInear Programming module for PYthon.
developed by:
        Tanmay Verma
        aka. Buggermenot

Can solve some linear maximization optimization problems using the simplex method

Mat = [-, x1, x2, s1, s2, s3, rhs, ratio
       z, -1, -4, 0 , 0 , 0 ,  0 ,   -  
       ... ]    

call slippy.simplex() to give input and solve

"""

def simplex():
        nvar = int(input("Enter number of Variables: "))
        ncon = int(input("Enter number of Constraints: "))

        print("\nDefining the Optimization Function z =", end=" ")
        for i in range(1, nvar):
                print(f'a{i}x{i}', end=" + ")
        print(f'a{nvar}x{nvar}')

        z = list(map(int, input("Enter the values of ai in series as => a1, a2, a3, ..., an: ").split()))

        for _ in range(len(z), nvar):
                z.append(0)

        print("\nDefine Constraints")
        print("Constraints defined as:", end = " ")
        for i in range(1, nvar):
                print(f'a{i}x{i}', end=" + ")
        print(f'a{nvar}x{nvar} <= bound')


        constraints = []
        bounds = []

        for i in range(ncon):
                print(f"Constraint {i+1}:")
                s = list(map(int, input("Enter the values of ai in series as => a1, a2, a3, ..., an: ").split()))
                b = int(input("Enter the bound value: "))

                for _ in range(len(s), nvar):
                        s.append(0)

                constraints.append(s)
                bounds.append(b)
        vars = [f'x{i}' for i in range(1, nvar+1)]
        slack = [f's{i}' for i in range(1, ncon+1)]

        print("\nAll inputs taken")
        print("Displaying full problem:\n")

        print("Maximize z =", end=" ")
        for i in range(nvar-1):
                print(f'{z[i]} * {vars[i]}', end=" + ")
        print(f'{z[nvar-1]} * {vars[nvar-1]}\n')

        print("Constraints: ")
        for i in range(ncon):
                s = constraints[i]
                for j in range(nvar-1):
                        print(f'{s[j]} * {vars[j]}', end=" + ")
                print(f'{s[nvar-1]} * {vars[nvar-1]} <= {bounds[i]}')
        
        print(", ".join(vars), ">= 0")

        if input("Continue? "):
                print("Restarting problem input")
                return simplex()
        

        mat = [['-'] + vars + slack + ['rhs', 'ratio']]
        # Z
        row = ['z'] + [-i for i in z] + [0 for _ in range(ncon)] + [0, 0] 
        mat.append(row)

        for i in range(ncon):
                row = [f's{i+1}'] + constraints[i] + [1 if j==i else 0 for j in range(ncon)] + [bounds[i]] + [0]
                mat.append(row)
        
        return solve(mat, vars)



def solve(mat: list[list]=[[]], vars:list=[]):
        print("Solving Optimization problem with Simplex")
        
        display(mat)
        display(iterate(mat, vars))

def display(mat: list[list]):
        mx = 0
        for row in mat:
                for ele in row:
                        if len(str(ele)) > mx:
                                mx = len(str(ele))
        
        for row in mat:
                for ele in row:
                        e = str(ele)
                        print(' ' * (mx - len(e)) + e, end = ", ")
                print()
        

def getRC(mat: list[list]) -> (int, int):
        key_col = -1

        row0 = mat[1]

        # Best column
        for i in range(1, len(row0) - 1):
                if row0[i] >= 0:
                        continue
                
                if row0[i] < row0[key_col] or key_col == -1: 
                        key_col = i
        
        if key_col == -1:
                # Terminated
                return -1, -1
        
        # Get Smallest Positive Ratio
        for j in range(1, len(mat)):
                try:
                        mat[j][-1] = mat[j][-2] / mat[j][key_col]
                except ZeroDivisionError:
                        mat[j][-1] = mat[j][-2] / zero
        
        print("Update Ratio")
        display(mat)

        # Best Row
        key_row = -1
        for j in range(1, len(mat)):
                if mat[j][-1] <= 0:
                        continue
                
                if mat[j][-1] < mat[key_row][-1] or key_row == -1:
                        key_row = j

        return key_row, key_col

def iterate(mat:list[list], vars: list):
        key_row, key_col = getRC(mat)
        if key_col == -1:
                print("Results found")
                getSolution(mat, vars)
                print("Thank you for using slippy :D")
                exit()

        if key_row == -1:
                print("No Solutions")
                print("Thank you for using slippy :D")
                exit()
        print(key_row, key_col)
        

        # Divide key row by key element
        key_ele = mat[key_row][key_col]
        if not key_ele:
                key_ele = zero


        mat[key_row] = [mat[0][key_col]] + [i / key_ele for i in mat[key_row][1:-1]] + [mat[key_row][-1]]

        for i in range(1, len(mat)):
                if i == key_row:
                        continue
                div = mat[i][key_col]
                if not div:
                        div = zero

                mat[i] = [mat[i][0]] + [mat[i][col] - div * mat[key_row][col] for col in range(1, len(mat[0]) - 1)] + [mat[i][-1]] 

        display(mat)
        return iterate(mat, vars)


def getSolution(mat: list[list], vars: list):
        vars = dict([(v, 0) for v in vars])
        print(f"Optimized value of z = {mat[1][-2]}")
        for i in range(2, len(mat)):
                if mat[i][0] in vars.keys():
                        vars[mat[i][0]] = mat[i][-2]

        print("Values: ")
        for k, v in vars.items():
                print(f'{k}: {v}')