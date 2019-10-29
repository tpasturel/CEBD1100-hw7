import os, argparse, csv
import matplotlib.pyplot as plt
import numpy as np

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file")
    parser.add_argument("-d", "--degree", 
                        help="Polynomial degree to use for linear regression (defaults to 1)")
    args = parser.parse_args()
    return args

def is_there_an_input_file():
    # While building this function, I ran through the two errors where either
    # I provided the wrong input file name or no input file name at all
    # and looked for a way to address both
    args = arg_parser()
    if args.input_file is not None:
        input_file = os.path.join(os.getcwd(),args.input_file)
        try:
            with open(input_file) as data:
                read_data = data.read()
                return input_file
        except FileNotFoundError:
            print("Failed to open" + str(input_file) + \
            ". \nPlease look for a potential typo in your file name and/or file path.")
            exit()
    else:
        print("Please provide an input file.")
        exit()

# Setting the input file calling the function I created above
input_file = is_there_an_input_file()

def convert_type(element):
    # Case 2: is an emptry str, should be ignored
    if element == "": # len(element) == 0
        return None
    # Case 4: is a # with no ., should be int
    try:
        return int(element)
    except ValueError:
        # Case 3: has a . but is a #, should be float
        try:
            return float(element)
        except ValueError:
            # Case 1: is a string, should remain a string
            return element


# My weird way of dealing with either commas, single spaces or double spaces separators
def format_row(row):
    if "," in row:
        row = row
    else:
        # Shrinking multiples spaces separators into a single one and replacing them 
        # by a comma in each row
        row = " ".join(row.split())
        row = row.replace(" ", ",")
    return row

def populate_outer_list_orig():
    data=open(input_file, 'r')
    my_read_data = data.read()
    my_read_data1 = my_read_data.split('\n')    
    outer_list = []
    for row in my_read_data1:
        row = format_row(row)
        row_list = []
        for element in row.split(","):    
            new_element = convert_type(element)
            if new_element is not None:
                row_list += [new_element]
        if len(row_list) > 0:
            outer_list += [row_list]
    return outer_list

def populate_outer_list_csv():
    with open(input_file, 'r') as data:
        # Trying to read with comma separators, if csv.reader fails using commas, 
        # getting rid of the error and using default "one or more spaces" delimiter
        try:
            inputcsv = csv.reader(data, delimiter=',')
        except csv.Error:
            pass
        else:
            inputcsv = csv.reader(data)
            outer_list = []
            for row in inputcsv:
                row_list = []
                for (index,element) in enumerate(row):
                    new_element = convert_type(element)
                    if new_element is not None:
                        row_list += [new_element]
                if len(row_list) > 0:
                    outer_list += [row_list]
            return outer_list

def populate_dict():
    dd = {}
    outer_list = populate_outer_list_orig()
    for location, column_headings in enumerate(outer_list[0]):
        # Setting the dictionary's keys based on outer_list's indexes
        dd[location] = []
        for row in outer_list[:]:
            dd[location] += [row[location]]
    return dd


def define_polynomial_degree():
    parser = arg_parser()
    value = parser.degree
    if value is None:
        degree = 1
    else:   
        degree = value
    return degree

# This function does not yet plot the data in a consistent way because I am not really sure 
# on how to plot together the values from each column of each list in outer_list_orig :(
def plot_data():
    dd = populate_dict()
    for column1 in dd.keys():
        xlist = []
        ylist = []
        for column2 in dd.keys():
            # Defining the lists of values to apply regression on and performing polynomial regression 
            x = np.array(dd[column1])
            y = np.array(dd[column2])
            degree = define_polynomial_degree()
            coef = np.polyfit(x, y, int(degree))
            trend = np.poly1d(coef)
            minx = np.min(x)
            maxx = np.max(x)
            miny = np.min(y)
            maxy = np.max(y)
            plt.xlim(minx, maxx)
            plt.ylim(miny, maxy)
            plt.plot(x, y, 'yo', x, trend(x))
            plt.show()
            #return(x, y)

# I kept this but it does not provide the expected results
# def multi_plot():
#     x = plot_data()[0]
#     y = plot_data()[1]
#     fig, ax = plt.subplots(nrows = 10, ncols = 14)
#     for row in ax:
#         for col in row:
#             degree = define_polynomial_degree()
#             coef = np.polyfit(x, y, int(degree))
#             trend = np.poly1d(coef)
#             minx = np.min(x)
#             maxx = np.max(x)
#             miny = np.min(y)
#             maxy = np.max(y)
#             plt.xlim(minx, maxx)
#             plt.ylim(miny, maxy)
#             col.plot(x, y, 'yo', x, trend(x))
#     plt.show()

def main():
    arg_parser()
    populate_outer_list_orig()
    populate_dict()
    populate_outer_list_csv()
    plot_data()

if __name__ == "__main__": 
    main()