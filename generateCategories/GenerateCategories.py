import csv
import os

BasicIndustries = []
CapitalGoods = []
ConsumerDurables = []
ConsumerNonDur = []
ConsumerServices = []
Energy = []
Finance = []
HealthCare = []
Miscellaneous = []
PublicUtilities = []
Technology = []
Transportation = []

with open('companylist.csv') as prices_csv_file:
    info = list(csv.DictReader(prices_csv_file))
    for i in range(len(info)):
        if info[i]['Sector'] == 'Basic Industries':
            BasicIndustries.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Capital Goods':
            CapitalGoods.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Consumer Durables':
            ConsumerDurables.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Consumer Non-Durables':
            ConsumerNonDur.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Consumer Services':
            ConsumerServices.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Energy':
            Energy.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Finance':
            Finance.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Health Care':
            HealthCare.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Miscellaneous':
            Miscellaneous.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Public Utilities':
            PublicUtilities.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Technology':
            Technology.append(info[i]['Symbol'])
        elif info[i]['Sector'] == 'Transportation':
            Transportation.append(info[i]['Symbol'])

try:
    os.remove('BasicIndustries.txt')
except:
    pass

f = open('info.txt', 'w')
f.write('BasicIndustries = [')
for i in range(len(BasicIndustries)):
    if i == len(BasicIndustries) - 1:
        f.write('\'' + BasicIndustries[i] + '\'')
    else:
        f.write('\'' + BasicIndustries[i] + '\'' + ', ')
f.write(']\n')

f.write('CapitalGoods = [')
for i in range(len(CapitalGoods)):
    if i == len(CapitalGoods) - 1:
        f.write('\'' + CapitalGoods[i] + '\'')
    else:
        f.write('\'' + CapitalGoods[i] + '\'' + ', ')
f.write(']\n')

f.write('ConsumerDurables = [')
for i in range(len(ConsumerDurables)):
    if i == len(ConsumerDurables) - 1:
        f.write('\'' + ConsumerDurables[i] + '\'')
    else:
        f.write('\'' + ConsumerDurables[i] + '\'' + ', ')
f.write(']\n')

f.write('ConsumerNonDurables = [')
for i in range(len(ConsumerNonDur)):
    if i == len(ConsumerNonDur) - 1:
        f.write('\'' + ConsumerNonDur[i] + '\'')
    else:
        f.write('\'' + ConsumerNonDur[i] + '\'' + ', ')
f.write(']\n')

f.write('ConsumerServices = [')
for i in range(len(ConsumerServices)):
    if i == len(ConsumerServices) - 1:
        f.write('\'' + ConsumerServices[i] + '\'')
    else:
        f.write('\'' + ConsumerServices[i] + '\'' + ', ')
f.write(']\n')

f.write('Energy = [')
for i in range(len(Energy)):
    if i == len(Energy) - 1:
        f.write('\'' + Energy[i] + '\'')
    else:
        f.write('\'' + Energy[i] + '\'' + ', ')
f.write(']\n')

f.write('Finance = [')
for i in range(len(Finance)):
    if i == len(Finance) - 1:
        f.write('\'' + Finance[i] + '\'')
    else:
        f.write('\'' + Finance[i] + '\'' + ', ')
f.write(']\n')

f.write('HealthCare = [')
for i in range(len(HealthCare)):
    if i == len(HealthCare) - 1:
        f.write('\'' + HealthCare[i] + '\'')
    else:
        f.write('\'' + HealthCare[i] + '\'' + ', ')
f.write(']\n')

f.write('Miscellaneous = [')
for i in range(len(Miscellaneous)):
    if i == len(Miscellaneous) - 1:
        f.write('\'' + Miscellaneous[i] + '\'')
    else:
        f.write('\'' + Miscellaneous[i] + '\'' + ', ')
f.write(']\n')

f.write('PublicUtilities = [')
for i in range(len(PublicUtilities)):
    if i == len(PublicUtilities) - 1:
        f.write('\'' + PublicUtilities[i] + '\'')
    else:
        f.write('\'' + PublicUtilities[i] + '\'' + ', ')
f.write(']\n')

f.write('Technology = [')
for i in range(len(Technology)):
    if i == len(Technology) - 1:
        f.write('\'' + Technology[i] + '\'')
    else:
        f.write('\'' + Technology[i] + '\'' + ', ')
f.write(']\n')

f.write('Transportation = [')
for i in range(len(Transportation)):
    if i == len(Transportation) - 1:
        f.write('\'' + Transportation[i] + '\'')
    else:
        f.write('\'' + Transportation[i] + '\'' + ', ')
f.write(']\n')

f.close()
