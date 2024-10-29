import requests
import unittest
import prediction

from model.autoarima import AutoARIMA
from datetime import datetime 
from unittest.mock import patch


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

# Testing outside via VPN
ENDPOINT = 'http://data-storage.integration/prediction' 
PROMETHEUS = 'http://prometheus.integration'
# Inside cluster
#ENDPOINT = 'http://data-storage-service.dkg-engine.svc.cluster.local:8080/prediction'
#PROMETHEUS = 'http://monitoring-stack-prometheus-server.monitoring.svc.cluster.local:80'


class TestPredictionService(unittest.TestCase):

    def test_prometheus(self,):
        """ Test retrieving data from prometheus """
        
        # Build query based on current time 
        cur_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        query = (
            'sum(increase(kepler_container_joules_total{job=%27kepler%27}[1d]))'
            f'&start=2024-08-11T00:00:00.000Z&'+f'end={cur_time}&step=86400s'
        )
        # Get full query
        prometheus_query = f'{PROMETHEUS}/api/v1/query_range?query={query}'
        # Get the metrics
        res = requests.get(prometheus_query)
        self.assertTrue(res.ok)

    def test_dss_service(self,):
        """ Test storing data into DSS service via API endpoint """
        self.assertEqual(prediction.store(ENDPOINT, TEST_DATA), 204)

    def test_prediction(self,):
        """ Test prediction falls into the confidence interval 
            of the forecasting model with simple example 
        """
         # Get the precition
        pred = AutoARIMA(TEST_DATA['timeseries'], evaluate=1)
        self.assertGreaterEqual(TEST_DATA['forecasting_values'][0], pred.lower_bound)
        self.assertLessEqual(TEST_DATA['forecasting_values'][0], pred.upper_bound)

    @patch('sys.argv', ['prediction.py', 
                        '--forecasting_method', 'ARIMA',
                        '--dss_endpoint', ENDPOINT,
                        '--prometheus', PROMETHEUS
                        ])
    def test_integration(self,):
        """ Test the whole pipeline of 
            querying data from Prometheus
            training and inference with AutoARIMA
            storing the results in DSS service
        """
        self.assertEqual(prediction.main(), 204)
