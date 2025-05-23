import pandas as pd
import numpy as np
import regex as re
def find_serial_number(string):
    all_occurence = re.findall(r"\b\d{5}\b",string)
    if len(all_occurence) > 0:
        output = all_occurence[0].strip()
    else:
        return ""
    return output
def find_model_type(string):
    all_occurence = re.findall(r":(.*?)\(",string)
    if len(all_occurence) > 0:
        output = all_occurence[0].strip()
    else:
        return ""
    return output
def find_date(string):
    pattern = r"(?<!\d)(\d{1,2}-\d{2}|-\d{2})(?=\))"
    all_occurence = re.findall(pattern,string)
    if len(all_occurence) > 0:
        output = all_occurence[0].strip()
    else:
        return ""
    return output
Raw_data = pd.read_excel("CGdata12925.xlsx")
Raw_data = Raw_data[Raw_data["locomotives"].notna()]
Raw_data = Raw_data.reset_index()
Expanded_data = pd.DataFrame(np.zeros(shape=(0,12)),columns=[
    'company name','affiliation','former ID', 'ind',
    'city','state','address / directions','Phone #',
    'locomotive serial number','locomotive model',
    'Manufactured Date(MM/YY)','locomotives'
    ])
for i in range(len(Raw_data)):
    x_string = Raw_data.loc[i,"locomotives"]
    if len(x_string) > 0:
        x_list = re.split(r"\n", x_string)
        xlist_clean = [re.sub(r"\s+", " ", x) for x in x_list] # remove extra spaces
        # remove spaces at the beginning and end of each string
        xlist_clean = [x.strip() for x in xlist_clean]
        if len(xlist_clean) >= 1:
            for line in xlist_clean:
                row_number = len(Expanded_data)
                serial_numbers = find_serial_number(line) # Find all 5-digit number sequences that are engine serial numbers
                loco_type = find_model_type(line) # Find the Loco model listed after the ":" and before the "(", exceptions may occur
                build_date = find_date(line) # Find the build-date, most likely has a lot of exceptions, pattern is "-/YY" or "M-YY" or "MM-YY", need to be directly before a ")"
                Expanded_data.loc[row_number,"company name"] = Raw_data.loc[i,"company name"]
                Expanded_data.loc[row_number,"affiliation"] = Raw_data.loc[i,"affiliation"]
                Expanded_data.loc[row_number,"former ID"] = Raw_data.loc[i,"former ID"]
                Expanded_data.loc[row_number,"ind"] = Raw_data.loc[i,"ind"]
                Expanded_data.loc[row_number,"city"] = Raw_data.loc[i,"city"]
                Expanded_data.loc[row_number,"state"] = Raw_data.loc[i,"state"]
                Expanded_data.loc[row_number,"address / directions"] = Raw_data.loc[i,"address / directions"]
                Expanded_data.loc[row_number,"Phone #"] = Raw_data.loc[i,"Phone #"]
                Expanded_data.loc[row_number,"locomotive serial number"] = serial_numbers
                Expanded_data.loc[row_number,"locomotive model"] = loco_type
                Expanded_data.loc[row_number,"Manufactured Date(MM/YY)"] = build_date
cols = ['locomotive serial number','locomotive model','Manufactured Date(MM/YY)']
mask_all_empty = Expanded_data[cols].apply(lambda x: x.isna() | (x.str.strip() == ""),axis = 1).all(axis=1)
Expanded_data = Expanded_data[~mask_all_empty]
Expanded_data.to_csv("Expanded_CGData.csv")
# Full_data = pd.read_csv("CGdata_manual_processed.csv",encoding='cp1252')

# Full_data["Manufactured Date(MM/YY)"] = Full_data["Manufactured Date(MM/YY)"].astype(str)
# Expanded_data = pd.DataFrame(np.zeros(shape=(0,12)),columns=[
#     'company name','affiliation','former ID', 'ind',
#     'city','state','address / directions','Phone #',
#     'locomotive number','locomotive model',
#     'Manufactured Date(MM/YY)','locomotives'
#     ])
# for i in range(len(Full_data)):
#     #Find total number of ";"s and initiate another loop to iterate all instances
#     company_slice = Full_data.loc[i,:]
#     number_of_loco = len(company_slice["locomotive number"].rsplit(";"))-1
#     for loco in range(number_of_loco):
#         loco_slice = pd.DataFrame(np.zeros(shape=(1,12)),columns=[
#     'company name','affiliation','former ID', 'ind',
#     'city','state','address / directions','Phone #',
#     'locomotive number','locomotive model',
#     'Manufactured Date(MM/YY)','locomotives'
#     ])
#         loco_slice.loc[0,"company name"] = company_slice["company name"]
#         loco_slice.loc[0,"affiliation"] = company_slice["affiliation"]
#         loco_slice.loc[0,"former ID"] = company_slice["former ID"]
#         loco_slice.loc[0,"ind"] = company_slice["ind"]
#         loco_slice.loc[0,"city"] = company_slice["city"]
#         loco_slice.loc[0,"state"] = company_slice["state"]
#         loco_slice.loc[0,"address / directions"] = company_slice["address / directions"]
#         loco_slice.loc[0,"Phone #"] = company_slice["Phone #"]
#         loco_slice.loc[0,"locomotive number"] = company_slice["locomotive number"].rsplit(";",number_of_loco)[loco]
#         loco_slice.loc[0,"locomotive model"] = company_slice["locomotive model"].rsplit(";",number_of_loco)[loco]
#         loco_slice.loc[0,"Manufactured Date(MM/YY)"] = company_slice["Manufactured Date(MM/YY)"].rsplit(";",number_of_loco)[loco]
#         Expanded_data = pd.concat([Expanded_data,loco_slice],axis=0)
# Expanded_data.to_csv("Expanded_CGData.csv")
# # link_name = link_name.rsplit(".",1)[0]