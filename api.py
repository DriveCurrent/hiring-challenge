import json
from datetime import datetime, timedelta

from flask import Flask, request
from flask_cors import CORS

from db import DataBase

DATE_FORMAT = '%Y-%m-%d'

app = Flask(__name__)
app.debug = True
cors = CORS(app)


metric_id_to_name_map = {
    'unique_visitors': 'Unique Visitors',
    'page_views': 'Page Views',
    'visits': 'Visitors',
}


def ensure_data_for_missing_dates(data, start_date, end_date):
    days_delta = (end_date - start_date).days
    data = dict(data)
    data = [
        data.get(start_date + timedelta(days=date), 0)
        for date in xrange(days_delta)
    ]

    return data


def transform_data_to_series(metric_id, data):
    transformed_data = {
        'name': metric_id_to_name_map[metric_id],
        # 'total': sum(data),
        'data': data
    }

    return transformed_data


@app.route('/')
def api():
    start_date = datetime.strptime(request.args.get('start_date'), DATE_FORMAT).date()
    end_date = datetime.strptime(request.args.get('end_date'), DATE_FORMAT).date()
    metrics = request.args.getlist('metrics')

    delta_days = (end_date - start_date).days
    db = DataBase()

    api_response = {
        'index': [
            int((start_date + timedelta(day)).strftime('%s'))
            for day in xrange(delta_days)
        ],
        'series': {

        }
    }

    for metric_id in metrics:
        data = db.get_data(metric_id, start_date, end_date)
        data = ensure_data_for_missing_dates(data, start_date, end_date)

        api_response['series'][metric_id] = transform_data_to_series(metric_id, data)

    return json.dumps(api_response, indent=4)


if __name__ == '__main__':
    app.run()
