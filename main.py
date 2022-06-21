"""
INTRODUCTION
This program uses two external .CSV files:
DictionaryLabels.CSV - contains the column headers (labels) for a dataframe
fileinputs.CSV - contains a list of bank statements in CSV formats to be combined into one data frame,
    some files have a "-1" coefficient in an adjacent column if the file's dollar amount polarity needs to be reversed.
"""

import csv
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime

today=date.today()
now=datetime.now()
current_time = now.strftime("%H:%M:%S")

# pd.set_option("precision",2)
# Create DataFrames for the list of financial statements to be input, and for the dictionary of column labels
df_FileInputs = pd.read_csv("FileInputs.csv", engine='python')
df_DictionaryLabels = pd.read_csv("DictionaryLabels.csv", engine='python')

# Create a regular dictionary using 2 columns of the dataframe dictionary
# To debug, see this section in pdtest3A
DictionaryLabels = dict(zip(df_DictionaryLabels.iloc[:,1],df_DictionaryLabels.iloc[:,0],))
# print(DictionaryLabels)

"""
# DIAGNOSTIC START - OLD ------------------------------
 PRINTING THE ELEMENTS OF A DICTIONARY
dictionary_items = DictionaryLabels.items()
for item in dictionary_items:
  print(item)
# DIAGNOSTIC END  - OLD -------------------------------
"""

# Create an empty DataFrame named InputsAllDataFrame, using a dictionary created from the dictionary dataframe
df_InputsAll = pd.DataFrame(columns = DictionaryLabels.keys())  # empty dataframe

