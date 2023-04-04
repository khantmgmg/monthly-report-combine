from gsheet import GoogleSheets as gs
from dataProcess import dataProcess as dp
import json
import os
import pandas as pd
from dotenv import load_dotenv
import time
load_dotenv()

def clear_data_folder():
  dir = 'data/'
  dataDir = os.listdir(dir)
  for file in dataDir:
    filePath = os.path.join(dir, file)
    os.remove(filePath)

def main():
  print("Function call received")
  clear_data_folder()

  service_account_info = {
    "type": "service_account",
    "project_id": "combine-report",
    "private_key_id": "4d2d7a7a0959ba9aec04827060e15bce2f3552b9",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDTyzizDcbVQXFj\nxxCcjoFEQqk5pbLNhwZ9/sNTecQwUv46R2tVZ9WtrtXivCmVx4uWKw/AeLMcdWtN\nVwMAmfIVPWM9hYKcocHHr05TmD80+YFGuxRZYyD8KcuGoAYBb7mM+3Fyu3YvIh3I\nLM45D7v+7CfRV1oOt6n7n+idkjJy5uT6jGRvBnDojjObGV6LwLqZTQLgALrU/SLf\nzRWXxkOU3qMvQKbU39+nQnhbAm2wL6be6MmQ7bSkSMIyIoX2SMFvxiH/AXsJcsGP\noypLhSc1UuOEcM7vBfcArjvMC7iCUlGVo+MQo19aMcqy5VV0fYKY2RYjtU9HAP8a\n+AXqE4UVAgMBAAECggEAFX7VMNsPmJpNQ1azWWhfN0naugaWuKRhJM2EDodXwZ3S\nvqB8BM2GktuhSqNVRyXbBXE2Zo75gsRqEQ3pOJjnSH+UAGz5/iKus7EXroVPuPUv\nyTl4jb/xW5Z0WSQJqACqYOQuNfpPuuXoBuaBQapWpr9aJTWL5t1+K5MlvURWyXF1\nX8Thd5iJRpLew+ixuHMtqIZcD9LPV9D+gmGBa37xT4EhB24XXlNiW14RyHFAd6WT\nS/4kvlyQYrq/fY4306rgN3A3xDoj4//R13StTGJnWDdp5MBbvU/pIeWMfeQRHOdn\nzLt0hnpj6N3q/YkNIjQ/yOuw85amaMahKtd0SNMy2wKBgQD5lt7SdAzLtMVdFHgg\nahKehMtQEgu42brKIQ0axnVO76M2bbetNmrMn8ErryCWL30R56QnjNKKSbedS7y3\nF9oBGW/zZ5a7rCZCdcmO8RHHey8PzfKX6QFtBJO2G3cluuObsi4BLONSQT5AvDZO\nPWvDvLCYSwnT0MRnbyaxNNm3+wKBgQDZO9VlUQOUfpRY311Oox4foePWoR+95GJz\nteDCc9q/oYBMCg9rfNQmnBu+iVGrvwu4pCgQ5gQo3FeFEZeJ3XZvHc0K/hr6PrtJ\n/y1sR9p5Kaq9rCFTWAJ7Z8jp5Pqajf0z7hK/bTY2WKK4dVg7c7/dGswvIOg3OezZ\nMoT8aB3aLwKBgBVYjuQG4tVFN5/3UTLMf50pFE5bzL7ZeD0zSHCiyoOewSG1joD0\n53tqqlW3G51coGC4o/Rx+cuz9E0yngg2tQFlEIsLr/uLBJaohj2AZpnd8i9y2K2f\nUuzk+FEZ1j3W1wKI4aBeG278f3t/3VEhtaa+64eK22NPNoz2F6QONhSjAoGBAKnt\nPPsZCUTiUybF6tY1kL3LxE7DEPJYsY6z6hIR0D5wlcxlXjSFm+pr2OQNxJ4lPoT7\nm//D/eL8oVWNMk38t8UpuZfst6ui4Jx8iMqX1lVK+62M9TCduqtPvwD/Re0aPsOd\nanrlci/G29qQqCkxXRcW/DutcRiqLhSkiRRsWVWvAoGBAKftIPZJSKBPqMWV3fJA\nd5MCCZWQB34GkaUSkQIZ+IBtMJ3PjJ/8bWQOrZ8yrWyW5wzo2bfVGtD/9iB1RypB\n6w+ntBH/UV2COhyBQLrrDgIGqTcfXoJfdnqTKhYSSLY2SWvkv0m59y1xXmd6/XLp\nAOQPpwrco99p4o+E2vz5bqWQ\n-----END PRIVATE KEY-----\n",
    "client_email": "pmi-em-mel-central@combine-report.iam.gserviceaccount.com",
    "client_id": "117235204728811468597",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pmi-em-mel-central%40combine-report.iam.gserviceaccount.com",
  }
