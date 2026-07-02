import pandas as pd

from IPython.display import HTML as html_print
from IPython.display import display

import re

import numpy as np

##############
##  Set Up  ##
##############

### Dataset Construction ###

def construct_dataset(data,id,new_year,new_year_num,old_year,old_year_num): # data to load, position of the id column, position of the new_year column, position of the old_year column

  nyn = 'y_'+ str(new_year_num)
  oyn = 'y_'+ str(old_year_num)

  dataset = pd.DataFrame({'Statement ID' : [],
                         nyn : [],
                         oyn : []})

  if id != False:

    dataset['Statement ID']=data.iloc[:, id].apply(int)
    dataset[nyn]=data.iloc[:, new_year].apply(str)
    dataset[oyn]=data.iloc[:, old_year].apply(str)

  else:
    dataset['Statement ID']= range(len(data))
    dataset[nyn]=data.iloc[:, new_year].apply(str)
    dataset[oyn]=data.iloc[:, old_year].apply(str)

  return dataset[['Statement ID',nyn,oyn]]

##############################
##  Text Reuse Definitions  ##
##############################

### IDENTIFY REUSE ###

def id_reuse(str1,str2,l):

  new1 = str1.lower().split()
  new2 = str2.lower().split()

  #print(new1)
  #print(new2)

  long_answer = []

  for i in range(0,len(new1)-1):
    for j in range(0,len(new2)-1):
      ans = []
      if new1[i]==new2[j]:
        n=i
        m=j
        while new1[n]==new2[m]:

          ans.append(new1[n])
          if n<len(new1)-1 and m<len(new2)-1:
            n+=1
            m+=1
          else:
            break


      if len(ans)>=len(long_answer):
        long_answer = list(ans)

  if len(long_answer) >= l:
    return" ".join(long_answer)

### IDENTIFY ALL REUSE ###

