'''SYSTEM PACKAGES'''
import os
import numpy as np
from pandas import DataFrame as DF
from pandas import read_csv as READCSV
from pandas import to_numeric as TO_NUMERIC
from pprint import pprint as pp


#########################################################################
def call_input_str(menu_str):
    '''
    Common function to accept user input option
    '''
    
    # Accept user input and convert to int and return
    try :
        value = int(input(menu_str))
    except :
        value = 0
    return value 
#########################################################################

#########################################################################
def iterative_input_on_error(menu_str, min_op, max_op):
    '''
    Common function to iteratively accept input option until correct
    '''
    
    # Accept user input and convert to int and return
    value = call_input_str(menu_str)
    
    ## Error handling if the input option is not from the given list
    while (value < min_op or value > max_op) :
        print("Invalid selection!")
        # Re-confirm user input until correct
        value = call_input_str(menu_str)
        
        if value >= min_op and value <= max_op :
            break
    return value    
#########################################################################

#########################################################################
def iterative_col_input_check(data_df, msg):
    '''
    Common function to iteratively display column names
    and ask user input and validate until correct
    '''
    
    print(msg)
    col_input = None
    ## Confirm user input for column name until correct option provided
    ## Will break the loop if no input provided
    while (col_input not in data_df.columns) :
        ## Display names of the columns
        for each_c in data_df.columns :
            print(f"\t{each_c}")
        col_input = input(">>> ")
        col_input = col_input.strip()
        
        if col_input == "" :
            break
        if col_input not in data_df.columns :
            print("Invalid Selection!")
    
    return col_input
#########################################################################


#########################################################################
def op1_menu_items() :
    '''
    Function to drive the Option - 1 submenu items
    '''
    
    ## Display subitems of Option 1 menu
    op1 = "1 – Load data from a file"
    op2 = "2 – Go back to the main menu"
    
    op1_menu_str = f"Please choose from the following options:\n\t{op1}\n\t{op2}\n>>> "
    op_ans = iterative_input_on_error(op1_menu_str, 1, 2)
    
    ## An empty dataframe to be returned 
    ## when the user input is incorrect
    ret_df = DF()
    
    ## Ask user for filename and return empty if errors
    if op_ans == 2 :
        return ret_df
    elif op_ans == 1 :
        op1_1_str = "Enter file name : "
        fname = input(op1_1_str)
        while (not fname) :
            fname = input(op1_1_str)
    else :
        print("Invalid selection!")
        return ret_df
       
    if not os.path.exists(op_ans) :
        print("Error - File not found")
        print("Returning to main menu")
        return ret_df
    
    ## Read the input file and check if all the values are numeric
    ## Else, return appropriate errors as specified
    try :
        data_df = READCSV(fname)
        if data_df.empty :
            print("Error - All values in the file are not numeric")
            print("Returning to main menu")
            return ret_df
        
        
        if not data_df.shape[1] == data_df.select_dtypes(include=np.number).shape[1] :
            print("Error - All values in the file are not numeric")
            print("Returning to main menu")
            return ret_df
        
        
        print("Data has been loaded successfully.")
        
        ##################################################
        ########## Setting column name as index as per user input
        msg = "Which column do you want to set as index? (leave blank for none)"
        col_input = iterative_col_input_check(data_df, msg)
        if col_input in data_df.columns :
            data_df = data_df.set_index(col_input)
            print(f"{col_input} set as index.")
        else :
            print(f"No column is set as index.")
        ##################################################   

        return data_df

    except :
        print("Error - Unable to load data")
        print("Returning to main menu")
        return ret_df
#########################################################################

#########################################################################
def op2_menu_items(data_df) :
    '''
    Function to drive the Option - 2 submenu items
    '''
    
    ## Printing the dataframe
    print(data_df)
    return data_df
#########################################################################

#########################################################################
def op3_x_iterative_loop(msg):
    '''
    Common function to iteratively accept user input 
    for option 3 sub menu until correct
    '''
    
    ## Iteratively ask user input until a valid integer is not provided
    ## Else, return the valid integer
    val = input(msg)
    while(not val) :
        print("Invalid Selection!")
        val = input(msg)
    
    try :
        val = int(val)
    except :
        print("Please enter a valid number.")
        val = op3_x_iterative_loop(msg)
        
    return val  
#########################################################################


