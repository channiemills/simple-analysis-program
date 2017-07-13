# Simple Analysis Program
This command line program was built on request to perform basic analysis on a provided sql lite database. The program allows the user to perform the square root, cube root, and reciprocal operations on one of the columns in the database and returns the result and standard deviation. The user can determine whether they want the results to be exported to csv.

The program was built using Python 2.7 and the sqlite3, numpy, numpy.ma, csv, and os libraries.
I chose Python based on having experience with it in the past and feeling comfortable writing the functions required for the program.

My initial design idea was to approach the task as I would manually: bring in the data, clean it if necessary, analyze, then export.


### Ingesting:

I chose numpy arrays for the ability to leverage numpy methods for the transformations.


### Cleaning:

I excluded records that might be negative upon ingestion using the numpy.ma.masked_less method. This allows the array to be transformed without negative values affecting the results. I considered just filtering out negatives from each column but the array of the column would then lose its ordering and therefore their association to their index values.

For additionally cleaning purposes, I considered handling data where there were unexpected strings. In reviewing the database table, the columns annual_income and transaction_amount were integer so noninteger values could not be ingested. If the column type were to change for those columns the program would need refactoring.

### Analysis:

I built two functions to start, one to get the column and another to perform the transformation. I spent much time testing here to insure the functions returned correct results if valid or invalid inputs were provided.

User inputs were forced to be lower case and stripped of any spaces that might be entered to add flexibility.

Transformations performed using numpy's built in methods.


### Bringing it together:

To create the interactivity for the program, I moved the function to get the columns into a new function that would run at the execution of the program and receive the inputs from the user. This required a bit of refactoring of error handling in the original two functions. I also created a rerun function to call from within the transformation function after each transform (successful or unsuccessful).

Lastly I created a function, to be called from within rerun for the user to export results if they desire.

I found some difficulty with exporting to the CSV that might have proven easier using another library, such as pandas.

Currently the program exports the entire db as it was originally into one csv file, then generates another csv file with the original db in one column and the transformed column (without the header) in another column. An MVP next step is to include the header for the transformed column so that data is clearly labeled and the last row of data is not lost. I started this process but felt I was running out of time (can be found commented out of lines 61 and 62). Another library likely has a more elegant solution for the export but I was concerned about the time it would take to restructure all of the other places in the program data structures were used.