def reuse_loops2(str1,str2,l):

  ##################
  # Pre Processing

  m_str1 = str1.lower()
  m_str1 = re.sub('([a-zA-Z.,;!?()-])([.,;!?()-])', r'\1 \2', m_str1) #  !()-[]{};:'"\,<>./?@#$%^&*_~
  m_str1 = re.sub('([.,;!?()-])([a-zA-Z])', r'\1 \2', m_str1)
  m_str1 = m_str1.replace("  ", " ")
  m_str2 = str2.lower()
  m_str2 = re.sub('([a-zA-Z.,;!?()-])([.,;!?()-])', r'\1 \2', m_str2)
  m_str2 = re.sub('([.,;!?()-])([a-zA-Z])', r'\1 \2', m_str2)
  m_str2 = m_str2.replace("  ", " ")

  ##################
  # First Split

  # Get reused phrase
  reuse = id_reuse(m_str1,m_str2,l)

  if reuse != None:

    # split phrases string #1
    new_str = []
    #try:
    #  if m_str1 == reuse:
    #    print("YES")
    #    new_str.append((reuse,'black'))
    #  else:
    try:
      str1_pre = m_str1.split(reuse)[0]
      #print("m_str1:", m_str1)
      #print("reuse:", reuse)
      #print("pre:", str1_pre)
      #print(m_str1 == reuse)
      new_str.append((str1_pre, 'green'))
    except IndexError:
      False
    new_str.append((reuse,'black'))
    #print("reuse:", reuse)
    try:
      str1_post = m_str1.split(reuse)[1]
      new_str.append((str1_post, 'green'))
      #print("post:", str1_post)
    except IndexError:
      False
    #except IndexError:
    #    False
    #print(new_str)

    # split phrases string #2
    old_str = []
    try:
      str2_pre = m_str2.split(reuse)[0]
      old_str.append((str2_pre, 'red'))
    except IndexError:
      False
    old_str.append((reuse,'black'))
    try:
      str2_post = m_str2.split(reuse)[1]
      old_str.append((str2_post, 'red'))
    except IndexError:
      False
    #print(old_str[1][1])

    #####################
    # Additional Splits
    s = -1
    for s in range(round(int((len(m_str1.split()))/(l)),0)):

      #print('####')
      #print(s)
      #print(new_str)
      #print(old_str)

      s+=1

      for x in range(len(new_str)):
        if new_str[x][1] != 'black':
          for y in range(len(old_str)):
            if old_str[y][1] != 'black':
              #print('x is:', x)
              #print('str x is:', new_str[x][0])
              #print('y is:', y)
              #print('str y is:', old_str[y][0])
              reuse_a = id_reuse(new_str[x][0],old_str[y][0],l)
              if reuse_a == None:
                #print('reuse_a is: NONE')
                continue
              else:
                #print('reuse_a is:', reuse_a)

                # split phrases string #1
                g = x
                #print('g is:', g)
                m_str_1_a = new_str[g][0]
                #print(new_str[g][0])
                #print(m_str_1_a.split(reuse_a))
                new_str.pop(g)

                try:
                  str1_pre = m_str_1_a.split(reuse_a)[0]
                  #print(g, (str1_pre, 'green'))
                  new_str.insert(g,(str1_pre, 'green'))
                except IndexError:
                  False
                new_str.insert(g+1,(reuse_a,'black'))
                #print(g+1, (reuse_a,'black'))
                try:
                  str1_post = m_str_1_a.split(reuse_a)[1]
                  new_str.insert(g+2,(str1_post, 'green'))
                  #print(g+2, (str1_post, 'green'))
                except IndexError:
                  False

                #print(new_str)

                # split phrases string #2
                w = y
                #print('w is:', w)
                m_str_2_a = old_str[w][0]
                old_str.pop(w)

                try:
                  str2_pre = m_str_2_a.split(reuse_a)[0]
                  old_str.insert(w,(str2_pre, 'red'))
                except IndexError:
                  False
                old_str.insert(w+1,(reuse_a,'black'))
                try:
                  str2_post = m_str_2_a.split(reuse_a)[1]
                  old_str.insert(w+2,(str2_post, 'red'))
                except IndexError:
                  False

              #print(old_str)

  else:
    new_str = []
    new_str.append((m_str1, 'green'))

    old_str = []
    old_str.append((m_str2, 'red'))


  #####################
  return new_str, old_str

### Dataset to Dataset ###

