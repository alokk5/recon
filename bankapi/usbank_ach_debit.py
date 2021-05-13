# Token generation
import http.client
import mimetypes
import uuid
import json
import time
import base64

CLIENT_ID = 'wBQoKHD2AMSB1hGa8LOrmWHzYTWeV2lp'      #NEVER SHARE it with anyone
SECRET = 'slG10Hf5wyokTVEo'                         #NEVER SHARE IT with ANYONE

CORR_ID = str(uuid.uuid4())                         #This is like a CMG batch_number

def get_session_token():
    conn = http.client.HTTPSConnection("it-api.usbank.com")
    payload = 'grant_type=client_credentials'

    b4_encoded_client_id_secret = base64.b64encode(f'{CLIENT_ID}:{SECRET}'.encode()).decode()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Correlation-Id': CORR_ID,
        'Authorization': b4_encoded_client_id_secret #'Basic cG01RzBnbWVReDFBaUxlajNvSGFMdkdMZ1h0WmxwQU06bnJXSWlBVDRZeWptblZxcQ' #Ask USBank what this is for?
    }
    conn.request("POST", "/auth/oauth2/v1/token", payload, headers)
    time.sleep(3)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    json_obj = json.loads(data.decode('utf-8'))
    return json_obj['accessToken']

session_token = get_session_token()

# POST Payment
print("Posting payment")
conn = http.client.HTTPSConnection("it-api.usbank.com")
client_request_id = 'TRX-000000500'
company_name = 'Acme Inc.'
company_id = '123456789'
company_notes = 'blah blah blah,some more blah. well not enough, need more blah still'
company_descriptive_date = 'Jan 13'
discretionary_data = 'Some data'

#payload = "{ \r\n    \"transaction\": {\r\n    \"clientDetails\": {\r\n      \"clientID\": \"TXM47nzQvKX2CYNVmAFTRkxQbgazTw1P\",\r\n      \"clientRequestID\": \"TRX-000000500\"\r\n    },\r\n    \"requestorDetails\": {\r\n      \"companyName\": \"Tesla, In\",\r\n      \"companyID\": \"1123456789\",\r\n      \"companyNotes\": \"Company Notes\",\r\n      \"companyDescriptiveDate\" : \"Jan 13\",\r\n      \"discretionaryData\": \"DK\"\r\n    },\r\n    \"recipientDetails\": {\r\n      \"recipientType\": \"Individual\",\r\n      \"recipientName\": \"John Snow\",\r\n      \"recipientAccountType\": \"Savings\",\r\n      \"recipientAccountNumber\": \"77777777777777781\",\r\n      \"recipientRoutingNumber\": \"061000104\",\r\n      \"recipientIdentificationNumber\": \"1234\"\r\n    },\r\n    \"transactionDetails\": {\r\n      \"transactionType\": \"Payment\",\r\n      \"standardEntryClassCode\": \"CTX\",\r\n      \"isWebAuthorized\": false,\r\n      \"isPhoneAuthorized\": false,\r\n      \"effectiveDate\": \"2020-04-19 11:59:45Z\",\r\n      \"amount\": \"24000.0\",\r\n      \"isTestTransaction\" : false\r\n      \r\n     \r\n    },\r\n   \r\n\t\"communications\": {\r\n      \"commentsForRecipients\": \"PAYROLL AX\",\r\n      \"remittanceRecords\": [\"ISA*00*0000000000*00*0000000000*ZZ*11111111TRS *ZZ*US TREASURY 980312*002786659\",\"ISA*00*0000000000*00*0000000000*ZZ*11111111TRS *ZZ*US TREASURY 980312*002786659\"\r\n        \r\n      ]\r\n    }\r\n  }\r\n}"
print(payload)
payload = f"""{{
  "transaction": {{
    "clientDetails": {{
      "clientID": "{CLIENT_ID}",
      "clientRequestID": "TRX-000000500"
    }},
    "requestorDetails": {{
      "companyName": "TerrierMe",
      "companyID": "1123456789",
      "companyNotes": "Company Notes",
      "companyDescriptiveDate" : "Jan 13",
      "discretionaryData": "DK"
    }},
    "recipientDetails": {{
      "recipientType": "Individual",
      "recipientName": "John Snow",
      "recipientAccountType": "Savings",
      "recipientAccountNumber": "77777777777777781",
      "recipientRoutingNumber": "061000104",
      "recipientIdentificationNumber": "1234"
    }},
    "transactionDetails": {{
      "transactionType": "Payment",
      "standardEntryClassCode": "CTX",
      "isWebAuthorized": false,
      "isPhoneAuthorized": false,
      "effectiveDate": "2020-04-19 11:59:45Z",
      "amount": "24000.0",
      "isTestTransaction" : false
    }},
    "communications": {{
      "commentsForRecipients": "PAYROLLTAX",
      "remittanceRecords": [
        "ISA*00*0000000000*00*0000000000*ZZ*11111111TRS *ZZ*US TREASURY 980312*002786659",
        "ISA*00*0000000000*00*0000000000*ZZ*11111111TRS *ZZ*US TREASURY 980312*002786659"
      ]
    }}
  }}
}}"""

print(payload)
idempotency_key = uuid.uuid4()
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Accept-Encoding': 'accept-encoding',
  'Correlation-ID': f'{CORR_ID}',
  'Idempotency-Key': f'{idempotency_key}',  #GUID identifier assigned to each unique ACH request. This ID is used to
  #                                          prevent the initiation of more than one ACH transaction when identical
  #                                          requests are unintentionally received from an application.
  'Authorization': f'Bearer {session_token}'
}
conn.request("POST", "/gtm/money-movement/ach-sandbox/v1/transactions/domestic", payload, headers)
time.sleep(3)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# GET transaction
print("Getting Transaction")
conn = http.client.HTTPSConnection("it-api.usbank.com")
payload = ''
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Accept-Encoding': 'accept-encoding',
  'Correlation-ID': f'{CORR_ID}',
  'Idempotency-Key': f'{idempotency_key}',
  'Authorization': f'Bearer {session_token}'
}
conn.request("GET", "/gtm/money-movement/ach-sandbox/v1/transactions/ACH20200610-154050783", payload, headers)
time.sleep(3)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# Delete transaction
import http.client
import mimetypes
conn = http.client.HTTPSConnection("it-api.usbank.com")
payload = ''
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Accept-Encoding': 'accept-encoding',
  'Correlation-ID': f'{CORR_ID}',
  'Idempotency-Key': f'{idempotency_key}',
  'Authorization': f'Bearer {session_token}'
}
conn.request("DELETE", "/gtm/money-movement/ach-sandbox/v1/transactions/ACH20200610-154050783", payload, headers)
time.sleep(3)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
