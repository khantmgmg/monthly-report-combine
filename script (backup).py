from gsheet import GoogleSheets as gs
from dataProcess import dataProcess as dp
import json
import os

dir = 'data/'
dataDir = os.listdir(dir)
for file in dataDir:
  filePath = os.path.join(dir, file)
  os.remove(filePath)

def main():
  print("Function call received")
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
  print(sheetIds)

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
  data = {}
  for sheetId in sheetIds[:2]:
    print(f"reading data from {sheetId}")
    service = gs(service_account_info, sheetId)
    sheetsData = service.batch_read(ranges)
    for sheetName in sheetsData:
      modSheetName = sheetName.replace("'","")
      modSheetName = modSheetName.replace(" ","_")
      modSheetName = modSheetName.replace(",","_")
      # print(f"{sheetName} : {modSheetName}")
      if not modSheetName in data:
        data[modSheetName] = []
      data[modSheetName] += sheetsData[sheetName]['listOfDict']

  data['All_provider'] = dp.restructure_all_provider(data['All_villages'],data['All_provider'])
  data['IPC_additional_and_PR_IPC'] = dp.total_ipc(data['IPC_additional'], data['Patient_record'])
  data['Meeting_supervision_stockout'] = dp.prepare_mss(data['Meeting_supervision_stockout'])
  data['Patient_record'] = dp.prepare_patient_record(data['Patient_record'])

  data['CaseMx'] = dp.casemx_by_rpMth_PvNpv(data['Patient_record'])
  data['RPP_calc'] = dp.rpp_calc(data['Patient_record'])
  data['Responded cases'] = dp.responded_cases(data['Patient_record'])
  data['CaseMx (RpMth)'] = dp.casemx_by_rpMth(data['Patient_record'])
  data['Positive_Only'] = dp.positive_only(data['Patient_record'])

  del data['IPC_additional']
  del data['Patient_record']

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
      data2write[shId][range] = data[sheet]

  # loop through data2write and write data to destination sheets
  for shId in data2write:
    service = gs(service_account_info, shId)
    writeInfo = service.batch_write_ranges(data2write[shId])
    print(writeInfo)

# main()