def reuse_dataset_to_dataset(data,id,new_year,old_year,l):

  ny = data.columns[new_year]
  oy = data.columns[old_year]

  nt = ny+'_N_Text'
  ntw = ny+'_N_Text_WC'

  na = ny+'_Added'
  naw = ny+'_Added_WC'
  nr = ny+'_Reused'
  nrw = ny+'_Reused_WC'
  nter = ny+'_Terminated'
  nterw = ny+'_Terminated_WC'

  ot = ny+'_O_Text'
  otw = ny+'_O_Text_WC'

  rmnt = ny+'_New_Ratio_of_Match'
  rmot = ny+'_Old_Ratio_of_Match'
  njs = ny+'_Jaccard_Similarity'

  clean_data = pd.DataFrame(columns = ['Statement ID', nt, ntw, na, naw, nr, nrw, nter, nterw, ot, otw, rmnt, rmot, njs])

  for x in range(len(data)):

    id_num = data.iloc[x,id]
    new = data.iloc[x,new_year]
    old = data.iloc[x,old_year]

    new_str, old_str = reuse_loops2(new,old,l)

    added = ""
    added2 = ""
    reuse = ""
    reuse2 = ""
    removed = ""
    removed2 = ""

    # Reused text

    for x in range(len(new_str)):
      if new_str[x][1] != 'black':
        if added != "":
          added = " ".join([added, "[...]"])
        added = " ".join([added, new_str[x][0]])
        added2 = " ".join([added2, new_str[x][0]])
      else:
        if reuse != "":
          reuse = " ".join([reuse, "[...]"])
        reuse = " ".join([reuse, new_str[x][0]])
        reuse2 = " ".join([reuse2, new_str[x][0]])

    for x in range(len(old_str)):
      if old_str[x][1] != 'black':
        if removed != "":
          removed = " ".join([removed, "[...]"])
        removed = " ".join([removed, old_str[x][0]])
        removed2 = " ".join([removed2, old_str[x][0]])

        # Counts

    if new != "" and new != "nan" and new != " nan":
      new_wc = len(re.findall(r'\w+', new))
    else:
      new_wc = 0

    if added2 != "" and added2 != "nan" and added2 != " nan":
      added_wc = len(re.findall(r'\w+', added2))
    else:
      added_wc = 0

    if reuse2 != "" and reuse2 != "nan" and reuse2 != " nan":
      reuse_wc = len(re.findall(r'\w+', reuse2))
    else:
      reuse_wc = 0

    if removed2 != "" and removed2 != "nan" and removed2 != " nan":
      removed_wc = len(re.findall(r'\w+', removed2))
    else:
      removed_wc = 0

    if old != "" and old != "nan" and old != " nan":
      old_wc = len(re.findall(r'\w+', old))
    else:
      old_wc = 0

    # Reuse Calculations

    if new_wc != 0:
      rom_new = reuse_wc/new_wc
    else:
      rom_new = 0
    if old_wc != 0:
      rom_old = reuse_wc/old_wc
    else:
      rom_old = 0

    if new_wc == 0 and old_wc == 0 :
      jac_sim = 0
    else:
      jac_sim = reuse_wc/(added_wc + reuse_wc + removed_wc)

    clean_data = clean_data._append({'Statement ID':id_num,nt:new,ntw: new_wc, na:added, naw: added_wc, nr:reuse, nrw: reuse_wc, nter:removed, nterw: removed_wc, ot:old, otw: old_wc, rmnt: rom_new, rmot: rom_old, njs: jac_sim},ignore_index=True)
  return clean_data

###############
##  MERGING  ##
###############

### STRAINGHT MERGE ####

def straight_merge(new_df,old_df):

  n_suf = "_"+new_df.columns[1][:6]
  o_suf = "_"+old_df.columns[1][:6]

  matched_df = new_df.join(old_df.drop(old_df.columns[:1], axis=1), lsuffix=n_suf, rsuffix=o_suf)

  return matched_df

### STRAINGHT MERGE Text Only ####

def straight_merge_text_only(new_df,old_df):

  small_new_df = new_df.iloc[:, [0,1,3,5,7]]
  small_old_df = old_df.iloc[:, [1,3,5,7,9]]

  n_suf = "_"+new_df.columns[1][:6]
  o_suf = "_"+old_df.columns[1][:6]

  matched_df = small_new_df.join(small_old_df, lsuffix=n_suf, rsuffix=o_suf)

  return matched_df

##########################
##  LOOP THROUGH SHEET  ##
##########################

### SHEET LOOP ####

def sheet_loop(TAB,l):

  # get all column headings that contain the text "Stats" and put it into a list
  cols = [col for col in TAB.columns]
  c_prev = None
  results = []
  for i in range (len(cols) -1):
    c = construct_dataset(TAB,False,i,cols[i],i+1,cols[i+1])
    c_out = reuse_dataset_to_dataset(c,0,1,2,l)
    #print(c_out)
    if c_prev is not None:
      c_prev = straight_merge(c_prev,c_out)
    else:
      c_prev = c_out


  return c_prev

################
##  OUTPUTS   ##
################

### Print in Color ###

from IPython.display import HTML as html_print
from IPython.display import display

def cstr(s, color='black'):
    return "<text style=color:{}>{}</text>".format(color, s)

def print_color(t):
    display(html_print(' '.join([cstr(ti, color=ci) for ti,ci in t])))

### Single Color ###

def reuse_color_coded(str1,str2,l):
  new_str, old_str = reuse_loops2(str1,str2,l)

  # PRINT
  print('New Language:')
  print_color((new_str))

  print('Old Language:')
  print_color((old_str))

#####################################
## Patching and Packaging Measures ##
#####################################