#########################################################################
def op3_menu_items(data_df) :
    '''
    Function to drive the Option - 3 submenu items
    '''
    
    ## Displaying the suboptiopns of Option 3 for cleaning data
    print("\nCleaning ..")
    print(data_df)
    
    op1 = "1 – Drop rows with missing values"
    op2 = "2 – Fill missing values"
    op3 = "3 – Drop duplicate rows"
    op4 = "4 – Drop column"
    op5 = "5 – Rename column"
    op6 = "6 – Finish cleaning"
    
    op3_menu_str = f"\nCleaning data:\n\t{op1}\n\t{op2}\n\t{op3}\n\t{op4}\n\t{op5}\n\t{op6}\n>>> "
    op_ans = iterative_input_on_error(op3_menu_str, 1, 6)
    
    
    ## For each suboption provided by user,
    ## Follow the specified steps to clean the data accordingly
    
    ## Suboption1 - Drop rows as per the threshold for non null values
    ## Count null values and compare with threshold and drop
    if op_ans == 1 :
        msg = "Enter the threshold for dropping rows: "
        thrshold = op3_x_iterative_loop(msg)
        row_idx_to_drop = []
        null_res = data_df.isnull().sum(axis=1).to_dict()
        for k in null_res :
            if null_res[k] > thrshold :
                row_idx_to_drop.append(k)
        data_df = data_df.drop(index=row_idx_to_drop)
        print(data_df)
        
        data_df = op3_menu_items(data_df)
    
    ## Ask user input for replacing null values with 
    elif op_ans == 2 :
        msg = "Enter the replacement value: "
        fillna_val = op3_x_iterative_loop(msg)
        data_df = data_df.fillna(fillna_val)
        data_df = op3_menu_items(data_df)
    
    ## Drop all the duplicate rows if any  
    elif op_ans == 3 :
        duplicate_cnt = data_df.duplicated().sum()
        data_df = data_df.drop_duplicates()
        print(f"**{duplicate_cnt} rows dropped")
        
        data_df = op3_menu_items(data_df)
        
    ## Drop a specific columns
    elif op_ans == 4 :
        msg = "Which column do you want to drop? (leave blank for none)"
        col_input = iterative_col_input_check(data_df, msg)
        if col_input in data_df.columns :
            data_df = data_df.drop(col_input, axis=1)
            print(f"{col_input} is dropped.")
        else :
            print(f"No column dropped.")
        
        data_df = op3_menu_items(data_df)

    # Rename a specific columns by asking as user input (both col and new name)
    elif op_ans == 5 :
        msg = "Which column do you want to rename? (leave blank for none)"
        col_input = iterative_col_input_check(data_df, msg)
        if not col_input :
            print(f"No column selected to rename.")
            #data_df = op3_menu_items(data_df)
        
        elif col_input in data_df.columns :
            msg = "Enter the new column name to rename? (Don't leave as blank) : "
            new_name = input(msg)
            while (not new_name) :
                new_name = input(msg)
            data_df = data_df.rename(columns={col_input:new_name})
        
        data_df = op3_menu_items(data_df)
    
    ## Finish clearing, exiting the process back to main menu
    elif op_ans == 6 :
        print("Finished cleaning")
    
    return data_df
#########################################################################
   
#########################################################################
def op4_menu_items(data_df) :
    '''
    Function to drive the Option - 4 submenu items
    '''
    
    print("Analyzing data\n")
    
    ## For each column in data, calculate the required stats 
    ## then print the same in the given format
    for each_c in data_df.columns :
        print(f"{each_c}");print("-"*len(each_c))
        
        min_val = round(data_df[each_c].min(),2)
        max_val = round(data_df[each_c].max(),2)
        mean_val = round(data_df[each_c].mean(),2)
        median_val = round(data_df[each_c].median(),2)
        std_dev = round(data_df[each_c].std(),2)
        sem = round(data_df[each_c].sem(),2)
        
        row_data = data_df[each_c].shape[0]
        print(f"{'number of values (n)' : >20} : {row_data}")
        print(f"{'minimum' : >20} : {min_val}")
        print(f"{'maximun' : >20} : {max_val}")
        print(f"{'mean' : >20} : {mean_val}")
        print(f"{'median' : >20} : {median_val}")
        print(f"{'standard deviation' : >20} : {std_dev}")
        print(f"{'std. err. of mean' : >20} : {sem}")
        
        print("\n")
    
    ## Calculate correlation matrix for the data and print
    print("Correlation Matrix");print("-"*len("Correlation Matrix"))
    print(data_df.corr())
    
    return data_df   
#########################################################################
   

