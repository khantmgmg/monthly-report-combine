from gsheet import GoogleSheets as gs
from dataProcess import dataProcess as dp

def main():
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
  for sheetId in sheetIds:
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
