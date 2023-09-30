import csv
from pprint import pprint 
import numpy as np

with open('./Catalog/catalog.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

numpyList = np.array(rows)

print (numpyList[:, 2])

# # Updates the column
# numpyList[:, 3] = range(0, 7921)

formatted_data = np.array([f'{row[0]}, "{row[1]}", "{row[2]}", "{row[3]}"' for row in numpyList])
# savedArray = np.asarray(numpyList)

np.savetxt('./Catalog/test.csv', formatted_data, delimiter=',', fmt='%s', header='col1,col2,col3,col4', comments='')