import json
import requests
import influxdb_client

from openapi_server.models.metric import Metric
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime, timezone, time, timedelta
from influxdb_client.client.write_api import SYNCHRONOUS


# Influx settings
DATA_ACCESS_BUCKET = 'data_access'
ENERGY_CONSUMPTION_BUCKET = 'energy_consumption'
ORG = 'glaciation'
TOKEN = 'iiN2cpMECn2ohmDQD8l4GDFUAwW7-GyV8a_IVZBPhJJY4kG6aBLERYZU4WsmBglWz4G72kUHxD_l_CUvT15Idw=='
URL = 'http://data-storage-service-db-data-storage-service-db.dkg-engine.svc.cluster.local:8086'
DSS_ENDPOINT = 'http://data-storage-service.dkg-engine.svc.cluster.local:8086'
# Testing
#URL = 'http://dss-db.integration'
#DSS_ENDPOINT = 'http://data-storage.integration'

client = influxdb_client.InfluxDBClient(
    url = URL,
    token = TOKEN,
    org = ORG
)


def query_dss(metricID: str) -> dict:
    """ Return the latest prediction results """
    # Get the latest date
    query_api = client.query_api()
    start_time = '2000-01-01T00:00:00Z'
    end_time = datetime.now(timezone.utc) + timedelta(days=7)
    end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    query = f'''
        from(bucket:"{ENERGY_CONSUMPTION_BUCKET}") 
        |> range(start: {start_time}, stop: {end_time}) 
        |> filter(fn:(r) => r._measurement == "forecasting")
        |> filter(fn:(r) => r.metricId == "M04") 
        |> group(columns: []) 
        |> max(column: "_time")
    '''
    
    res = query_api.query(org=ORG, query=query)
    forecasting_time = res[0].records[0].values.get('_time').strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f'Latest forecasting time: {forecasting_time}')

    # Call Data Storage API
    res = requests.get(
        f'{DSS_ENDPOINT}/prediction/M04?forecasting_time={forecasting_time}'
    )

    if res.status_code == 200:
        ts_dict = res.json()
        ts_json = json.dumps(ts_dict)
        
        return ts_json
    else:
        return f'''
            Status code to Data Storage Service: {res.status_code}
            URL: {res.url}
            Content: {res.text}
        '''

def query(metricID):
    """ This function is deprecated and will be removed in future versions.
        Please use `new_function()` instead.
    """
    sparql = SPARQLWrapper("http://192.168.0.94:3030/ds/sparql")
    sparql.setReturnFormat(JSON)
    
    # gets the first 3 geological ages
    # from a Geological Timescale database,
    # via a SPARQL endpoint

    query = """ 
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    prefix prov: <http://www.w3.org/ns/prov#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?measure ?date
    WHERE {
      ?subject rdf:type om:Measure .
      ?subject om:hasNumericalValue ?measure .
      ?subject prov:generatedAtTime ?date .
    }
    ORDER BY ASC(?date)
    LIMIT 30
    """

    sparql.setQuery("""
        SELECT ?a
        WHERE {
            ?a <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?b .
        }
        LIMIT 3
        """
    )

    sparql.setQuery(query)
    
    try:
        # Using SPARQL results
        #ret = sparql.queryAndConvert()
        #metric = Metric(id=metricID, time=[], value=[])
        #for r in ret["results"]["bindings"]:
        #    metric.value.append(float(r['measure']['value']))
        #    metric.time.append(r['date']['value'])
        #print(metric) 
        #ts_dict = {
        #    'id': metricID,
        #    'time': metric.time,
        #    'value': metric.value
        #}

        # Dummpy data for testing
        ts_dict = {
            "aggregation_interval": 90,
            "forecasting_lower_bounds": [
              4
            ],
            "forecasting_model": "ARIMA",
            "forecasting_period": 1,
            "forecasting_upper_bounds": [
              6
            ],
            "forecasting_values": [
              5
            ],
            "metricId": metricID,
            "time": [
              "2024-03-20"
            ],
            "timeseries": [
              1,2,3,4
            ]
        }        

        ts_json = json.dumps(ts_dict)
        
        return ts_json
    except Exception as e:
        print(e)
        return str(e)


if __name__ == '__main__':
    query_dss('M04')
