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