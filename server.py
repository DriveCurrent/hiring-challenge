import json
from datetime import datetime, timedelta, date

from flask import Flask, request, jsonify
from db import DataBase

DATE_FORMAT = '%Y-%m-%d'  # Format for parsing api date params
JSON_DATE_FORMAT = '%Y-%m-%dT00:00:00Z'  # Format for converting dates to JSON

app = Flask(__name__)
app.debug = True


# Map of metric_id's to friendly names
metric_id_to_name_map = {
    'unique_visitors': 'Unique Visitors',
    'page_views': 'Page Views',
    'visits': 'Visitors',
}


def ensure_data_for_missing_dates(data, start_date, end_date):
    """
    Checks the data for missing dates and fills gaps with zeros

    Params
    ------
    data: [[datetime.date, int], ...]
    start_date: datetime.date
    end_date: datetime.date

    Returns
    -------
    [int, ...]
    """
    def gap_filler(start, end, target):
        """Returns list of dates with 0 values"""
        diff = (start - end).days
        dates = [[start - timedelta(days=x), 0] for x in range(diff+1)]

        """Dict comprehension to prevent duplicates"""
        target_dict = {date: value for date, value in target}

        for i in dates:
            if i[0] not in target_dict:
                target.append(i)
            else:
                pass

    """Check front and rear of list to see if gaps exist"""
    try:
        first_date = data[0][0]
        if start_date < first_date:
            gap_filler(first_date, start_date, data)
        else:
            pass
    except IndexError:
        pass

    try:
        last_date = data[-1][0]
        if last_date < end_date:
            gap_filler(end_date, last_date, data)
        else:
            pass

    except IndexError:
        pass

    """Extract values and return sorted list"""
    data = [x[1] for x in sorted(data)]
    return data



def transform_data_to_series(metric_id, data):
    """
    Prepares the metric and data to be sent as the API's response

    Params
    ------
    metric_id: string
        metric_id used to query the data
    data: [int, ...]

    Returns
    -------
    {
        'name': string  # Friendly metric name
        'total': int  # Sum of the data
        'data': [int, ...] # The data that was passed in

    }
    """
    return {
        'name': metric_id_to_name_map[metric_id],
        'total': sum(data),
        'data': data
    }


def get_index(start_date, end_date):
    """
    Get the index for the requested range
    This is an array of dates from the start_date
    to the end_date inclusive

    This will be used as the x-axis labels for the chart

    Params
    ------
    start_date: datetime.date
    end_date: datetime.date

    Returns
    -------
    [datetime.date, ...]
    """
    diff = (start_date - end_date).days
    return sorted([start_date + timedelta(days=x) for x in range(abs(diff)+1)])


@app.route('/')
def root():
    """
    The root '/' route
    Serves the index.html file

    Static files are served automatically by flask
    """
    return app.send_static_file('index.html')


@app.route('/api', methods=['GET'])
def api():
    """
    Api endpoint at '/api'

    Fetches the data for the requested metrics and date range

    Query Params
    ------------
    start_date: string  # 'YYYY-mm-dd'
    end_date: string  #  'YYYY-mm-dd'
    metrics:  [metric_id, ...]
    """

    """If nothing is in the URL, return empty JSON array"""
    if request.args == {}:
        today = date.today()
        response = {}
        response['index'] = [today.strftime(JSON_DATE_FORMAT),
                             (today + timedelta(7)).strftime(JSON_DATE_FORMAT)]
        response['series'] = []
        return json.dumps(response)

    # We may want to do some sanity checking on the query params
    # What should be done in the event the params do not make sense?

    """If start and end dates are missing, default to today and a week from now, respectively"""
    if request.args.get('start_date') is not None:
        start_date = datetime.strptime(request.args.get('start_date'), DATE_FORMAT).date()
    else:
        start_date = datetime.strptime(str(date.today()), DATE_FORMAT).date()
    if request.args.get('end_date') is not None:
        end_date = datetime.strptime(request.args.get('end_date'), DATE_FORMAT).date()
    else:
        end_date = datetime.strptime(str(date.today() + timedelta(7)), DATE_FORMAT).date()

    metrics = request.args.getlist('metrics')

    for i in metrics:
        if i == '':
            metrics.pop(i)

    db = DataBase()

    response = {
        'index': get_index(start_date, end_date),
        'series': {}
    }

    for metric_id in metrics:
        data = db.get_data(metric_id, start_date, end_date)
        data = ensure_data_for_missing_dates(data, start_date, end_date)
        data = transform_data_to_series(metric_id, data)
        response['series'][metric_id] = data

    """Convert datetimes to ISO strings so they can be JSONified"""
    response['index'] = [x.strftime(DATE_FORMAT) for x in response['index']]

    """Switched to jsonify to make the output cleaner"""
    return jsonify(response)


# Start the api if calling directly
# $ python server.py
if __name__ == '__main__':
    app.run()