def add_term_measures(file_name, out):

  from IPython import get_ipython
  from IPython.display import display

  # Mount google drive and go to subfolder
  # %%
  #from google.colab import drive
  #drive.mount('/content/drive')
  # %%
  import os
  import pandas as pd
  import re
  import numpy as np
  import math

###############################

  df = pd.DataFrame(file_name)

# identify strings to identify and keep within variable names
  pattern = r'(\d{4}).*(N_Text_WC|Added_WC|Terminated_WC|O_Text_WC)'
  #create empty list to hold column names (columns will be renamed with Year followed by one of the 3 expressions above (Text_WC, Added_WC, Terminated_WC))
  new_columns = []
  for col in df.columns:
    # find columns that match those strings and save to list
    match = re.search(pattern, col)
    if match:
      new_columns.append(f"{match.group(1)}_{match.group(2)}")
    else:
      new_columns.append(col)

  #print(new_columns) ### select based on the needed columns not all of the columns.....?

  #update columns in dataframe df to rename variables with names from 'new_columns' list
  df.columns = new_columns
  # check output
  #print("\nModified column names:")
  #print(df.columns)
  #print("\nModified DataFrame:")
  #print(df.head())


########################
#Filter data frame to only keep relevant variables
  pattern = 'N_Text_WC|Added_WC|Terminated_WC|Statement ID|O_Text_WC'
  filtered_df = df.filter(regex=pattern, axis=1)
  filtered_df.head()

#######################
# Reshape the data to get only 1 variable for each "Terminated_WC" "Added_WC" and "Text_WC" and multiple rows for each statement id (corresponding to different years). The year that was in the variables names will now appear as a new variable.  I keep Text_WC in case we want to weight the statements unequally (by length of the statement) when computing the Gini coefficient over the whole policy for each year.
  # Melt the DataFrame to long format, specify the content in the name of the variables to extract info about (to populate "year", "Terminated_WC", "Added_WC", and "Text_WC" variables), and specify the id for the statements that are repeated over time and will have multiple observations after reshaping
  df_melted = pd.melt(filtered_df, id_vars=['Statement ID'], var_name='year_variable', value_name='value')

  #######################
  # Extract the year and variable name from the 'year_variable' column
  df_melted['year'] = df_melted['year_variable'].str.extract(r'(\d{4})')  # Extract year
  df_melted['variable'] = df_melted['year_variable'].str.extract(r'_(.*)')  # Extract the variable name (N_Text_WC, Terminated_WC, Added_WC, O_Text_WC)

  # Drop the 'year_variable' column as it's no longer needed
  df_melted = df_melted.drop(columns=['year_variable'])

  # Pivot the DataFrame to have separate columns for Terminated_WC, Added_WC, and Text_WC. Save as a new data frame called "df_pivot"
  df_pivot = df_melted.pivot_table(index=['Statement ID', 'year'], columns='variable', values='value', aggfunc='first').reset_index()

  # Replace missing values (NaN) with 0 (these are for the variables "Added_WC" and "Terminated_WC" in the first year, it is not possible to identify them as a "." if we want to conver the strings containing counts to a numerical format after.
  df_pivot['Terminated_WC'] = df_pivot['Terminated_WC'].astype(float).fillna(0)
  df_pivot['Added_WC'] = df_pivot['Added_WC'].astype(float).fillna(0)
  df_pivot['N_Text_WC'] = df_pivot['N_Text_WC'].astype(float).fillna(0)
  df_pivot['O_Text_WC'] = df_pivot['O_Text_WC'].astype(float).fillna(0)

  # Convert to integers
  df_pivot['Terminated_WC'] = df_pivot['Terminated_WC'].astype(int)
  df_pivot['Added_WC'] = df_pivot['Added_WC'].astype(int)
  df_pivot['N_Text_WC'] = df_pivot['N_Text_WC'].astype(int)
  df_pivot['O_Text_WC'] = df_pivot['O_Text_WC'].astype(int)

  # Remove Rows that have no Word Count
  df_pivot['Text_WC'] = df_pivot['N_Text_WC'] + df_pivot['O_Text_WC']
  df_pivot = df_pivot[df_pivot['Text_WC'] != 0] # <------------------------------------------------------------------------------------------------- a problem of zeros?

  # Flatten the multi-level columns
  df_pivot.columns.name = None  # Remove the column name
  df_pivot = df_pivot.rename(columns={'Terminated_WC': 'Terminated_WC', 'Added_WC': 'Added_WC', 'N_Text_WC': 'N_Text_WC', 'O_Text_WC': 'O_Text_WC'})

  # Print the reshaped DataFrame
  df_pivot['Total_WC_change'] = df_pivot['Added_WC'] + df_pivot['Terminated_WC']

