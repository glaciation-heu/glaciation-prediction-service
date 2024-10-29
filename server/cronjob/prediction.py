import argparse
import requests
import json
import numpy as np

from model.autoarima import AutoARIMA
from datetime import datetime

# Testing outside via VPN
ENDPOINT = 'http://data-storage.integration/prediction' 
PROMETHEUS = 'http://prometheus.integration'
# Inside cluster
ENDPOINT = 'http://data-storage-service.dkg-engine.svc.cluster.local:8080/prediction'
PROMETHEUS = 'http://monitoring-stack-prometheus-server.monitoring.svc.cluster.local:80'

TEST_DATA = {
    "aggregation_interval": 86400,
    "forecasting_lower_bounds": [5],
    "forecasting_model": "ARIMA",
    "forecasting_period": 1,
    "forecasting_upper_bounds": [5],
    "forecasting_values": [5],
    "metricId": "M02",
    "time": [
        "2024-07-12",
        "2024-07-13",
        "2024-07-14",
        "2024-07-15",
        "2024-07-16",
    ],
    "timeseries": [0,1,2,3,4]
}


def main():
    """
    Run prediction based on given input
    Implemented based on daily prediction 
    """
    cur_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')

    parser = argparse.ArgumentParser('Prediction service')
    parser.add_argument(
        '--prometheus_query', 
        type=str, 
        help='API endpoint to get the relevant metric', 
        default='sum(increase(kepler_container_joules_total{job=%27kepler%27}[1d]))&start=2024-08-11T00:00:00.000Z&'+f'end={cur_time}&step=86400s'
    )
    parser.add_argument('--forecasting_method', help='Choose forecasting method [ARIMA, HBNN]', default='ARIMA')
    parser.add_argument('--prometheus', help='Prometheus service hostname', default=PROMETHEUS)
    parser.add_argument('--dss_endpoint', help='Data storage service endpoint', default=ENDPOINT)
    args = parser.parse_args()

    # Get full query
    prometheus_query = f'{args.prometheus}/api/v1/query_range?query={args.prometheus_query}'
    # Get the metrics
    res = requests.get(prometheus_query)
    print(res.content)
    if (res.ok):
        res_json = json.loads(res.content)['data']['result'][0]['values']
        data_dict = {item[0]:item[1] for item in res_json}
        data_dict = dict(sorted(data_dict.items()))
        times = data_dict.keys()
        vals = data_dict.values()
        vals = np.array(list(vals)).astype(float)
        print('\ntimes', times)
        print('\nvals', vals)
        
        # Get the precition
        pred = AutoARIMA(vals, evaluate=1)
        print(pred.prediction, pred.upper_bound, pred.lower_bound)

        # Construct JSON format data to be posted
        data = {
            "aggregation_interval": 86400,
            "forecasting_lower_bounds": pred.lower_bound if isinstance(pred.lower_bound, list) else [pred.lower_bound],
            "forecasting_model": args.forecasting_method,
            "forecasting_period": 1,
            "forecasting_upper_bounds": pred.upper_bound if isinstance(pred.upper_bound, list) else [pred.upper_bound],
            "forecasting_values": pred.prediction if isinstance(pred.prediction, list) else [pred.prediction],
            "metricId": "M04",
            "time": [datetime.utcfromtimestamp(t).strftime('%Y-%m-%dT%H:%M:%S.000Z') for t in list(times)],
            "timeseries": list(vals)
        }

        return store(args.dss_endpoint, data)
    else:
        print(f'\nResponse: {res}')


def store(
    endpoint: str = ENDPOINT, 
    data: dict = TEST_DATA,
):
    """ Post data to REST API endpoint

    Parameters:
        endpoint: REST API endpoint
        data: dictionary for posting to data storage endpoint
    
    """
    print(data)
    res = requests.post(endpoint, json=data)
    print(res.status_code)
    return res.status_code


if __name__ == '__main__':
    main()
    #store()
