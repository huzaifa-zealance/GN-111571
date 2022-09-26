'''SYSTEM PACKAGES'''
import os, sys
import numpy as np
from pandas import DataFrame as DF
from pandas import read_csv as READCSV
from glob import glob
from pprint import pprint as pp


#########################################################################
def is_sheet_usable(sheet) :
    '''
    Function to evaluate and return 
    if the sheet can be used or not
    '''
    
    #Checking if type is ndarray - else raising value error
    if type(sheet) != np.ndarray :
        raise TypeError("Input type is not a numpy array!")

    #Fetching the shape of the ndarray
    sheet_nxm = sheet.shape
    #Checking if shape is nxn - else raising value error
    if sheet_nxm[0] != sheet_nxm[1] :
        raise ValueError("Array shape is not 100x100 (nxn)")
    
    #Checking if all the elements are 1's and 0's only
    check_vals = np.isin(sheet, [1,0])
    if not np.all(check_vals) :
        raise ValueError("Array contains values other than 1's and 0's")
    
    
    #Evaluating total elements in the ndarray
    sheet_size = sheet_nxm[0]*sheet_nxm[1]
    
    #If size <= 9, and total sum is <=4 then sheet is passed
    #Else if size > 9 and total defects <=8 then sheet is passed
    #Else sheet is rejected
    if sheet_size <= 9:
        total_defects = sheet.sum()
        if total_defects <= 4 :
            return True
        else :
            return False
    else :
        total_defects = sheet.sum()
        if total_defects <= 8 :
            return True
        else :
            return False
#########################################################################

#########################################################################
def combine_csv_files(directory, output_filename) :
    '''
    Function to combine multiple csv 
    in same format into a dataframe
    '''
    
    #Checking if directory path exists
    if not os.path.exists(directory) :
        raise FileNotFoundError(f"Unable to find directory - {directory}")
    
    # Listing all the csv files present in the given directory
    list_of_files = glob(os.path.join(directory, "*.csv"))
    #Declaring an empty dataframe
    combined_df = DF()
    
    # Iterating through all the .csv files
    for each_f in list_of_files :
        try :
            # Reading csv file using pandas dataframe module read_csv
            csv_df = READCSV(each_f)
            
            # Extracting all the column names and checking 
            # if 'key' is part of columns
            # else, skipping the csv file
            csv_col_names = csv_df.columns.to_list()
            if 'key' not in csv_col_names :
                continue
            
            # Setting up key named column as index 
            csv_df.set_index("key", inplace=True)
            
            # Combining csv data to the empty dataframe
            combined_df = combined_df.append(csv_df)
            
        except :
            continue
    
    # Sorting dataframe index columns in ascending order
    combined_df = combined_df.sort_index(ascending=True)
    
    # Sorting all the columns in alphabetical order
    combined_df_cols = list(combined_df.columns.values)
    combined_df_cols_sorted = sorted(combined_df_cols)
    combined_df = combined_df.reindex(combined_df_cols_sorted, axis=1)
    
    # Dropping columns if 50% of the rows are null
    perc_th = 0.5
    combined_df = combined_df.dropna(thresh=combined_df.shape[0]*perc_th, 
                                     how='all', axis=1)
    
    # Dumping the final data into dataframe
    combined_df.to_csv(output_filename)
    
    return 1
#########################################################################

#########################################################################
def make_html_files(directory) :
    '''
    Function to create simple HTML pages
    '''
    
    ## Looking for index.txt file in the directory
    index_fpath = os.path.join(directory, "index.txt")
    if not os.path.exists(index_fpath) :
        raise FileNotFoundError(f"Unable to find index.txt file in directory - {directory}")
    
    ## Reading file data and maintaining the sequence
    fr = open(index_fpath, "r")
    file_lines = [x.strip() for x in fr.readlines()]
    
    ## Mapping each csv file to corresponding html file path
    ## Also, maintaining the same sequence defined in index.txt
    csv_to_html_map = []
    for fx in file_lines :
        filename = os.path.splitext(fx)[0]
        html_path = f"{filename}.html"
        csv_to_html_map.append((fx, html_path, filename))
    file_len = len(csv_to_html_map)
    
    ##################################################
    ## For each csv to html file formation,
    ##    defining prev and next hyperlinks in the same sequence
    ##    forming the data html code using dataframe
    ##    plotting the data using dataframe
    ## Finally, writing all in the corresponding HTML file
    for fid, each_f_data in enumerate(csv_to_html_map) :
        prev_link = None
        next_link = None
        
        curr_fpath = os.path.join(directory, each_f_data[0])
        html_path = os.path.join(directory, each_f_data[1])
        plot_fname = os.path.join(directory, f"{each_f_data[2]}.png")
        
        if fid == 0 :
            next_link = csv_to_html_map[fid+1][1]
            next_fname = csv_to_html_map[fid+1][2] 
            para_html = f"""Next: <a href="{next_link}">{next_fname}</a>"""
        elif fid == (file_len-1) :
            prev_link = csv_to_html_map[fid-1][1]
            prev_fname = csv_to_html_map[fid-1][2] 
            para_html = f"""Previous: <a href="{prev_link}">{prev_fname}</a>"""
        else :
            next_link = csv_to_html_map[fid+1][1]
            next_fname = csv_to_html_map[fid+1][2] 
            prev_link = csv_to_html_map[fid-1][1]
            prev_fname = csv_to_html_map[fid-1][2] 
            para_html = f"""Previous: <a href="{prev_link}">{prev_fname}</a>\nNext: <a href="{next_link}">{next_fname}</a>"""
        
        
        curr_f_df = READCSV(curr_fpath)
        table_html_str = curr_f_df.to_html(index=False)
        
        plt = curr_f_df.plot.line(title=each_f_data[2])
        fig = plt.get_figure()
        fig.savefig(plot_fname)
         
        html_str = f"""
        <html>
            <body>
                <h1>{each_f_data[2]}</h1>
                <p>
                  {para_html}  
                </p>
                {table_html_str}
                <img src="{plot_fname}">
            </body>
        </html>
        """
        
        fw = open(html_path, "w")
        fw.write(html_str)
        fw.close()
    ##################################################
    
#########################################################################

    
#########################################################################
if __name__ == '__main__':
    
    #####################################
    ### TASK 1
    ### Quality Control
    print("Task 1: Quality control")
    example_sheet = np.array([[1,0,0], [1,0,1], [0,0,2]])
    if_passed = is_sheet_usable(example_sheet)
    print(f"Sheet is Passed? - {if_passed}")
    #####################################
    
    
    #####################################
    ## TASK 2
    ## Combining CSV's
    print("Task 1: Combining CSV's")
    c_directory = "csvdir"
    output_filename = "task2_out.csv"
    combine_csv_files(c_directory, output_filename)
    #####################################
    
    
    #####################################
    ## TASK 3
    ## Making HTML files
    print("Task 1: Making HTML files")
    h_directory = "htmlplots"
    make_html_files(h_directory)
    #####################################