#########################################################################
def op5_menu_items(data_df):
    '''
    Function to drive the Option - 5 submenu items
    '''
    
    ## ASk user input for specific type of plot, iterate until correct option provided
    msg = "Please choose from the following kinds: line, bar, box : "
    plot_type = input(msg)
        
    while (not plot_type or plot_type.lower() not in ['line', 'bar', 'box']) :
        print("Invalid Selection!")
        plot_type = input(msg)
    plot_type = plot_type.lower()
    
    
    ## Ask if subplots to be included or not
    msg = "Do you want to use subplots? (y/n) : "
    subplot_t = input(msg)
    while (not subplot_t or subplot_t.lower() not in ['y', 'n']) :
        print("Invalid Selection!")
        subplot_t = input(msg)
    p_subplot = True if subplot_t.lower() == "y" else False

    ## Ask user input for title of plot
    msg = "Please enter the title for the plot (leave blank for no title) : "
    p_title = input(msg)
    
    ## Ask user input for x axis for plot
    msg = "Please enter the x-axis label (leave blank for no label) : "
    p_xaxis = input(msg)
    
    ## Ask user input for y axis for plot
    msg = "Please enter the y-axis label (leave blank for no label) : "
    p_yaxis = input(msg)
    
    ## Plotting as per the inputs using dataframe + matplotlib
    plt = data_df.plot(
                    kind=plot_type,
                    subplots = p_subplot,
                    title = p_title,
                    xlabel = p_xaxis,
                    ylabel = p_yaxis
                )
    
    ## Saving the plot in a specific file
    plot_fname = f"fig_{plot_type}.png"
    
    if p_subplot :
        fig = plt[0].get_figure()
        fig.tight_layout()
        fig.savefig(plot_fname)
    else :
        fig = plt.get_figure()
        fig.savefig(plot_fname)
    
    print(f"Plot is generated and saved as file - {plot_fname}")
    
    return data_df   
#########################################################################  

#########################################################################
def op6_menu_items(data_df) :
    '''
    Function to drive the Option - 6 submenu items
    '''
    
    ## Ask user input for file name to be saved as
    msg = "Enter the filename, including extension: "
    fname = input(msg)
    if not fname :
        print("Cancelling save operation.")
        return data_df
    
    data_df.to_csv(fname)
    print(f"Data saved to {fname}")
    
    return data_df
#########################################################################
    
    
#########################################################################
def main_menu_options(data_df):
    '''
    Function to drive the main menu options interactively
    '''
    
    ## Printing all the given options for user to choose
    op1 = "1 – Load data from a file"
    op2 = "2 – View data"
    op3 = "3 – Clean data"
    op4 = "4 – Analyse data"
    op5 = "5 – Visualise data"
    op6 = "6 – Save data to a file"
    op7 = "7 – Quit"
    main_menu_str = f"\n\nPlease choose from the following options:\n\t{op1}\n\t{op2}\n\t{op3}\n\t{op4}\n\t{op5}\n\t{op6}\n\t{op7}\n>>> "

    # Iterating until correct input option is provided by user
    value = iterative_input_on_error(main_menu_str, 1, 7)
    
    
    # Performing specific option (subitems)
    # Corresponding to the user input provided (between 1-7)
    if value == 1 :
        data_df = op1_menu_items()
        main_menu_options(data_df)
    
    elif value == 2 :
        if data_df.empty :
            print("No data to display.")
            main_menu_options(data_df)
        data_df = op2_menu_items(data_df)
        main_menu_options(data_df)
        
    elif value == 3 :
        if data_df.empty :
            print("No data to display.")
            main_menu_options(data_df)
        data_df = op3_menu_items(data_df)
        main_menu_options(data_df)
    
    elif value == 4 :
        if data_df.empty :
            print("No data to display.")
            main_menu_options(data_df)
        data_df = op4_menu_items(data_df)
        main_menu_options(data_df)
        
    elif value == 5 :
        if data_df.empty :
            print("No data to display.")
            main_menu_options(data_df)
        data_df = op5_menu_items(data_df)
        main_menu_options(data_df)
        
    elif value == 6 :
        if data_df.empty :
            print("No data to display.")
            main_menu_options(data_df)
        data_df = op6_menu_items(data_df)
        main_menu_options(data_df)
    elif value == 7 :
        print("Goodbye!")
    else :
        print("Invalid selection!")
        main_menu_options()
    
    return 1
#########################################################################

    

#########################################################################
def main():
    '''
    main function which drive the complete engine
    '''
    
    ## Printing introductory message
    name = "<>" #----> Enter your name here
    print(f"Welcome to The DataFrame Statistician!\nProgrammed by {name}\n")
    

    ## Function to handle the main menu options
    data_df = DF()
    main_menu_options(data_df)
    
#########################################################################

    
#########################################################################
if __name__ == '__main__':
    main()
#########################################################################