import pandas as pd
import numpy as np
Full_data = pd.read_csv("CGdata_manual_processed.csv",encoding='cp1252')
Full_data["Manufactured Date(MM/YY)"] = Full_data["Manufactured Date(MM/YY)"].astype(str)
Expanded_data = pd.DataFrame(np.zeros(shape=(0,12)),columns=[
    'company name','affiliation','former ID', 'ind',
    'city','state','address / directions','Phone #',
    'locomotive number','locomotive model',
    'Manufactured Date(MM/YY)','locomotives'
    ])
for i in range(len(Full_data)):
    #Find total number of ";"s and initiate another loop to iterate all instances
    company_slice = Full_data.loc[i,:]
    number_of_loco = len(company_slice["locomotive number"].rsplit(";"))-1
    for loco in range(number_of_loco):
        loco_slice = pd.DataFrame(np.zeros(shape=(1,12)),columns=[
    'company name','affiliation','former ID', 'ind',
    'city','state','address / directions','Phone #',
    'locomotive number','locomotive model',
    'Manufactured Date(MM/YY)','locomotives'
    ])
        loco_slice.loc[0,"company name"] = company_slice["company name"]
        loco_slice.loc[0,"affiliation"] = company_slice["affiliation"]
        loco_slice.loc[0,"former ID"] = company_slice["former ID"]
        loco_slice.loc[0,"ind"] = company_slice["ind"]
        loco_slice.loc[0,"city"] = company_slice["city"]
        loco_slice.loc[0,"state"] = company_slice["state"]
        loco_slice.loc[0,"address / directions"] = company_slice["address / directions"]
        loco_slice.loc[0,"Phone #"] = company_slice["Phone #"]
        loco_slice.loc[0,"locomotive number"] = company_slice["locomotive number"].rsplit(";",number_of_loco)[loco]
        loco_slice.loc[0,"locomotive model"] = company_slice["locomotive model"].rsplit(";",number_of_loco)[loco]
        loco_slice.loc[0,"Manufactured Date(MM/YY)"] = company_slice["Manufactured Date(MM/YY)"].rsplit(";",number_of_loco)[loco]
        Expanded_data = pd.concat([Expanded_data,loco_slice],axis=0)
Expanded_data.to_csv("Expanded_CGData.csv")
# link_name = link_name.rsplit(".",1)[0]