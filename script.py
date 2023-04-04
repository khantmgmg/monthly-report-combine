from gsheet import GoogleSheets as gs
from dataProcess import dataProcess as dp
import json
import os
import pandas as pd



def main():
  print("Function call received")
  
  dir = 'data/'
  dataDir = os.listdir(dir)
  for file in dataDir:
    filePath = os.path.join(dir, file)
    os.remove(filePath)
    
  service_account_info = {
  "type": os.environ['type'],
  "project_id": os.environ['project_id'],
  "private_key_id": os.environ['private_key_id'],
  "private_key": os.environ['private_key'],
  "client_email": os.environ['client_email'],
  "client_id": os.environ['client_id'],
  "auth_uri": os.environ['auth_uri'],
  "token_uri": os.environ['token_uri'],
  "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
  "client_x509_cert_url": os.environ['client_x509_cert_url'],
}
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
      with open(filePath,'a') as f:
        df.to_csv(f, header=f.tell()==0, index=False)

  # Restructuring all_provider data
  print("Preparing all_provider data")
  csvAllVillages = pd.read_csv('data/All_villages.csv')
  csvAllVillages = csvAllVillages.to_dict(orient='records')
  csvAllProvider = pd.read_csv('data/All_provider.csv')
  csvAllProvider = csvAllProvider.to_dict(orient='records')
  # print(csvAllVillages)
  csvAllProvider = dp.restructure_all_provider(csvAllVillages, csvAllProvider)
  csvAllProvider = pd.DataFrame(csvAllProvider)
  # print(csvAllProvider)
  os.remove('data/All_provider.csv')
  with open('data/All_provider.csv','a') as f:
    csvAllProvider.to_csv(f, header=f.tell()==0, index=False)
    
  # Prepare patient record
  # Define the chunk size
  chunk_size = 100000
  
  # Open the large file in chunks
  for chunk in pd.read_csv('data/Patient_record.csv', chunksize=chunk_size, dtype={'Year in Carbonless':str, 'Reporting Year':str}):
  
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
    with open('data/Patient_record_new.csv', 'a') as f:
      chunk.to_csv(f, header=f.tell()==0, index=False)
  
  # Remove the original file
  os.remove('data/Patient_record.csv')
  # rename the new file to the original filename
  os.rename('data/Patient_record_new.csv', 'data/Patient_record.csv')

    
  
  
  # Preparing total IPC data from IPC_additional and Patient_record
  csvIpcAdditional = pd.read_csv('data/IPC_additional.csv')
  csvIpcAdditional = csvIpcAdditional.to_dict(orient='records')
  csvPR = pd.read_csv('data/Patient_record.csv')
  csvPR = csvPR.to_dict(orient='records')
  csvIpcAdditionalAndPrIPc = dp.total_ipc(csvIpcAdditional, csvPR)
  csvIpcAdditionalAndPrIPc = pd.DataFrame(csvIpcAdditionalAndPrIPc)
  with open('data/IPC_additional_and_PR_IPC.csv', 'a') as f:
    csvIpcAdditionalAndPrIPc.to_csv(f, header=f.tell()==0, index=False)

  # Preparing Meeting,Supervision,Stockout
  csvMss = pd.read_csv('data/Meeting_supervision_stockout.csv')
  csvMss = csvMss.to_dict(orient='records')
  csvMss = dp.prepare_mss(csvMss)
  csvMss = pd.DataFrame(csvMss)
  os.remove('data/Meeting_supervision_stockout.csv')
  with open('data/Meeting_supervision_stockout.csv', 'a') as f:
    csvMss.to_csv(f, header=f.tell()==0, index=False)

  csvPrOrig = pd.read_csv('data/Patient_record.csv')
  csvPrOrig = csvPrOrig.to_dict(orient='records')
  
  csvCaseMx = dp.casemx_by_rpMth_PvNpv(csvPrOrig)
  csvCaseMx = pd.DataFrame(csvCaseMx)
  with open('data/CaseMx.csv', 'a') as f:
    csvCaseMx.to_csv(f, header=f.tell()==0, index=False)

  
  csvRppCalc = dp.rpp_calc(csvPrOrig)
  csvRppCalc = pd.DataFrame(csvRppCalc)
  with open('data/RPP_calc.csv', 'a') as f:
    csvRppCalc.to_csv(f, header=f.tell()==0, index=False)
    
  # print(csvPrOrig[:10])
  csvRespondedCases = dp.responded_cases(csvPrOrig)
  csvRespondedCases = pd.DataFrame(csvRespondedCases)
  with open('data/Responded cases.csv', 'a') as f:
    csvRespondedCases.to_csv(f, header=f.tell()==0, index=False)

  csvCaseMxRpMth = dp.casemx_by_rpMth(csvPrOrig)
  csvCaseMxRpMth = pd.DataFrame(csvCaseMxRpMth)
  with open('data/CaseMx (RpMth).csv', 'a') as f:
    csvCaseMxRpMth.to_csv(f, header=f.tell()==0, index=False)

  csvPosOnly = dp.positive_only(csvPrOrig)
  csvPosOnly = pd.DataFrame(csvPosOnly)
  with open('data/Positive_Only.csv', 'a') as f:
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
      data = pd.read_csv(filePath)
      data = data.to_dict(orient='records')
      data2write[shId][range] = data

  # loop through data2write and write data to destination sheets
  for shId in data2write:
    service = gs(service_account_info, shId)
    writeInfo = service.batch_write_ranges(data2write[shId])
    print(writeInfo)