# Begin loop to fill df_InputsAll with data from all of the financial statements
for iter in df_FileInputs.itertuples(): #  ITERATE THROUGH DATA FILES

    # DIAGNOSTIC START - PRINTING THE ELEMENTS OF A DICTIONARY BIF
    print('Financial Statement File Name = ', iter[1], " , T_Sign = ", iter[2], "line 46") #
    # DIAGNOSTIC END

    # Read in data from the Financial Statement
    df_Statement = pd.read_csv(iter[1], index_col=False, engine='python') # void index column

    # Create Columns by assigning constant values to them
    df_Statement['FileSource'] = iter[1]
    df_Statement['FileDate'] = today
    df_Statement['FileTime'] = current_time
    # IMPORTANT - This is creating new columns by assignment
    print("BIF Iter[1]", iter[1], "line 57") # DIAGNOSTIC

    df_Statement.to_csv("Output.Test1.FirstReading.csv", index=False, mode='a')

    # CHANGE COLUMN LABELS, https://stackoverflow.com/questions/36531675/rename-columns-in-pandas-based-on-dictionary
    dict_labels = df_DictionaryLabels.set_index('KEY').to_dict() # make first column keys in new dictionary
    df_Statement.columns = df_Statement.columns.to_series().map(dict_labels['VALUE'])

    # TestForAMOUNT checks to see if AMOUNT column is blank
    # if AMOUNT column is blank, fill in the value from CREDIT or DEBIT columns

    TestForAMOUNT = "AMOUNT" in df_Statement # Does the Statement have an AMOUNT column?
    print("TestForAMOUNT ", TestForAMOUNT, "line 69")
    if TestForAMOUNT == True:
      df_Statement["AMOUNT"] = df_Statement["AMOUNT"] * int(iter[2]) # * 3 # polarity: multiply by T_Sign
      print("BIF Iter[2] line 72", iter[2])
      print(df_Statement)

      # OLD DIAGNOSTIC ---- START
      # print(df_Statement.head(5))
      # df_Statement.to_csv("TestOutput.csv", mode='w', index=False, float_format = '%.2f')
      # OLD DIAGNOSTIC ---- END

    else:
      # OLD DIAGNOSTIC ---- START
      # print("TestForAmount=FALSE, so insert column AMOUNT")
      # Create dummy list to insert as a column in df

      # list_AMOUNT = df_Statement.index
      # df_Statement.insert(2, "AMOUNT",list_AMOUNT, True)
      # IMPORTANT - this is way overcomplicated see line above like this:
      # df_Statement['FileDate'] = today
      # OLD DIAGNOSTIC ---- END

      # Set to numeric (decimals)
      df_Statement["AMOUNT"] = 3.00
      df_Statement["AMOUNT"] = pd.to_numeric(df_Statement["AMOUNT"], downcast="float")
      print(df_Statement)

      # Replace dummy value in AMOUNT with Value from CREDIT OR DEBIT

      TestForCREDIT = "CREDIT" in df_Statement.values # Does the Statement have a CREDIT column?
      TestForDEBIT = "DEBIT" in df_Statement.values # Does the Statement have a DEBIT column?
      print("test for credit, test for debit, line 99 approx")
      print(TestForCREDIT, TestForDEBIT, "***** line 100 approx")
      if TestForCREDIT == False:
        if TestForDEBIT == False:
          print(iter[1],"ERROR - CREDIT AND DEBIT COLUMNS ARE BLANK, line 104")
      #for loop2 in df_Statement.index:  #df_temp loops columns, df_temp.index loops rows, no () or [] needed here
      #for loop2 in df_Statement.itertuples():  #df_temp loops columns, df_temp.index loops rows, no () or [] needed here
      for loop2 in range(len(df_Statement)):  #df_temp loops columns, df_temp.index loops rows, no () or [] needed here
        #print(df_Statement.AMOUNT)
        #a=pd.isnull(df_Statement.CREDIT[iter2]) # is CREDIT empty?
        #b=pd.isnull(df_Statement.DEBIT[iter2])  # is DEBIT empty?

        # DANGER https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
        #returning-a-view-versus-a-copy
        #   df_Statement.AMOUNT[iter2] = float(df_Statement.CREDIT[iter2])
        # print("This is for AMOUNT line = ", loop2)
        print(loop2, " is loop2 line 115")
        a=df_Statement.at[loop2,"CREDIT"]
        b=df_Statement.at[loop2,"DEBIT"]
        c=df_Statement.at[loop2,"CREDIT"]
        d=df_Statement.isnull().at[loop2,"CREDIT"]
        e=2
        f=2
        print("a,b =  ",a,b, "line 122")
        print("c,d =  ", c, d, "line 123")

        # if d (is true), then Credit is null, so assign Debit to the Amount; ELSE assign Credit

        if d:
          print ("a is none, loop2 = ", loop2, "d TRUE = ", d, " CREDIT DEBIT = ", a, b)
          df_Statement.at[loop2,"AMOUNT"] = b
        else:
          print ("a is NOT none ------------so loop2 =", loop2, "d FALSE= ", d, " CREDIT DEBIT = ", a, b)
          df_Statement.at[loop2,"AMOUNT"] = a
        print("AMOUNT, CREDIT, DEBIT =", df_Statement.at[loop2,"AMOUNT"], df_Statement.at[loop2,"CREDIT"], df_Statement.at[loop2,"DEBIT"] )

        #if pd.isnull(df_Statement["CREDIT"]):
          #print("CREDIT is null, Filling AMOUNT column wdf_Statement.at[loop2,"AMOUNT"]ith DEBIT, so isnull=", pd.isnull(df_Statement.CREDIT[loop2]))
          #print("prior AMOUNT = ", df_Statement.loc[:,("AMOUNT")])
          #print("DEBIT is = ", df_Statement.loc[:,("DEBIT")])
          # df_Statement.loc[:,("AMOUNT")] = df_Statement.loc[:,("DEBIT")]   #ERROR, this writes a column NOT a cell
         # df_Statement.at[loop2,"AMOUNT"] = a
          #print("New AMOUNT is = ", df_Statement.loc[:,("AMOUNT")])
        #if pd.isnull(df_Statement.DEBIT[loop2]):
          #print("DEBIT is null, Filling AMOUNT column with CREDIT, so isnull=", pd.isnull(df_Statement.DEBIT[loop2]))
          #print("prior AMOUNT = ", df_Statement.loc[:,("AMOUNT")])
          #print("CREDIT is = ", df_Statement.loc[:,("CREDIT")])
          # df_Statement.loc[:,("AMOUNT")] = df_Statement.loc[:,("CREDIT")] #ERROR, this writes a column NOT a cell
        #   a=df_Statement.at[loop2,"CREDIT"]
          # df_Statement.at[loop2,"AMOUNT"] = a
          #print("New AMOUNT is = ", df_Statement.loc[:,("AMOUNT")])

      """print("/n here is df_Statement with AMOUNT filled in by CREDIT OR DEBI /n")
 

      print(df_Statement)
      df_Statement.to_csv("TestOutput.csv", mode='a', index=False)
      """
      print('-------------- PAUSE HERE ------- LINE 157 -----------------')

    """
    for (columnName, columnData) in df_Statement.iteritems(): # INTERATE THROUGH COLUMNS

      print('Colunm Name : ', columnName) 
      print('Column Contents : ', columnData.values, "  ",len(columnData.values)) 
    
    print("/n stop here /n")
    """

    print('-------------- PAUSE HERE ------- LINE 168 -----------------')
    print("df_InputsAll - INNER loop - pre assignment")
    print(df_InputsAll)
    # APPEND MODIFIED DATAFRAME TO PRIOR STATEMENTS
    df_InputsAll=df_InputsAll.append(df_Statement, ignore_index=True) # Append statement to prior statements
    print("df_InputsAll - INNER loop - POST assignment")
    print(df_InputsAll)
print("df_InputsAll - outer loop")
print(df_InputsAll)
#df_InputsAll.to_csv("TestOutputFinal.csv", mode='w', index=False, float_format = '%.2f')
df_InputsAll.to_csv("Output2.InputsAll.FINAL.csv", mode='w', index=False, float_format = '%.2f')

print("END OF PROGRAM --------------------------------------------------------")
"""
source file: PDTest9 based on PDTest7a.
"""
