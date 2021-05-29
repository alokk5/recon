# Token generation
import http.client
import mimetypes
import uuid
import json
import time
import base64
import logging

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

"""
ISA Segment: Interchange Control Header
Purpose:  To start and identify an interchange of one or more functional groups and 				
          interchange-related control segments.

General	Information:  This segment is mandatory. It contains the value of the data element separators,		
                      data segment terminators, the identify of the sender and receiver and the required 			
                      authorization and security information.

Example:
	ISA*00*      00*       ZZ*YOURID*ZZ*BGETESTWEH*950331*0915*U*003040*0001*0*T*
    1   2        3         4  5      7  8          9      10   1 2      3    4 5
Segment Ref
ID	    No. Segment Name	            Req. / Opt.	    Contents
------- --- --------------------------- ------------    ------------------------------------------
ISA01	I01	Auth. Information Qual	    Req.	        “00”
ISA02	I02	Auth. Information	        Req.	        All Spaces
ISA03	I03	Security Info. Qual.	    Req.	        “00”
ISA04	I04	Security Information	    Req.	        All Spaces
ISA05	105	Interchange ID Qual.	    Req.	        Trading Partner Defined
ISA06	I06	Interchange Sender ID	    Req.	        Your Interchange ID
ISA07	I05	Interchange ID Qual.	    Req.	        Test - “ZZ”  Prod - “01”
ISA08	I07	Interchange Receiver ID	    Req.	        Test - BGETEST___(3 initials)
                                                        Prod - “156171464” (BGE DUNS)
ISA09	I08	Date	                    Req.	        Creation Date (YYMMDD)
ISA10	I09	Time	                    Req.	        Creation Time. Time in 24-hour as follows: HHMM, or HHMMSS, etc
ISA11	I10	Interchange Cntrl. Stnds. Code	Req.	    “U”
ISA12	I11	Interchange Version ID	    Req.	        “00304”
ISA13	I12	Interchange Control No.	    Req.	        Sequential Number
ISA14	I13	Acknowledgment Requested	Req.	        “0”  (No) “1” (Yes)
ISA15	I14	Test Indicator	            Req.	        “T”  (Test) “P” (Production)
ISA16	I15	Sub Element Separator	    Req.	        Hex “3A”
"""

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
