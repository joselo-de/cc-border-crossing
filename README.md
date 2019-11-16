## Coding challenge - Bureau of Transportation Statistics
### Jose L Garcia
### November, 2019

* This repo uses python3 to calculate the total number of times a vehicle, equipment, passenger or pedestrian crosses the US border each month. Both borders included Canada and Mexico. 

* It also calculates each month's running average of crossings by the respecive type of crossing and border.

* Dataset can be found here: [Border Crossing Entry Data](https://data.transportation.gov/Research-and-Statistics/Border-Crossing-Entry-Data/keg4-3bc2)

* Modules used: sys, math, datetime, operator

Solution overview: At first, we tried to use a single loop that would iterate on different levels using nested dictionaries. That approach got really complicated because it's easy to get lost in the different levels of nesting loops.

The solution provided uses classes as to emulate a database. It enabled access to specific values on every line of the csv file. Combining that approach with other dictionaries we were able to calculate averages and sums in an efficient way.

At the end, the use of itemgetter() provided and easy way to sort our results according to the requirements.
