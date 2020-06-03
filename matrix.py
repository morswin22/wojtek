from math import sqrt

"""Lu"""
def doolittle(matrix):
  """
  L * U = matrix
  :param matrix: Matrix to use Doolittle's algorithm on
  :return: matrix L and matrix U
  """
  # Matrix L with unknown quantities
  L = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
  for i in range(len(matrix)):
      L[i][i] = 1
  # Matrix U with unknown quantities
  U = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
  for i in range(len(matrix)):
    for j in range(i, len(matrix)):
      if j >= i:
        utemp = 0  # variable to temporary assign u[i][j] value
        for k in range(len(matrix)):
          utemp += L[i][k] * U[k][j]
        U[i][j] = matrix[i][j] - utemp
      ltemp = 0  # variable to temporary assign l[i][j] value
      if j > i:
        for k in range(len(matrix)):
          ltemp += L[j][k] * U[k][i]
        ltemp = matrix[j][i] - ltemp
        if U[i][i] != 0:
          L[j][i] = (ltemp / U[i][i])
  return L, U

"""Cholesky decomposition"""
def cholesky(matrix):
  """
  Lt * L = matrix
  :param matrix: matrix to decompose
  :return: L, Lt
  """
  # Matrix L with unknown quantities
  L = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
  for i in range(len(matrix)):
    L[i][i] = 1
  # Matrix Lt with unknown quantities
  Lt = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
  for i in range(len(matrix)):
    for j in range(len(matrix)):
      if j == i:
        stemp = 0
        for k in range(i):
          stemp += L[i][k] ** 2
        L[i][i] = sqrt(matrix[i][i] - stemp)
      if j > i:
        stemp = 0
        for k in range(i):
          stemp += L[j][k] * L[i][k]
        L[j][i] = (matrix[j][i] - stemp) / L[i][i]
  for i in range(len(matrix)):
    for j in range(len(matrix)):
      Lt[i][j] = L[j][i]
  return L, Lt

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