#   service_account_info = {
#   "type": os.getenv('type'),
#   "project_id": os.getenv('project_id'),
#   "private_key_id": os.getenv('private_key_id'),
#   "private_key": os.getenv('private_key'),
#   "client_email": os.getenv('client_email'),
#   "client_id": os.getenv('client_id'),
#   "auth_uri": os.getenv('auth_uri'),
#   "token_uri": os.getenv('token_uri'),
#   "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url'),
#   "client_x509_cert_url": os.getenv('client_x509_cert_url')
# }
  # Getting the sheet IDs of report files
  getSheetIdService = gs(service_account_info, '16ru3j-n3b0mpdqSUL2586v-p0_N_P4nFFZJgkHMnTuw')
  getSheetId = getSheetIdService.read_range('LF!A1:B')
  sheetIds = []
  for fileData in getSheetId['listOfDict']:
    link = fileData['File URL']
    link = link.split("/")[5]
    sheetIds.append(link)
  # print(sheetIds)

  # Defining ranges of report file
  ranges = [
        "All_provider!A2:Q",
        "All_villages!A1:AG",
        "Potential malaria outbreak!A1:P",
        "PLA session!A1:X",
        "IPC_additional!A1:K",
        "GHT,Worksite HE!A1:Q",
        "LLIN dist(mass,continuous)!A1:AB",
        "LLIN dist(ANC)!A1:P",
        "LLIN dist(Other)!A1:I",
        "CBO,CSG,EHO support!A1:J",
        "Recruitment!A1:Q",
        "C19 material distribution!A1:K",
        "IEC,material distribution!A1:L",
        "Meeting,supervision,stockout!A1:AG",
        "RDT,ACT,CQ,PQ distribution!A1:I",
        "procurement!A1:H",
        "Design,develop!A1:K",
        "Study,assessment,survey!A1:J",
        "visits!A2:K",
        "Training,Meeting,Workshop!A1:Q",
        "Training attendance (Provider)!A1:AA",
        "CSG!A3:T",
        "ICMV other disease!A3:AD",
        "Expired drug!A1:Q",
        "CSG (small grant)!A1:L",
        "Waste disposal!A2:V",
        "Patient record!A1:AZ"
    ]
  
  # Get data from all report files and save it in data.
  # data = {}
  for sheetId in sheetIds:
    time.sleep(1)
    print(f"reading data from {sheetId}")
    service = gs(service_account_info, sheetId)
    sheetsData = service.batch_read(ranges)
    for sheetName in sheetsData:
      modSheetName = sheetName.replace("'","")
      modSheetName = modSheetName.replace(" ","_")
      modSheetName = modSheetName.replace(",","_")
      # print(f"{sheetName} : {modSheetName}")
      df = pd.DataFrame(sheetsData[sheetName]['listOfDict'])
      filePath = f"data/{modSheetName}.csv"
      with open(filePath,'a', encoding='utf-8') as f:
        df.to_csv(f, header=f.tell()==0, index=False)

  # Restructuring all_provider data
  print("Preparing all_provider data")
  csvAllVillages = pd.read_csv('data/All_villages.csv', encoding='utf-8')
  csvAllVillages = csvAllVillages.to_dict(orient='records')
  csvAllProvider = pd.read_csv('data/All_provider.csv', encoding='utf-8')
  csvAllProvider = csvAllProvider.to_dict(orient='records')
  # print(csvAllVillages)
  csvAllProvider = dp.restructure_all_provider(csvAllVillages, csvAllProvider)
  csvAllProvider = pd.DataFrame(csvAllProvider)
  # print(csvAllProvider)
  os.remove('data/All_provider.csv')
  with open('data/All_provider.csv','a', encoding='utf-8') as f:
    csvAllProvider.to_csv(f, header=f.tell()==0, index=False)
    
  # Prepare patient record
  # Define the chunk size
  chunk_size = 100000
  
  # Open the large file in chunks
  for chunk in pd.read_csv('data/Patient_record.csv', chunksize=chunk_size, dtype={'Year in Carbonless':str, 'Reporting Year':str}, encoding='utf-8'):
  
    # Clean up the data
    chunk['Year in Carbonless'] = chunk['Year in Carbonless'].astype(str).str.replace(',', '')
    chunk['Reporting Year'] = chunk['Reporting Year'].astype(str).str.replace(',', '')
    chunk['Year in Carbonless'] = pd.to_numeric(chunk['Year in Carbonless'], errors='coerce').fillna(0).astype(int)
    chunk['Reporting Year'] = pd.to_numeric(chunk['Reporting Year'], errors='coerce').fillna(0).astype(int)
  
    # Convert to dictionary and prepare the data
    chunk = chunk.to_dict(orient='records')
    chunk = dp.prepare_patient_record(chunk)
    chunk = pd.DataFrame(chunk)
  
    # Append to the new file
    with open('data/Patient_record_new.csv', 'a', encoding='utf-8') as f:
      chunk.to_csv(f, header=f.tell()==0, index=False)
  
  # Remove the original file
  os.remove('data/Patient_record.csv')
  # rename the new file to the original filename
  os.rename('data/Patient_record_new.csv', 'data/Patient_record.csv')

    
  
  
  # Preparing total IPC data from IPC_additional and Patient_record
  csvIpcAdditional = pd.read_csv('data/IPC_additional.csv', encoding='utf-8')
  csvIpcAdditional = csvIpcAdditional.to_dict(orient='records')
  csvPR = pd.read_csv('data/Patient_record.csv', encoding='utf-8')
  csvPR = csvPR.to_dict(orient='records')
  csvIpcAdditionalAndPrIPc = dp.total_ipc(csvIpcAdditional, csvPR)
  csvIpcAdditionalAndPrIPc = pd.DataFrame(csvIpcAdditionalAndPrIPc)
  with open('data/IPC_additional_and_PR_IPC.csv', 'a', encoding='utf-8') as f:
    csvIpcAdditionalAndPrIPc.to_csv(f, header=f.tell()==0, index=False)

  # Preparing Meeting,Supervision,Stockout
  csvMss = pd.read_csv('data/Meeting_supervision_stockout.csv', encoding='utf-8')
  csvMss = csvMss.to_dict(orient='records')
  csvMss = dp.prepare_mss(csvMss)
  csvMss = pd.DataFrame(csvMss)
  os.remove('data/Meeting_supervision_stockout.csv')
  with open('data/Meeting_supervision_stockout.csv', 'a', encoding='utf-8') as f:
    csvMss.to_csv(f, header=f.tell()==0, index=False)

  csvPrOrig = pd.read_csv('data/Patient_record.csv', encoding='utf-8')
  csvPrOrig = csvPrOrig.to_dict(orient='records')
  
  csvCaseMx = dp.casemx_by_rpMth_PvNpv(csvPrOrig)
  csvCaseMx = pd.DataFrame(csvCaseMx)
  with open('data/CaseMx.csv', 'a', encoding='utf-8') as f:
    csvCaseMx.to_csv(f, header=f.tell()==0, index=False)

  
  csvRppCalc = dp.rpp_calc(csvPrOrig)
  csvRppCalc = pd.DataFrame(csvRppCalc)
  with open('data/RPP_calc.csv', 'a', encoding='utf-8') as f:
    csvRppCalc.to_csv(f, header=f.tell()==0, index=False)
    
  # print(csvPrOrig[:10])
  csvRespondedCases = dp.responded_cases(csvPrOrig)
  csvRespondedCases = pd.DataFrame(csvRespondedCases)
  with open('data/Responded cases.csv', 'a', encoding='utf-8') as f:
    csvRespondedCases.to_csv(f, header=f.tell()==0, index=False)

  csvCaseMxRpMth = dp.casemx_by_rpMth(csvPrOrig)
  csvCaseMxRpMth = pd.DataFrame(csvCaseMxRpMth)
  with open('data/CaseMx (RpMth).csv', 'a', encoding='utf-8') as f:
    csvCaseMxRpMth.to_csv(f, header=f.tell()==0, index=False)

  csvPosOnly = dp.positive_only(csvPrOrig)
  csvPosOnly = pd.DataFrame(csvPosOnly)
  with open('data/Positive_Only.csv', 'a', encoding='utf-8') as f:
    csvPosOnly.to_csv(f, header=f.tell()==0, index=False)

  os.remove('data/IPC_additional.csv')
  os.remove('data/Patient_record.csv')

  sheetsAndId = {
      "16xXmqe21mk70GJKmCwQklndkD_gQEAOA-J8dcERfLr0":[
          "All_villages","All_provider","RPP_calc"
      ],
      "1L0hm_toCwILwAOMWWvfN0-InfJQKBPKoOQBMDQU7CUw":[
          "Positive_Only","CaseMx (RpMth)","Responded cases"
      ],
      "1A03pSW9EXcH8IdQJSEjJE627putJel_0g2NSn7no8DU":[
          "CaseMx","Potential_malaria_outbreak","PLA_session","IPC_additional_and_PR_IPC","GHT_Worksite_HE","LLIN_dist(mass_continuous)","LLIN_dist(ANC)","LLIN_dist(Other)",
          "CBO_CSG_EHO_support","Recruitment","C19_material_distribution","IEC_material_distribution","Meeting_supervision_stockout","RDT_ACT_CQ_PQ_distribution",
          "procurement","Design_develop","Study_assessment_survey","visits","Training_Meeting_Workshop","Training_attendance_(Provider)","CSG","ICMV_other_disease","Expired_drug",
          "CSG_(small_grant)","Waste_disposal"
      ]
  }
  range2clear = {}
  # set ranges to be cleared
  for shId in sheetsAndId:
    for sheet in sheetsAndId[shId]:
      if not shId in range2clear:
        range2clear[shId] = []
      range2clear[shId].append(sheet + "!A:ZZ")

  # loop through range2clear items and clear the defined range of sheets
  for shId in range2clear:
    service = gs(service_account_info, shId)
    clearInfo = service.batch_clear_ranges(range2clear[shId])
    print(clearInfo)

  #setting data to write to combined report files
  data2write = {}
  for shId in sheetsAndId:
    for sheet in sheetsAndId[shId]:
      if not shId in data2write:
        data2write[shId] = {}
      range = sheet + "!A1"
      filePath = f"data/{sheet}.csv"
      data = pd.read_csv(filePath, encoding='utf-8')
      data = data.to_dict(orient='records')
      data2write[shId][range] = data

  # loop through data2write and write data to destination sheets
  for shId in data2write:
    service = gs(service_account_info, shId)
    writeInfo = service.batch_write_ranges(data2write[shId])
    print(writeInfo)
  clear_data_folder()

main()