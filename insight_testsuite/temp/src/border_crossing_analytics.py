#!/usr/bin/python3

# Author: Jose Garcia
# Date: 11/09/2019

""" Coding challenge using Border Crossing Entry Data.
    
    This program takes the csv files from /input and performs basic statistics about
    the contents. It uses a class to emulate records on a database. Total crossings 
    per date and crossing type are simplyfied with this approach.
"""

import sys
import math
from datetime import datetime
from operator import itemgetter

class db_registry:
  """Class to create a database abstraction to manipulate date from csv file"""
  def __init__(self, border, date, measure, value):
    self.border = border
    self.date = date
    self.measure = measure
    self.value = value


def csv_to_dblist(filename):
  """Read csv file, return its content as a list of classes. 
     Returns:
     crossing_db. database abstraction containing integers, strings or datetype
     cross_types. list of all available cross types in csv (Passengers, Trains, etc)
     years_in_file. list of all years encountered in csv
  """
  with open(filename, 'r') as f:
    # skip first line (header)
    first_line = f.readline()

    # put data from csv into a temporary list. use "," to separate elements
    f_list = [[int(x) if x.rstrip().isdigit() else x for x in line.split(',')] for line in f.readlines()]

    # crossing_db list. each element will store a class abstraction
    crossing_db = []
    cross_types = []
    years_in_file = []

    for line in f_list:
      port_name, state, code, border, date, measure, value, *extras = line
      as_datetype = datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
      
      crossing_db.append(db_registry(border, as_datetype, measure, value))

      # cross_types list. insert only unique "measure" values
      if measure not in cross_types:
        cross_types.append(measure)
      
      # years_in_file list. insert only unique years contained in csv
      if as_datetype.year not in years_in_file:
        years_in_file.append(as_datetype.year)

  return crossing_db, cross_types, sorted(years_in_file)


def write_header(filename):
  """Create the output file. Add header"""
  f = open(filename, 'w')
  f.write('Border,Date,Measure,Value,Average\n')
  f.close()
  return

  
def write_line(filename, line):
  """Open output file in Append mode to write one line at a time"""
  f = open(filename, 'a')

  # format and join text with a comma
  format_line = ['{}'.format(i) for i in line]
  write_line = ','.join(format_line) + '\n'
  f.write(write_line)
  f.close()
  return


def round_up_trunc(number, decimals=0):
  """Rounds up decimals of a float number, returns only integer part of number"""
  multiplier = 10 ** decimals
  return math.trunc(math.ceil(number * multiplier) / multiplier)


# main function
def main():
  if len(sys.argv) != 3:
    print('\n##########################################################')
    print('Make sure you execute the program using the following form:')
    print('python3 border_crossing.py input_file.csv report_file.csv\n')
    sys.exit(1)

  # convert input file into list
  crossing_db, cross_types, years_in_file = csv_to_dblist(sys.argv[1])
  results = []
  
  for year in years_in_file:

    # create dictionaries to store crossing type and sums per month
    # also clean values each iteration of year
    canada_crossings = {}
    mexico_crossings = {}
    accumulate_canada = {}
    accumulate_mexico = {}
    for cross_t in cross_types:
      if cross_t not in canada_crossings:
        canada_crossings[cross_t] = 0
      if cross_t not in mexico_crossings:
        mexico_crossings[cross_t] = 0
      if cross_t not in accumulate_canada:
        accumulate_canada[cross_t] = []
      if cross_t not in accumulate_mexico:
        accumulate_mexico[cross_t] = []

    for month in range(1, 13):

      # clean values each month
      for cross_t in cross_types:
        canada_crossings[cross_t] = 0
        mexico_crossings[cross_t] = 0
        running_avg = 0

      # iterate over db. all crossing types for Canada
      for _, db_row in enumerate(crossing_db):
        if (db_row.border == 'US-Canada Border') and (db_row.date.year == year) and (db_row.date.month == month):

          # take the date to use it outside this loop
          date_to_report = db_row.date

          for cross_t in cross_types:
            if db_row.measure == cross_t:
              tmp_sum = canada_crossings[cross_t]
              tmp_sum += db_row.value
              canada_crossings[cross_t] = tmp_sum

        # iterate over all crossing types for Mexico
        if (db_row.border == 'US-Mexico Border') and (db_row.date.year == year) and (db_row.date.month == month):

          date_to_report = db_row.date

          for cross_t in cross_types:
            if db_row.measure == cross_t:
              tmp_sum = mexico_crossings[cross_t]
              tmp_sum += db_row.value
              mexico_crossings[cross_t] = tmp_sum

      # we've just accumulated all crossings per type and month
      # calculate averages and put results into a list
      for item, value in canada_crossings.items():
        if value > 0:

          # accumulate_canada and accumulate_mexico store all the values we observe
          # for each crossing during the year. 12 values maximum (one per month)
          # we use avg_list just to simplify the code.
          accumulate_canada[item].append(value)
          avg_list = accumulate_canada[item]
          
          # running average is zero at the beginning of the year, or until avg_list
          # grows to 2 values. in that case running average is the first value on 
          # avg_list
          if len(avg_list) == 2:
            running_avg = avg_list[0]

          # after avg_list grows bigger than 2, calculate running average as follows
          # sum all elements on avg_list except the last value (which is our current
          # value to save on results), and divide by number of elements on avg_list-1
          if len(avg_list) > 2:
            running_avg = round_up_trunc((sum(avg_list) - avg_list[-1]) / (len(avg_list) - 1))
          results.append(['US-Canada Border', date_to_report, item, value, running_avg])

      # exact same process for mexico crossings
      for item, value in mexico_crossings.items():
        if value > 0:
          accumulate_mexico[item].append(value)
          avg_list = accumulate_mexico[item]
          if len(avg_list) == 2:
            running_avg = avg_list[0]
          if len(avg_list) > 2:
            running_avg = round_up_trunc((sum(avg_list) - avg_list[-1]) / (len(avg_list) - 1))
          results.append(['US-Mexico Border', date_to_report, item, value, running_avg])

  
  # sort results according to requirements using itemgetter()
  # 1. Date
  # 2. Value (or number of crossings)
  # 3. Measure (type of crossing)
  # 4. Border
  sorted_results = sorted(results, key=itemgetter(1, 3, 2, 0), reverse=True)

  # write results to report file
  write_header(sys.argv[2])

  for column in sorted_results:
    date_as_str = datetime.strftime(column[1], '%m/%d/%Y %I:%M:%S %p')
    line = [column[0], date_as_str, column[2], column[3], column[4]]
    write_line(sys.argv[2], line)


if __name__ == '__main__':
  main()

