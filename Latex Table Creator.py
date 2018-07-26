stockList = ['SJM4.csv', 'ADSK4.csv', 'WHR4.csv', 'HBAN4.csv', 'HES4.csv', 'WY4.csv', 'AMGN4.csv', 'MBI4.csv', 'GLW4.csv', 'HUM4.csv', 'AFL4.csv', 'LYB4.csv', 'FAST4.csv', 'HON4.csv', 'COL4.csv', 'PNC4.csv', 'AMP4.csv', 'CTXS4.csv', 'AKAM4.csv', 'WFC4.csv', 'SCHW4.csv', 'FTI4.csv', 'ADBE4.csv', 'CSCO4.csv', 'JWN4.csv', 'HOG4.csv', 'HPQ4.csv', 'EFX4.csv', 'RTN4.csv', 'FMCC4.csv', 'EXPE4.csv', 'BWA4.csv', 'LH4.csv', 'SHW4.csv', 'SBUX4.csv', 'MTG4.csv', 'VAR4.csv', 'LLY4.csv', 'WMT4.csv', 'TIF4.csv', 'MYL4.csv', 'GD4.csv', 'MAS4.csv', 'FITB4.csv', 'UST4.csv', 'XRAY4.csv', 'ORLY4.csv', 'TER4.csv', 'CLX4.csv', 'S4.csv', 'UIS4.csv', 'MUR4.csv', 'BBBY4.csv', 'GOOG4.csv', 'VLO4.csv', 'NOV4.csv', 'STI4.csv', 'TEX4.csv', 'FNMA4.csv', 'AMT4.csv', 'HRB4.csv', 'ED4.csv', 'RRC4.csv', 'NSC4.csv', 'WFT4.csv', 'BC4.csv', 'PFE4.csv', 'MU4.csv', 'ROK4.csv', 'DGX4.csv', 'BLL4.csv', 'CF4.csv', 'JCP4.csv', 'KR4.csv']

TABLE_LENGTH = 4
counter = 0
for i in stockList:
    if counter == TABLE_LENGTH - 1:
        print i + '\\\\'
    else:
        print i + ' & ',
    counter += 1
    if counter == TABLE_LENGTH:
        print '\\hline'
        counter = 0
print '\\hline'