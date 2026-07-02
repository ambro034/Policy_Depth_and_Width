# Policy_Depth_and_Width
## Python functions for evaluating the the depth and with of policy change.

Paper Citation: Ambrose, G. and Gregoire-Zawilski, M., Mapping Measurement to Theory in Policy Evolution: A Case of Net Metering Policies of the United States. Policy Studies Journal, https://doi.org/10.1111/psj.70133.


We offer a new approach for measuring dynamics of patching and packaging, proposing three dimensions of a single measure evaluating evolution in policy text: (1) depth: the extent of change, on average, across policy statements, (2) width: how these changes are distributed across the policy, and (3) the (a)symmetry of depth and width across added and terminated text. With these three dimensions, we offer a more nuanced exploration of patching and packaging dynamics.

## Getting Started

These instructions will outline installation, a description of the functions, as well as identify examples.

# Table of Contents
1. [Installing](#Installing)
2. [Functions](#Functions)
   - [Practical Reuse Functions](#Construct-Base-Datasets)
   - [Color-coded Reuse Evaluation](#Color-coded-Reuse-Evaluation)
   - [Construct Reuse Dataset](#Construct-Reuse-Dataset)
   - [Policy Depth and Width](#Policy-Depth-and-Width)
   - [Depth and Width Plot](#Depth-and-Width-Plot)
3. [Examples](#Examples)
4. [Other Stuff](#Built-With)

### Installing

All of the functions that are identified below can be installed and imported given the code below:

```
!pip install "git+https://github.com/ambro034/Policy_Depth_and_Width.git"
import policy_DW as dw
```

## Functions

###Construct Base Datasets

#### construct_dataset
This is a function that takes a variably framed dataframe and conforms it to the structure useful to the following functions.

    construct_dataset(data,id,new_year,new_year_num,old_year,old_year_num)

Where:
  - *data* is the name of the dataframe
  - *id* is the column position for Statement IDs in the dataframe. If the data set does not have an ID column, `False` can be supplied.
  - *new_year* is the column position for Statement #1 in the dataframe
  - *new_year_num* is the year identifier that will be used for Statement #1 in the dataframe
  - *old_year* is the column position for Statement #2 in the dataframe
  - *old_year_num* is the year identifier that will be used for Statement #2 in the dataframe


### Color-coded Reuse Evaluation


### Construct Reuse Dataset

#### reuse_dataset_to_dataset
This is a function returns pairs of statements from a dataframe, to a new dataframe representing the new statement, the added text, the reused test, the terminated text, and the old statement. For the added text, the reused test, the terminated text -- text is reported sequentially, so '[...]' are inserted where text is not sequentually relevent.

    reuse_color_coded_dataset(data,id,new_year,old_year,l)

Where:
  - *data* is the name of the dataframe
  - *id* is the column position for Statement IDs in the dataframe
  - *new_year* is the column position for Statement #1 in the dataframe
  - *old_year* is the column position for Statement #2 in the dataframe
  - *l* is the minimum n-gram length the function is observing (i.e., *l* = 2, two-word chucks)

#### sheet_loop
This is a function returns a dataset of text reuse across two or more iterations of the same policies. This functions uses *reuse_dataset_to_dataset* to compare reused text between sequential policy versions, and uses *straight_merge* to merge these pair-wise comparisons into one large dataframe.

    sheet_loop(TAB,l)

Where:
  - *TAB* the file that is constructed in year-over-year amendments in columns and similar statements lined up within a row. For and example see *Colorado_Net_Metering_Overtime* and *Fake_data_2* included in the read me page.
  - *l* is the minimum n-gram length the function is observing (i.e., l = 2, two-word chucks)


### Policy Depth and Width

`add_term_measures(file_name, out)`

Where:
  - `file_name` is the name of the dataframe
  - `out` is the type of output such that (1) is a dataframe consisting 'Year', 'Gini Coeficient of Terminations', 'Evolution Depthof Terminations', 'Gini Coeficient of Additions', 'Evolution Depthof Additions'; and (2) is a dataframe consisting of all values used to calculate #1.

### Depth and Width Plot

`def plot_term_add(data,width_thresh, depth_thresh)`

Where:
  - `data` is the input data
  - `width_thresh` identifies the width threshold in the data.
  - `depth_thresh` identifies the width threshold in the data.
    
---

## Examples

```



```

[Link to Google Collaboratory](https://colab.research.google.com/drive/1zz002Z0REg3mKiaYo5psdy8yvWrRLh2A?usp=sharing](https://colab.research.google.com/drive/1lH-aBrbnMOuaOC8xuKMb4bBAu1h7wrLB?usp=sharing)
    
---
    
## Built With

  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used
    for the Code of Conduct
  - [Creative Commons](https://creativecommons.org/) - Used to choose
    the license

## Authors

  - **Graham Ambrose** - 
    [ambro034](https://github.com/ambro034/)


## License

This project is licensed under the [CC0 1.0 Universal](LICENSE.md)
Creative Commons License - see the [LICENSE.md](LICENSE.md) file for
details

## Acknowledgments

  - People
  