###################################
# Compute Termination and Addition Ratios for each statement
  df_pivot['Ratio_of_Term'] = np.where(df_pivot['O_Text_WC'] > 0 , df_pivot['Terminated_WC'] / (df_pivot['O_Text_WC']), 0 )
  #df_pivot['Ratio_of_Term'] = df_pivot['Terminated_WC'] / (df_pivot['O_Text_WC'])
  df_pivot['Ratio_of_Term'] = df_pivot['Ratio_of_Term'].astype(float).fillna(0)

  df_pivot['Ratio_of_Add'] = np.where(df_pivot['N_Text_WC'] > 0 , df_pivot['Added_WC'] / (df_pivot['N_Text_WC'] ), 0 )
  #df_pivot['Ratio_of_Add'] = df_pivot['Added_WC'] / (df_pivot['N_Text_WC'] )
  df_pivot['Ratio_of_Add'] = df_pivot['Ratio_of_Add'].astype(float).fillna(0)

###################################
# Compute the gini coefficient as the relative mean absolute difference. From Wikipedia: "An alternative approach is to define the Gini coefficient as half of the relative mean absolute difference, which is equivalent to the definition based on the Lorenz curve. The mean absolute difference is the average absolute difference of all pairs of items of the population, and the relative mean absolute difference is the mean absolute difference divided by the average, x¯ , to normalize for scale". https://en.wikipedia.org/wiki/Gini_coefficient. I use a simplified formula that exploits the fact that sorting the data in ascending order and taking the difference between the cumulative sum between Xi and Xi-1 is equivalent to taking the absolute differences of all possible pairs of individuals in the set.
  # Sort the entire DataFrame by 'year' and 'Total_WC_change', in ascending order
  df_sorted = df_pivot.sort_values(by=['year', 'Total_WC_change'], ascending=[True, True])
  #Check that it sorted properly
  #print(df_sorted)

  #### Termination Gini
  # Add rank within each year based on 'Terminated_WC'
  df_sorted['Term_rank'] = df_sorted.groupby('year')['Terminated_WC'].rank(method='first', ascending=True)
  # Print the sorted DataFrame with ranks (rank is the i in the numerator of the formula)
  #print("\nSorted DataFrame with Ranks:\n", df_sorted)
  #reset the index year that was created during the reshape of the data
  df_sorted = df_sorted.reset_index()

  # Create year-specific n and add as a column to data frame
  df_sorted['n_year'] = df_sorted.groupby('year')['Term_rank'].transform('count')
  # Calculate the 'cumulative_term' using the new 'n_year' column
  df_sorted['Term_cumulative_term'] = (2 * df_sorted['Term_rank'] - df_sorted['n_year'] - 1) * df_sorted['Terminated_WC'] ### Should these be negative?

  #### Addition Gini
  # Add rank within each year based on 'Terminated_WC'
  df_sorted['Add_rank'] = df_sorted.groupby('year')['Added_WC'].rank(method='first', ascending=True)
  # Print the sorted DataFrame with ranks (rank is the i in the numerator of the formula)
  #print("\nSorted DataFrame with Ranks:\n", df_sorted)
  #reset the index year that was created during the reshape of the data
  df_sorted = df_sorted.reset_index()

  # Create year-specific n and add as a column to data frame
  df_sorted['n_year'] = df_sorted.groupby('year')['Add_rank'].transform('count')
  # Calculate the 'cumulative_term' using the new 'n_year' column
  df_sorted['Add_cumulative_term'] = (2 * df_sorted['Add_rank'] - df_sorted['n_year'] - 1) * df_sorted['Added_WC'] ### Should these be negative?


