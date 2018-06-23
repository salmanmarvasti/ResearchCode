import os
from VARIABLES import ADDRESS_TO_FILES, ADDRESS_TO_UPDATED_FILES

nameList = os.listdir(ADDRESS_TO_FILES)
names = []

for i in nameList:
    if i[len(i)-3: len(i)] == 'csv':
        names.append(i[0: len(i)-4])

nameListUpdated = os.listdir(ADDRESS_TO_UPDATED_FILES)
namesUpdated = []

for i in nameListUpdated:
    if i[len(i)-3: len(i)] == 'csv':
        namesUpdated.append(i[0: len(i)-4])


result = []
for i in names:
    if i not in namesUpdated:
        result.append(i)

print result
