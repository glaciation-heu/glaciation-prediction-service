#!/bin/bash

ts_start=$1
ts_end=$2

curl 'http://grafana.validation/api/ds/query?ds_type=influxdb&requestId=Q114' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Origin: http://grafana.validation' \
  -H 'Referer: http://grafana.validation/d/ddvavpoxwbtvke/prediction-service?orgId=1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'content-type: application/json' \
  -H 'x-dashboard-uid: ddvavpoxwbtvke' \
  -H 'x-datasource-uid: beauhtxsgxvy8c' \
  -H 'x-grafana-device-id: d5d3aeb505ef64740e7c82ad8f6153e6' \
  -H 'x-grafana-org-id: 1' \
  -H 'x-panel-id: 3' \
  -H 'x-panel-plugin-id: timeseries' \
  -H 'x-plugin-id: influxdb' \
  --data-raw '{"queries":[{"datasource":{"type":"influxdb","uid":"beauhtxsgxvy8c"},"query":"import \"math\"\r\n\r\n// Forecasting Upper\r\nforecasting_upper = from(bucket: \"energy_consumption\")\r\n    |> range(start: -14d)\r\n    |> filter(fn: (r) => \r\n        r._measurement == \"forecasting\" and\r\n        r._field == \"forecasting_upper\" and \r\n        r.aggregation_interval == \"86400\" and \r\n        r.metricId == \"M04\" \r\n    )\r\n    |> drop(columns: [\"input_size\", \"forecasting_time\"])\r\n    |> timeShift(duration: 1d, columns: [\"_time\"])\r\n    |> map(fn: (r) => ({\r\n      r with _value: r._value / 3600000.0\r\n    }))\r\n    |> rename(columns: {_value: \"forecasting_upper\"})\r\n\r\n// Forecasting Lower\r\nforecasting_lower = from(bucket: \"energy_consumption\")\r\n    |> range(start: -14d)\r\n    |> filter(fn: (r) => \r\n        r._measurement == \"forecasting\" and\r\n        r._field == \"forecasting_lower\" and \r\n        r.aggregation_interval == \"86400\" and \r\n        r.metricId == \"M04\" \r\n    )\r\n    |> drop(columns: [\"input_size\", \"forecasting_time\"])\r\n    |> timeShift(duration: 1d, columns: [\"_time\"])\r\n    |> map(fn: (r) => ({\r\n      r with _value: r._value / 3600000.0\r\n    }))\r\n    |> rename(columns: {_value: \"forecasting_lower\"})\r\n\r\n// Original Data\r\noriginal = from(bucket: \"energy_consumption\")\r\n    |> range(start: -14d)\r\n    |> filter(fn: (r) => \r\n        r._measurement == \"timeseries\" and\r\n        r.aggregation_interval == \"86400\" and \r\n        r.metricId == \"M04\" \r\n    )\r\n    |> map(fn: (r) => ({\r\n      r with _value: r._value / 3600000.0\r\n    }))\r\n    |> rename(columns: {_value: \"original\"})\r\n\r\n// Join original with forecasting_upper\r\nfirst_join = join(\r\n    tables: {original: original, forecast_upper: forecasting_upper},\r\n    on: [\"_time\"]\r\n)\r\n\r\n// Join the first result with forecasting_lower\r\nfinal_join = join(\r\n    tables: {first_join: first_join, forecast_lower: forecasting_lower},\r\n    on: [\"_time\"]\r\n)\r\n\r\n// Apply logic to compare and return 1 if conditions are met\r\nresult = final_join\r\n    |> map(fn: (r) => ({\r\n        r with \r\n        result: if r.original > r.forecasting_upper or r.original < r.forecasting_lower then 1 else 0\r\n    }))\r\n    |> keep(columns: [\"_time\", \"result\"])\r\n\r\nresult","refId":"A","datasourceId":5,"intervalMs":1800000,"maxDataPoints":379}],"from":"$ts_start","to":"$ts_end"}' \
  --insecure
