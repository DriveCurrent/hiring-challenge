# Drive Current Project

##  Problem Description

Create an HTTP API endpoint that sends data in a specified format to the browser and display it graphically.

### Getting started
 1. Download and install python (virtualenv and virtualenvwrapper recommended)
 1. Download and install node
 1. In command line go to the project directory
 1. Install python requirements: `pip install -r requirements.txt`
 1. Install javascript requirements: `npm install && ./node_modules/.bin/bower install`
 1. Start the python server `python server.py`

### Running the tests
There are a few tests that test basic functionality of the API. The tests are not comprehensive and there are more cases to be considered. Please think about these additional scenarios when writing your code. It is not required but you can add more tests to the suite if you like.

**To run the tests:** `python -m tests`

### Specifications

The graph should update automatically with new data when the input controls are changed

The endpoint should accept the following parameters:

 * start_date `"YYYY-mm-dd"`
 * end_date `"YYYY-mm-dd"`
 * metrics `[metric_id, metric_id, ...]`

The API should accept the following metric_ids:

```
   metric_id          name
   ---------          -----
   unique_visitors => Unique Visitors
   page_views      => Page Views
   visits          => Visitors
 ```

The api should return JSON in this format
```javascript
 {
     "index": ['YYYY-mm-dd'],  # start_date, start_date + 1, ...,  end_date (inclusive)
     "series": {
         "<metric_id>": {
             "name": str,  # metric display name
             "total": float,  # metric total for all days
             "average": float,  # metric average for all days
             "data": [int]  # data points (int) for every day in the range
         },
     }
 }
```

Sample database response

```
>>> # db.get_data(metric_id, start_date, end_date)
>>> db.get_data('unique_visitors', '2015-01-01', '2015-01-15')
[
    [datetime.date(2015, 1, 1), 5],
    [datetime.date(2015, 1, 4), 13],
    [datetime.date(2015, 1, 7), 100],
    [datetime.date(2015, 1, 10), 23],
    [datetime.date(2015, 1, 15), 4],
]
```

### General Notes
* If you get stuck, Google is your friend. Feel free to reach out to us for a hint as well.
* We expect the project to take around four hours.
* Keep a rough estimate of your time so that we can adapt this project in the future.

### Technical Notes

* The graph should be a line graph using the API's index array for the x-axis and data array for the y-axis
  * The other data will not be consumed by the graph
* The index and the data arrays should be of the same length
* The data from the database may be sparse but is guaranteed to be ordered
* We use Python/Django and Javascript/Angular in or stack. However, feel free to use any language / framework combinations that you are comfortable with
* We love testing at Drive Current, feel free to write a few or many.. it is optional in the interest of time
* We've provided a helper function to generate data for the server response in Python
  * **Note:** If you want to use a language other than python make sure you use the sample database response to help with our grading of your submission

### Submission Guidelines
 1. Zip up working directory
 1. Submit the project to adam@drivecurrent.com
