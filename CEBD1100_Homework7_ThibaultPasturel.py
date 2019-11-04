import argparse
import os.path as op
import csv
import matplotlib.pyplot as plt
import numpy as np
import statistics
import re

def convert_type(data_value):
    try:
        return int(data_value)
    except ValueError:
        try:
            return float(data_value)
        except ValueError:
            return data_value

# I modified this function a bit and I am calling it in main because it was failing
# before with passing it the -H option (maybe I deleted something at some point, by mistake)
def lines_to_dict(lines, header=False, debug=False):
    column_titles = lines[0]
    if header:
        print("Here are the input file's column headers: " + str(column_titles))
        exit()
    
    if debug:
        print("Here are the first three lines of the input file: \n" + str(lines[0:1]) 
        + "\n" + str(lines[1:2]) + "\n" + str(lines[2:3]))
        exit()
 
    else:
        #column_titles = list(range(1, len(lines[0])+1))
        column_titles = lines[0]
        lines = lines[1:]

    data_dict = {}
    for idx, column in enumerate(column_titles):
        data_dict[column] = []
        for row in lines:
            data_dict[column] += [row[idx]]
    return data_dict

def parse_file(data_file, delimiter, debug=False):
    # Verify the file exists
    assert(op.isfile(data_file))

    # open it as a csv (not checking delimiters, so you can do better)
    with open(data_file, 'r') as fhandle:
        csv_reader = csv.reader(fhandle, delimiter=delimiter)

        # Add each line in the file to a list
        lines = []
        if debug:
            count = 0
        for line in csv_reader:
            if debug:
                if count > 2:
                    break
                count += 1
            newline = []
            for value in line:
                newline += [convert_type(value)]

            if len(newline) > 0:
                lines += [newline]

    # Return all the contents of our file
    return lines

def generate_points(coefs, min_val, max_val):
    xs = np.arange(min_val, max_val, (max_val-min_val)/100)
    return xs, np.polyval(coefs, xs)

def plot_data(dd, debug=False, plot=False, polys=[1,2,3,4]):
    # dd stands for data_dictionary, debug doesn't plot
    if debug:
        number_combinations = 0

    # Preventing the function from plotting the data if the -p switch if provided 
    if not plot:
        return 
    ncols = len(dd.keys())
    if not debug:
        fig = plt.Figure(figsize=(30, 30))   
    for i1, column1 in enumerate(dd.keys()):
        for i2, column2 in enumerate(dd.keys()):
            if debug:
                number_combinations += 1
                print(column1, column2)
                # import pdb
                # pdb.set_trace()
            else:
                # If my grid is :
                # 1  2  3  4  5
                # 6  7  8  9  10
                # 11 12 13 14 15
                #  ... then, I want to index it at i1*ncols + i2   (+1)
                loc = i1*ncols + i2 + 1
                plt.subplot(ncols, ncols, loc)
                x = dd[column1]
                y = dd[column2]
                
                if str(x) and str(y):
                    pass
                else:
                    plt.scatter(x, y)
                    # plt.xlabel(column1)
                    # plt.ylabel(column2)
                    # plt.title("{0} x {1}".format(column1, column2))

                # for poly_order in polys:
                #     coefs = np.polyfit(x, y, poly_order)  # we also want to do this for 2, 3
                #     xs, new_line = generate_points(coefs, min(x), max(x))
                #     plt.plot(xs, new_line)
    if not debug:
        # Note: I have spent no effort making it pretty, and recommend that you do :)
        # plt.legend()
        # plt.tight_layout()
        # plt.show()
        plt.savefig("./my_pairs_plot.png")

    if debug:
        print(len(dd.keys()), number_combinations)
    return 0


def check_column(dd, data_file=False, column=False):
    # Checking that a column name was provided
    if column:
        # Checking that the column name actually exists in the input file
        if column not in dd.keys():
            print("Please provide a column name that exists in " + str(data_file) + " file." )
            print("The script's -H option will allow you to see the input file's column headers.")
            exit()
        
        # Calculating the several requested values    
        values = dd[column]
        mean = statistics.mean(values)
        minimum = min(values)
        maximum = max(values)
        stdev = statistics.stdev(values)
        print("tc column's mean value is: " + str(mean) + ".")
        print("tc column's min value is: " + str(round(minimum, 2)) + ".")
        print("tc column's mean value is: " + str(round(maximum, 2)) + ".")         
        print("tc column's values standard deviation is: " + str((round(stdev, 2))) + ".")
        
        # Determining whether the column's data is categorical or continuous
        uniq_values = set(values)
        print(str(column) + " column contains " + str(len(values)) + " rows including " 
        + str(len(uniq_values)) + " unique values.")
        ratio = round(((int(len((uniq_values))) / int(len(values))) * 100), 2)
        if ratio < 20:
            print("The number of unique rows in " + str(column) + " represents " + str(ratio) 
            + "% of the total number of rows in the column. This data is therefore most likely categorical.")
        else:
            print("The number of unique rows in " + str(column) + " represents " + str(ratio) 
            + "% of the total number of rows in the column. This data is therefore most likely continuous.")
    else:
        exit()         

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", type=str,
                        help="Input CSV data file for plotting")
    parser.add_argument("delimiter", type=str,
                        help="the delimiter used in your file")
    parser.add_argument('-x', '--debug', action="store_true",
                        help="only prints start of file")
    parser.add_argument('-H', '--header', action="store_true",
                        help="determines if a header is present")
    parser.add_argument('-p', '--plot'  , action="store_true",
                        help="determines if we plot the data or not")
    parser.add_argument('-s', '--summary', action='store', dest='column', type=str,
                        help="perform a data sanity check for the provided column")
    args = parser.parse_args()
    my_data = parse_file(args.data_file, args.delimiter, debug=args.debug)
    data_dictionary = lines_to_dict(my_data, header=args.header, debug=args.debug)
    #print(data_dictionary)
    lines_to_dict(my_data, header=args.header, debug=args.debug)
    plot_data(data_dictionary, debug=args.debug, plot=args.plot)
    data_dictionary2 = lines_to_dict(my_data)
    check_column(data_dictionary2, data_file=args.data_file, column=args.column)

if __name__ == "__main__":
    main()