import requests
import allure
import csv
from STAGE_test_PJR.stage_settings_db_vs_azure import cursor

cursor.execute("SELECT NumAPI, WorkingInterests,TreatmentNumber from WellSummary JOIN TreatmentSummary ON WellSummary.WellSummaryId = TreatmentSummary.WellSummaryId order by NEWID()")
row = cursor.fetchone()
NumAPI = row[0]
WorkingInterest = row[1]
TreatmentNumber = row[2]
print(NumAPI)
print(WorkingInterest)
print(TreatmentNumber)


#String that you want to search
search_for = WorkingInterest
with open("STAGE_test_API/CustomerDataAPI_code/CustomerKeys.csv") as f_obj:
    reader = csv.reader(f_obj, delimiter=',')
    for row in reader:      #Iterates through the rows of your csv
        #print(row[0])          #line here refers to a row in the csv
        if row[0] in WorkingInterest:      #If the string you want to search is in the row
            print(row[0])
            print('Found: {}'.format(row[0]))
            b = row[1]
            print(row[1])

headers = {'content-type': 'application/json'}
url = 'https://test-fvnodeapipremium.azurewebsites.net/api/CustomerDataAPI'
params = {'code': 'KrMEEmrOAGSHrHlGYpXWuJG2L82mpqqGMsACkxdPY48khTSOnAV8QQ==', 'WellAPI': NumAPI, 'TreatmentNumber': TreatmentNumber, 'Key': b }
print(params)

@allure.feature('Send request to the CustomerDataAPI')
@allure.story('Send request with valid parameters')
@allure.step
def test_CustomerDataAPI_with_valid_parameters(headers=headers,url=url,params=params):

    response = requests.get(url, params=params, headers=headers)
    print(requests.get(url, params=params, headers=headers))

    assert response.status_code == 200

    url_content = response.content
    csv_file = open('STAGE_test_API/downloadedCSV/downloaded.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()
    print(response.content)

test_CustomerDataAPI_with_valid_parameters()


