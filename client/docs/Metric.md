# Metric


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metric_id** | **str** |  | [optional] 
**timeseries** | **List[float]** |  | [optional] 
**forecasting_values** | **List[float]** |  | [optional] 
**forecasting_upper_bounds** | **List[float]** |  | [optional] 
**forecasting_lower_bounds** | **List[float]** |  | [optional] 
**forecasting_model** | **str** |  | [optional] 
**forecasting_period** | **int** |  | [optional] 
**time** | **List[date]** |  | [optional] 
**aggregation_interval** | **int** |  | [optional] 

## Example

```python
from template_web_client.models.metric import Metric

# TODO update the JSON string below
json = "{}"
# create an instance of Metric from a JSON string
metric_instance = Metric.from_json(json)
# print the JSON string representation of the object
print Metric.to_json()

# convert the object into a dict
metric_dict = metric_instance.to_dict()
# create an instance of Metric from a dict
metric_form_dict = metric.from_dict(metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