###############################
# Create new dataframe to host numerator and denumerato data and to do final Gini coefficient calculation

  #### Termination Gini
  # Calculate the numerator (sum of 'cumulative_term' for each year)
  Gini_df = df_sorted.groupby('year')['Term_cumulative_term'].sum().reset_index()
  # Rename the column to 'numerator'
  Gini_df = Gini_df.rename(columns={'Term_cumulative_term': 'Term_numerator'})
  # Calculate the sum of Total_WC_change for each year and add it as a column
  Gini_df['Term_Sum_Xi'] = df_sorted.groupby('year')['Terminated_WC'].sum().values
  # calculate the denominator (sum of Xis * n_year)
  Gini_df['Term_denominator'] = Gini_df['year'].map(df_sorted.groupby('year')['n_year'].first()) * Gini_df['Term_Sum_Xi']
  # Drop unneeded Sum_Xi variable
  Gini_df.drop(columns=['Term_Sum_Xi'], inplace=True)
  # Calculate Gini
  Gini_df['Term_Gini'] = 1 - (Gini_df['Term_numerator'] / Gini_df['Term_denominator'])
  # Print the new DataFrame

  #### Addition Gini
  # Calculate the numerator (sum of 'cumulative_add' for each year)
  Gini_df['Add_numerator'] = Gini_df['year'].map(df_sorted.groupby('year')['Add_cumulative_term'].sum())
  # Calculate the sum of Total_WC_change for each year and add it as a column
  Gini_df['Add_Sum_Xi'] = df_sorted.groupby('year')['Added_WC'].sum().values
  # calculate the denominator (sum of Xis * n_year)
  Gini_df['Add_denominator'] = Gini_df['year'].map(df_sorted.groupby('year')['n_year'].first()) * Gini_df['Add_Sum_Xi']
  # Drop unneeded Sum_Xi variable
  Gini_df.drop(columns=['Add_Sum_Xi'], inplace=True)
  # Calculate Gini
  Gini_df['Add_Gini'] = 1 - (Gini_df['Add_numerator'] / Gini_df['Add_denominator'])
  # Print the new DataFrame
  #print(Gini_df)

###############################
# Add depth of change measures to the new dataframe

  #### Termination Depth
  # Calculate the sum of 'Ratio_of_Term' for each year
  Gini_df['Term_sum'] = Gini_df['year'].map(df_sorted.groupby('year')['Ratio_of_Term'].sum())
  # Calculate the the non zero values of 'Ratio_of_Term' for each year
  years = Gini_df['year'].to_list()
  counts = []
  for year in years:
    count = ((df_sorted['year'] == year) & (df_sorted['Ratio_of_Term'] > 0) ).sum()
    counts.append(count)
  # Map counts back to Gini_df
  counts_df = pd.DataFrame({'year': years, 'Term_count': counts})
  Gini_df = pd.merge(Gini_df, counts_df, on='year', how='left')

  # find average depth
  #if Gini_df['Term_count'] != 0:
  Gini_df['Term_depth'] = Gini_df['Term_sum'] / Gini_df['Term_count']
  #else:
  #  Gini_df['Term_depth'] = 0


  #### Addition Depth
  # Calculate the sum of 'Ratio_of_Add' for each year
  Gini_df['Add_sum'] = Gini_df['year'].map(df_sorted.groupby('year')['Ratio_of_Add'].sum())
  # Calculate the the non zero values of 'Ratio_of_Add' for each year
  years = Gini_df['year'].to_list()
  counts = []
  for year in years:
    count = ((df_sorted['year'] == year) & (df_sorted['Ratio_of_Add'] > 0) ).sum()
    counts.append(count)
  # Map counts back to Gini_df
  counts_df = pd.DataFrame({'year': years, 'Add_count': counts})
  Gini_df = pd.merge(Gini_df, counts_df, on='year', how='left')

  # find average depth
  #if Gini_df['Term_count'] != 0:
  Gini_df['Add_depth'] = Gini_df['Add_sum'] / Gini_df['Add_count']
  #else:
  #  Gini_df['Term_depth'] = 0

