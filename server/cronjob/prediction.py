import argparse
import requests
import json
import numpy as np

from model.autoarima import AutoARIMA


def main():
    """
    Run prediction based on given input
    """
    parser = argparse.ArgumentParser('Prediction service')
    parser.add_argument(
        '--prometheus_query', 
        type=str, 
        help='API endpoint to get the relevant metric', 
        default='http://prometheus.integration/api/v1/query_range?query=sum(increase(kepler_container_joules_total{job=%27kepler%27}[10m]))&start=2024-07-20T00:00:00.000Z&end=2024-07-23T00:00:00.000Z&step=600s'
    )
    parser.add_argument('--forecasting_method', help='Choose forecasting method [ARIMA, HBNN]', default='ARIMA')
    args = parser.parse_args()

    # Get the metrics
    res = requests.get(args.prometheus_query)
    if (res.ok):
        res_json = json.loads(res.content)['data']['result'][0]['values']
        data_dict = {item[0]:item[1] for item in res_json}
        data_dict = dict(sorted(data_dict.items()))
        vals = data_dict.values()
        vals = np.array(list(vals)).astype(float)
        print(vals)
        
        # Get the precition
        pred = AutoARIMA(vals, evaluate=10)
        print(pred)
    else:
        print(f'Response: {res}')


if __name__ == '__main__':
    main()
