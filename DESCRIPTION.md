# Description
The prediction microservice aims to adaptively provide a forecasting functionality for
energy consumption time series data on the GLACIATION platform. For example, it
can be configured to forecast next-day energy consumption based on the daily
aggregated energy consumption of all pods from historical time series
* Relevant work package and deliverable: WP6, D6.3
* The time series and prediction results are available in [Grafana dashboard](http://grafana.validation/d/ddvavpoxwbtvke/prediction-service?orgId=1), in case it needs to be added again, the [grafana](https://github.com/glaciation-heu/glaciation-prediction-service/tree/main/grafana) folder contains the dashboard file

The microservice runs a daily batch job. 
* The first part of
the job retrieves daily aggregated energy consumption time series data from the Metric
Store, along with relevant metadata from metadata service if needed.
* Secondly, a forecasting model is trained based on the retrieved time series data.
* Thirdly, the trained model is used to predict the energy consumption of the upcoming day(s).
* Finally, the job is completed by storing the predictions via the [data storage service](https://github.com/glaciation-heu/glaciation-data-storage-service).