###########################
# Fill in unbalanced evolution
  for p in range(len(Gini_df)):
    if math.isnan(Gini_df['Term_depth'].iloc[p]) and Gini_df['Add_depth'].iloc[p] > 0:
      Gini_df.loc[p, 'Term_depth'] = 0
      Gini_df.loc[p, 'Term_Gini'] = 1
    if math.isnan(Gini_df['Add_depth'].iloc[p]) and Gini_df['Term_depth'].iloc[p]> 0:
      Gini_df.loc[p, 'Add_depth'] = 0
      Gini_df.loc[p, 'Add_Gini'] = 1

###########################
  #print(df_pivot['Ratio_of_Term'], df_pivot['Terminated_WC'], df_pivot['O_Text_WC'])
###########################
#select output
  Output_df = Gini_df[['year', 'Term_Gini', 'Term_depth', 'Add_Gini','Add_depth']]
  if out == 1:
    return(Output_df)
  elif out == 2:
    return(df_sorted)
  else:
     print("Invalid 'out' input")


##############
## Plotting ##
##############

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import math
import matplotlib.lines as mlines

def plot_term_add(data, width_thresh, depth_thresh):

  data = data.reset_index()

  # Produce figure
  plt.scatter(data['Add_depth'], data['Add_Gini'], facecolors='none', edgecolors='blue', s=40, marker='o') # Plots the line and marks the points
  plt.scatter(data['Term_depth'], data['Term_Gini'], c='blue', s=40, marker='x') # Plots the line and marks the points
  plt.plot([data['Term_depth'], data['Add_depth']], [data['Term_Gini'], data['Add_Gini']], '--k', lw=0.5, zorder = -1)

  # add year
  for i, txt in enumerate(data['year']):
    if not math.isnan(data.loc[i, 'Add_depth']) and not math.isnan(data.loc[i, 'Add_Gini']):
      plt.annotate(txt, (data.loc[i, 'Add_depth']+0.01, data.loc[i, 'Add_Gini']-0.01))

  # Create marker legend
  plot_marker = []
  m1, = plt.plot([], [], 'x', color='black')
  m2, = plt.plot([], [], 'o', mfc='none', mec='black')
  plot_marker.append([m1, m2])
  legend1 = plt.legend(plot_marker[0], ['Termination', 'Addition'], loc=(1.01,0.8),title="Change Type")
  plt.gca().add_artist(legend1)
  plt.tight_layout()  # Prevents the legend from getting cut off

  plt.grid(True) # Adds a grid for better visualization
  plt.xlim(0, 1)  # Set x-axis range
  plt.ylim(0, 1)  # Set y-axis range
  plt.xlabel("Average Depth of Evolution \n (Termination and Addition)") # x-axis label
  plt.ylabel("Concentration of Evolution") # x-axis label

  # Plot Grid and Quadrents
  plt.xlim(-0.1, 1.1)  # Set x-axis range
  plt.ylim(-0.1, 1.1)  # Set y-axis range
  plt.axvline(x=depth_thresh, linewidth=1, color='r', ls='--', zorder = -2)
  plt.axhline(y=width_thresh, linewidth=1, color='r', ls='--', zorder = -2)
  plt.xlabel("Average Depth of Evolution \n (Termination and Addition)") # x-axis label
  plt.ylabel("Width of Evolution") # x-axis label

  # Table #5 Lables
  x = [-0.05, 1.025,-0.05, 1.025]
  y = [1.025, 1.025,-0.05,-0.05]
  labels = ['C', 'D', 'A', 'B']

  # Add labels to each point
  for i, txt in enumerate(labels):
    plt.annotate(txt, (x[i], y[i]), c='r',
             fontsize=12, fontweight='bold')

  plt.show()
