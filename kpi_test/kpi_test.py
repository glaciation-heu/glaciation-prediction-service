import time
import sys
import json
import subprocess
import requests

from colorama import Fore, Style
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')


# Testing accuracy and bound exceed during a certain period
START = '2025-04-14T00:00:00Z'
END = '2025-04-28T00:00:00Z'


dt_start = datetime.strptime(START, '%Y-%m-%dT%H:%M:%SZ')
ts_start = int(dt_start.timestamp()) * 1000
dt_end = datetime.strptime(END, '%Y-%m-%dT%H:%M:%SZ')
ts_end = int(dt_end.timestamp()) * 1000
print(ts_start, ts_end)


def test_energy_consumption():
    # Data range needs to be inline with data range stored in Prometheus of the cluster
    A_START = '2025-04-14T00:00:00Z'
    A_END = '2025-04-21T00:00:00Z'
    B_START = '2025-04-22T00:00:00Z'
    B_END = '2025-04-28T00:00:00Z'
    POD_ID = 'prediction-service-557b8c654b-lxrvm'

    A_PROMETHEUS_QUERY = 'sum(increase(kepler_container_joules_total{job=%27kepler%27, pod_name=%27' + POD_ID + '%27}[1d]))&start='+f'{A_START}&end={A_END}&step=86400s'
    B_PROMETHEUS_QUERY = 'sum(increase(kepler_container_joules_total{job=%27kepler%27, pod_name=%27' + POD_ID + '%27}[1d]))&start='+f'{B_START}&end={B_END}&step=86400s'
    A_PROMETHEUS_QUERY = f'http://prometheus.validation/api/v1/query_range?query={A_PROMETHEUS_QUERY}'
    B_PROMETHEUS_QUERY = f'http://prometheus.validation/api/v1/query_range?query={B_PROMETHEUS_QUERY}'

    print('#'* 80)

    # A/B Testing - A (Without AI decision engine)
    res_a = requests.get(A_PROMETHEUS_QUERY)
    print(res_a.content)
    if (res_a.ok):
        values = [float(x[1]) for x in json.loads(res_a.content)['data']['result'][0]['values']]
        avg_a = str(sum(values) / len(values))
        print(f'Average energy consumption (joules) before AI decision engine is enabled: {avg_a}')
    else:
        print(f'Error to get metrics before AI decision engine enabled: {res_a}')

    print(Fore.GREEN + 'PRETENT AI DECISION ENGINE TURNED ON ONE WEEK' + Style.RESET_ALL)

    # A/B Testing - B (AI decision engine enabled)
    res_b = requests.get(B_PROMETHEUS_QUERY)
    if (res_b.ok):
        values = [float(x[1]) for x in json.loads(res_b.content)['data']['result'][0]['values']]
        avg_b = str(sum(values) / len(values))
        print(f'Average energy consumption (joules) after AI decision engine is enabled: {avg_b}')
    else:
        print(f'Error to get metrics after AI decision engine enabled: {res_b}')

    assert avg_a >= avg_b
    print('✅ Energy consumption KPI test for prediction service passed...')
    print('#'* 92)


def get_results(curl_command: list, retry=0):
    result = subprocess.run(curl_command, capture_output=True, text=True)
    if result.returncode == 0:
        try: 
            # Parse the result as JSON
            data = json.loads(result.stdout)
            while data['results']['A']['status'] != 200 and retry < 10:
                print(f'Retrying due to connection status is not 200: {retry}')
                retry += 1
                time.sleep(2)
                return get_results(curl_command, retry)
            
            return data['results']['A']['frames'][0]['data']['values'][1]
        except json.JSONDecodeError as e:
            print(result.stdout)
    else:
            print(f'Error: {result.stderr}')


def test_prediction_accuracy():
    results = get_results(curl_command=['bash', 'ape.sh', str(ts_start), str(ts_end)])
    ape = sum(results) / len(results)
    print(f'Absolute percentage error: {ape}')

    assert ape < 5
    print('✅ Accuracy KPI test for prediction service passed...')


def test_exceed_bounds():
    results = get_results(curl_command=['bash', 'violation.sh', str(ts_start), str(ts_end)])
    vio = sum(results) / len(results)
    print(f'Violation percentage: {vio}')
    assert vio < 0.2
    print('✅ Prediction upper bound KPI test for prediction service passed...')

