def determinant(A):
    """
    Return the determinant
    :param A: sqare matrix
    :return: the determinant
    """
    first_row = list(range(len(A)))
    det = 0
    if len(A) == 2 and len(A[0]) == 2:
        det = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return det

    for i in first_row:
        copy_of_A = A[1:]

        for j in range(len(copy_of_A)): 
            copy_of_A[j] = copy_of_A[j][0:i] + copy_of_A[j][i+1:] 

        temp_det = determinant(copy_of_A)
        det += (-1) ** (i % 2) * A[0][i] * temp_det

    return det

def minor(A, i, j):
    """
    return minor Aij
    :param A: matrix
    :param i: row number
    :param j: column number
    :return: minor - determinant of A without i row and j column
    """
    A.pop(i)
    for i in range(len(A)):
        A[i] = A[i][:j] + A[i][j + 1:]
    return determinant(A)

def matrixMultiplication(A, B):
    """
    A*B
    :param A: matrix A
    :param B: matrix B
    :return: A x B
    """
    if len(A) == len(B) == len(A[0]) == len(B[0]):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s = 0
                for k in range(n):
                    s += A[i][k] * B[k][j]
                C[i][j] = s
        return C
    else:
        raise ValueError("Number of columns of matrix A must be equal to number of rows of matrix B")


def inverse(A):
    """
    Inverse matrix
    :param A: matrix
    :return: inverted Matrix
    """
    det = determinant(A)
    if det != 0:
        cofactorA = [[0 for _ in range(len(A))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(A)):
                cofactorA[i][j] = minor(A[:], i, j)
        invertedMatrix = [[0 for _ in range(len(A))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(A)):
                invertedMatrix[i][j] = 1./det * cofactorA[j][i]
        return invertedMatrix

    else:
        raise ValueError("Cannot inverse this matrix")

def trace(A):
    """
    Return trace
    :param A: matrix
    :return: trace
    """
    if len(A) == len(A[0]):
        tr = 0
        for i in range(len(A)):
            tr += A[i][i]
        return tr
    else:
        raise ValueError("Number of columns of matrix A must be equal to number of rows of matrix B")
