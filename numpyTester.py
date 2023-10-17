import numpy as np

matrix = [['FCTHNPE2IIOWM4S7DNA6RNF3', 'Train', '0.9839', 1, 0.729583919596127],['FCTHNPE2IIOWM4S7DNA6RNF3', 'Train', '0.9839', 0, 1], ['FCTHNPE2IIOWM4S7DNA6RNF3', 'Train', '0.9839', 3, 0.714541258858517], ['FCTHNPE2IIOWM4S7DNA6RNF3', 'Train', '0.9839', 0, 2]]

arr = np.array(matrix)
arr = arr[arr[:, 4].argsort()][::-1]

print(arr)