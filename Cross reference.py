import pandas as pd
import numpy as np
import regex as re
RR_data = pd.read_csv("HP Assigned RR Archive Data_extended.csv")
CG_data = pd.read_csv("HP Assigned CGData.csv")
Match = np.zeros(len(CG_data))
CG_data.insert(loc=16, column='Cross Match', value=Match)
print(CG_data)
RR_data_serial = RR_data["Serial Number"]
RR_data_reporting_num = RR_data["Reporting Number"]
RR_data_reporting_mark = RR_data["Reporting Mark"]
print(RR_data_serial)
for i in range(len(CG_data)):
    loco_serial_num = CG_data.loc[i,"locomotive serial number"]
    loco_reporting_mark = CG_data.loc[i,"Reporting Mark"]
    loco_reporting_num = CG_data.loc[i,"Reporting Number"]
    if loco_serial_num > 0:
        if loco_serial_num in RR_data_serial:
            print(str(i),"True")
            CG_data.loc[i,"Cross Match"] = "Serial Match"
            continue
    if isinstance(loco_reporting_mark, str) and isinstance(loco_reporting_num, str):
        if loco_reporting_mark in RR_data_reporting_mark.values and loco_reporting_num in RR_data_reporting_num.values:
            CG_data.loc[i,"Cross Match"] = "Reporting Match"
            continue
print(CG_data)

With_Matching = CG_data[CG_data["Cross Match"] != 0]
With_Matching = With_Matching.reset_index()
for i in range(len(CG_data)):
    if CG_data.loc[i,"Cross Match"] == 0:
        CG_data.loc[i,"Cross Match"] = "Not Matched"
count_ranked = With_Matching['company name'].value_counts().reset_index()
count_ranked.columns = ['company name', 'Count']
count_ranked['Rank'] = count_ranked['Count'].rank(method='min', ascending=False).astype(int)


for i in range(len(count_ranked)):
    index_val = CG_data[CG_data['company name'] == count_ranked.loc[i,"company name"]].index
    val = index_val[0]
    count_ranked.loc[i,"affiliation"] = CG_data.loc[val, 'affiliation']
    count_ranked.loc[i,"former ID"] = CG_data.loc[val, 'former ID']
    count_ranked.loc[i,"industry type"] = CG_data.loc[val, 'industry type']
    count_ranked.loc[i,"city"] = CG_data.loc[val, 'city']
    count_ranked.loc[i,"state"] = CG_data.loc[val, 'state']
    count_ranked.loc[i,"address / directions"] = CG_data.loc[val, 'address / directions']
    count_ranked.loc[i,"Phone #"] = CG_data.loc[val, 'Phone #']
print(With_Matching)
print(count_ranked)
CG_data.to_csv("After_mathing.csv")
With_Matching.to_csv("Matched Subset.csv")
count_ranked.to_csv("Company list that has matched locomotices.csv")