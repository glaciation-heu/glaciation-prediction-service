# template_web_client.DefaultApi

All URIs are relative to *http://0.0.0.0:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_metric_by_id**](DefaultApi.md#get_metric_by_id) | **GET** /prediction/{metricId} | Retrieve historical and predicted time series by ID


# **get_metric_by_id**
> Metric get_metric_by_id(metric_id)

Retrieve historical and predicted time series by ID

Returns a time series metric

### Example


```python
import template_web_client
from template_web_client.models.metric import Metric
from template_web_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://0.0.0.0:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = template_web_client.Configuration(
    host = "http://0.0.0.0:8080"
)


# Enter a context with an instance of the API client
with template_web_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = template_web_client.DefaultApi(api_client)
    metric_id = 'metric_id_example' # str | Id of the metric to return

    try:
        # Retrieve historical and predicted time series by ID
        api_response = api_instance.get_metric_by_id(metric_id)
        print("The response of DefaultApi->get_metric_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_metric_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metric_id** | **str**| Id of the metric to return | 

### Return type

[**Metric**](Metric.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: applicatin/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | successful operation |  -  |
**400** | Invalid Id supplied |  -  |
**404** | Metric not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

