import json
from datetime import datetime, timedelta

from flask import Flask, request
from flask_cors import CORS

from db import DataBase

DATE_FORMAT = '%Y-%m-%d'  # Format for parsing api date params
JSON_DATE_FORMAT = '%Y-%m-%dT00:00:00Z'  # Format for converting dates to JSON

app = Flask(__name__)
app.debug = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})


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
    # Get the difference between the start and end date in days
    days_delta = (end_date - start_date).days + 1

    # Convert the data values to dicts where the key is the date
    # and the value is the data for the date
    data = dict(data)

    # Iterate over the expected dates
    # use the value if present in the data dict
    # otherwise default to zero
    data = [
        data.get(start_date + timedelta(days=date), 0)
        for date in xrange(days_delta)
    ]

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
    transformed_data = {
        'name': metric_id_to_name_map[metric_id],
        'total': sum(data),
        'data': data
    }

    return transformed_data


@app.route('/')
def api():
    start_date = datetime.strptime(request.args.get('start_date'), DATE_FORMAT).date()
    end_date = datetime.strptime(request.args.get('end_date'), DATE_FORMAT).date()
    metrics = request.args.getlist('metrics')

    delta_days = (end_date - start_date).days + 1
    db = DataBase()

    response = {
        'index': [
            (start_date + timedelta(day)).strftime(JSON_DATE_FORMAT)
            for day in xrange(delta_days)
        ],
        'series': {}
    }

    for metric_id in metrics:
        data = db.get_data(metric_id, start_date, end_date)
        data = ensure_data_for_missing_dates(data, start_date, end_date)
        data = transform_data_to_series(metric_id, data)
        response['series'][metric_id] = data

    return json.dumps(response, indent=4)


# Start the api if calling directly
# $ python api.py
if __name__ == '__main__':
    app.run()
