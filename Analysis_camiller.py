__author__ = 'cmiller'

import sqlite3
import numpy
import numpy.ma
import csv
import os


column = []
t_column = []

# Open the database file and fetch data


db = sqlite3.connect("./transaction_data.db")
c1 = db.cursor()
c1.execute("SELECT annual_income FROM bt_data")
ai = c1.fetchall()
annual_income_before = numpy.array(ai)
annual_income = numpy.ma.masked_less(annual_income_before,0)



c2 = db.cursor()
c2.execute("SELECT transaction_amount FROM bt_data")
ta = c2.fetchall()
transaction_amount_before = numpy.array(ta)
transaction_amount = numpy.ma.masked_less(transaction_amount_before,0)


# Function to run program


def run_program():
    # ask user what they want to do
    data = raw_input("What field would you like to transform?").lower().strip()
    t_type = raw_input("What transformation would you like to apply?").lower().strip()
    global column
    if data == 'annual_income':
        column = annual_income
        transform(data, t_type)
    elif data == 'transaction_amount':
        column = transaction_amount
        transform(data, t_type)
    else:
        print "Invalid column. Please enter either annual_income or transaction_amount"
        run_program()


# Functions to transform specified column

def transform(data, t_type):
    init_std = numpy.std(column)
    global t_column
    if t_type == 'square_root':
        print "%s, standard deviation: $%d" % (data, init_std)
        sqrt_column = numpy.sqrt(column)
        fin_std = numpy.std(sqrt_column)
        print "%s of %s, standard deviation: $%d" % (t_type, data, fin_std)
        #sqrt_list = sqrt_column.tolist()
        #t_column= sqrt_list.insert(0,'%s of %s' % (t_type,data))
        t_column = sqrt_column
        rerun()


    elif t_type == 'cube_root':
        print "%s, standard deviation: $%d" % (data, init_std)
        cbrt_column = numpy.power(column,(1.0/3))
        fin_std = numpy.std(cbrt_column)
        print "%s of %s, standard deviation: $%d" % (t_type, data, fin_std)
        t_column = cbrt_column
        rerun()


    elif t_type == 'reciprocal':
        print "%s, standard deviation: $%d" % (data, init_std)
        #recp_column = numpy.reciprocal(column)
        recp_column = 1.0/column
        fin_std = numpy.std(recp_column)
        print "%s of %s, standard deviation: $%d" % (t_type, data, fin_std)
        t_column = recp_column
        rerun()
        #return recp_column

    else:
        print "Invalid transformation. Please enter square_root, cube_root, or reciprocal."
        run_program()


def rerun():
    user_request = raw_input(
        "Would you like to try a different transformation (d), write your results to a file (w), or quit (q)? (d/w/q)").lower().strip()
    if user_request == 'd':
        run_program()

    elif user_request == 'w':
        print "analysisexport.csv and originaldb.csv lives at %s" % os.getcwd()
        writefile()

    elif user_request == 'q':
        return

    else:
        print "Please select (d/w/q)."
        rerun()


def writefile():
    global db
    c3 = db.cursor()
    c3.execute("SELECT * FROM bt_data")
    table = c3.fetchall()

    with open("originaldb.csv", "wb") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in c3.description]) # write headers
        csv_writer.writerows(table)

    new_data = []
    with open("test.csv", "rb") as file:
        reader = csv.reader(file)
        for row in reader:
            new_row = row
            new_data.append(new_row)
        zipped = zip(new_data, t_column)

    with open("analysisexport.csv","wb") as to_file:
        writer = csv.writer(to_file)
        writer.writerows(zipped)



run_program()