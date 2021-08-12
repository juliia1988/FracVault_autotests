import requests
import json
import allure
from DEV_test_ETL.settings_for_etl import cursor

cursor.execute("select numAPI, TreatmentNumber, Operator from [dbo].WellSummary INNER JOIN TreatmentSummary on TreatmentSummary.WellSummaryId = WellSummary.WellSummaryId order by NEWID()")
row = cursor.fetchone()
new_numAPI = row[0]
new_interval = row[1]
new_operator = row[2]
print(new_numAPI,new_interval,new_operator)

url = 'https://witsmlapitrigger.azurewebsites.net/api/GenerateWitsmlAndSendEmail'
email = "yuliia.sokolova3@halliburton.com"
code = 'c4QwXXPhK/AzgTjpyal8DUZ/P9qtIEbLzXQtTKOXrNmxl/POmiuwkA=='
headers = {'content-type': 'application/json'}
data = {"numAPI": [new_numAPI], "Intervals": [str(new_interval)], "email": email, "operator": [new_operator], "WITSMLObjects": ["ALL"], "ExcludeElements": [[""]]}
params = {'code': code}

#data = {"numAPI": ["05-001-09880-00"], "Intervals": ["9"], "email": "yuliia.sokolova3@halliburton.com", "operator": ["Great Western"], "WITSMLObjects": ["ALL"], "ExcludeElements": [[""]]}
#params = {'code': 'c4QwXXPhK/AzgTjpyal8DUZ/P9qtIEbLzXQtTKOXrNmxl/POmiuwkA=='}


@allure.feature('Send request to the WITSML send Email API')
@allure.story('Send request with valid parameters')
@allure.step
def test_witsml_send_email_with_valid_parameters(headers=headers,url=url,data=data,params=params):

    response = requests.post(url, params=params, data=json.dumps(data), headers=headers)

    assert response.status_code == 200
    print(response.content)

test_witsml_send_email_with_valid_parameters()

@allure.feature('Send request to the WITSML send Email API')
@allure.story('Send request with Exclude elements parameters')
@allure.step
def test_witsml_send_email_with_ExcludeElements_parameters(headers=headers,url=url):

    data = {"numAPI": ["05-001-09880-00"], "Intervals": ["1"], "email": "yuliia.sokolova3@halliburton.com",
                "operator": ["Great Western"], "WITSMLObjects": ["ALL"],
                "ExcludeElements": [["/pds:stimJobs/pds:stimJob/pds:jobInterval/pds:totalProppantUsage","/pds:stimJobs/pds:stimJob/pds:jobInterval/pds:flowPath/pds:tubular"]]}
    params = {'code': 'c4QwXXPhK/AzgTjpyal8DUZ/P9qtIEbLzXQtTKOXrNmxl/POmiuwkA=='}

    response = requests.post(url, params=params, data=json.dumps(data), headers=headers)

    assert response.status_code == 200
    print(response.content)
test_witsml_send_email_with_ExcludeElements_parameters()

@allure.feature('Send request to the WITSML send Email API')
@allure.story('Send request with empty WITSML object parameter')
@allure.step
def test_witsml_send_email_with_emptyWITSMLObjects_parameter(headers=headers,url=url):

    data = {"numAPI": [new_numAPI], "Intervals": [str(new_interval)], "email": email, "operator": [new_operator], "WITSMLObjects": ["ALL"], "ExcludeElements": [[""]]}
    params = {'code': 'c4QwXXPhK/AzgTjpyal8DUZ/P9qtIEbLzXQtTKOXrNmxl/POmiuwkA=='}

    response = requests.post(url, params=params, data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    print(response.content)

    assert response.content == b'WITSMLObjects must not be empty. '
test_witsml_send_email_with_emptyWITSMLObjects_parameter()

@allure.feature('Send request to the WITSML send Email API')
@allure.story('Send request without numAPI parameters')
@allure.step
def test_witsml_send_email_without_numAPI_parameter(headers=headers,url=url):

    data = {"Intervals": [str(new_interval)], "email": email, "operator": [new_operator], "WITSMLObjects": ["ALL"], "ExcludeElements": [[""]]}
    params = {'code': 'c4QwXXPhK/AzgTjpyal8DUZ/P9qtIEbLzXQtTKOXrNmxl/POmiuwkA=='}

    response = requests.post(url, params=params, data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    print(response.content)

    assert response.content == b'Request should contain exactly 1 NumAPIWITSMLObjects must not be empty. '

test_witsml_send_email_without_numAPI_parameter()