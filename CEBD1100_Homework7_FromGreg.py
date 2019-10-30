import argparse
import os.path as op
import csv
import matplotlib.pyplot as plt
import numpy as np

def convert_type(data_value):
    try:
        return int(data_value)
    except ValueError:
        try:
            return float(data_value)
        except ValueError:
            return data_value

def lines_to_dict(lines, header=False):
    if header:
        column_titles = lines[0]
        lines = lines[1:]
    else:
        column_titles = list(range(1, len(lines[0])+1))
    
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

def plot_data(dd, debug=False, polys=[1,2,3,4]):
    # dd stands for data_dictionary, debug doesn't plot
    if debug:
        number_combinations = 0

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
                
                plt.scatter(x, y)
                plt.xlabel(column1)
                plt.ylabel(column2)
                plt.title("{0} x {1}".format(column1, column2))

                for poly_order in polys:
                    coefs = np.polyfit(x, y, poly_order)  # we also want to do this for 2, 3
                    xs, new_line = generate_points(coefs, min(x), max(x))
                    plt.plot(xs, new_line)
    if not debug:
        # Note: I have spent no effort making it pretty, and recommend that you do :)
        plt.legend()
        # plt.tight_layout()
        # plt.show()
        # plt.savefig("./my_pairs_plot.png")

    if debug:
        print(len(dd.keys()), number_combinations)
    return 0


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
    
    args = parser.parse_args()
    my_data = parse_file(args.data_file, args.delimiter, debug=args.debug)
    data_dictionary = lines_to_dict(my_data, header=args.header)
    print(data_dictionary)
    plot_data(data_dictionary, debug=args.debug)

if __name__ == "__main__":
    main()