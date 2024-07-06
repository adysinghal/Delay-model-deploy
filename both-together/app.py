import pandas as pd
import streamlit as st
import csv
import pickle
import math

df_delivery = pd.read_csv('estimation_cleaned.csv')

    
def prediction(warehouse_id1, pincode_id1):
    zone1 = int(pincode_id1 / 100000)
    sub_zone1 = int(pincode_id1 / 10000)
    sorting_district1 = int(pincode_id1 / 1000)
    return predictionHelper(warehouse_id1, pincode_id1, zone1, sub_zone1, sorting_district1)

def predictionHelper(warehouse_id1, pincode_id1, zone1, sub_zone1, sorting_district1):
    l = ['pincode_id', 'sorting_district', 'sub_zone', 'zone']
    l2 = [pincode_id1, sorting_district1, sub_zone1, zone1]
    for i in range(len(l)):
        temp = df_delivery[(df_delivery[l[i]] == l2[i]) & (df_delivery['warehouse_id'] == warehouse_id1)]['delivery_time']
        if not temp.empty:
            return math.ceil(temp.mean())
    for i in range(len(l)):
        temp = df_delivery[(df_delivery[l[i]] == l2[i])]['delivery_time']
        if not temp.empty:
            return math.ceil(temp.mean())
        
    return None

def predict(pincode, warehouse, list_of_codes):

    var1 = ['pincode_id', 'warehouse_id','ST-114','X-UNEX','CS-CSL','DLYLH-105','S-TAT2','S-MAR','EOD-38','FMOFP-101','CS-101','CS-104','DLYSHRTBAG-115','EOD-6O','EOD-11','DLYLH-126','DLYLH-133','DLYLH-136','DLYMR-118','DLYRG-125','X-OLL2F','DTUP-205','EOD-105','EOD-137','EOD-86','DLYLH-106','X-DBFR','DLYLH-115','EOD-3','DLYLH-152','DTUP-219','DLYB2B-108','FMEOD-152','RT-108','ST-108','ST-107','ST-115','DLYDC-107','EOD-138','EOD-6','EOD-111','DLYDC-101','DOFF-128','EOD-74','X-PNP','DTUP-210','RT-113','DLYSOR-101','RT-101','ST-117','DTUP-204','DLYRG-135','ST-110','DLYHD-007','DLYLH-104','DLYSU-100','ST-116','DLYLH-151','ST-NTL','ST-102','DTUP-207','EOD-36','DLYRG-130','X-SC','EOD-37','EOD-104','ST-NT','DTUP-235','ST-105','CL-106','DLYDG-120','DTUP-213','EOD-69','DLYDG-119','EOD-600','S-XIN','FMEOD-103','DLYDC-109','DLYDC-102','EOD-43','DLYLH-146','DLYRG-132','DTUP-ZL','U-FD','L-FD','DLYDC-105','DTUP-209','DTUP-203','X-PROM','DLYRG-120','DLYRPC-417','EOD-15','EOD-40','DLYB2B-101','S-MDIN','DLYLH-101','X-AWD','FMEOD-106','U-PMA','L-PMA','EOD-83','X-RWD','U-EOD','S-MNAR']

    my_dict = {item: 0.0 for item in var1}
    # pincode = int(input())
    # warehouse = int(input())
    my_dict['pincode_id'] = pincode
    my_dict['warehouse_id'] = warehouse
    user_list = list_of_codes

    for item in user_list:
        my_dict[item] = my_dict.get(item, 0) + 1  


    with open('output.csv', 'w', newline='') as csvfile:
        # Create a csv writer object
        writer = csv.writer(csvfile)
        # Write the header row (optional)
        writer.writerow(my_dict.keys())
        # Write the data row
        writer.writerow(my_dict.values())

    # print("CSV file created successfully!")

    # Load the pickled model
    with open("xgb_model.pkl", "rb") as f:
        xgb_model = pickle.load(f)
        # print("XGBoost model loaded successfully!")

    # Prepare your new test samples (X_new)
    # Ensure X_new has the same format (features and order) as your training data (X_train)

    X_test = pd.read_csv("output.csv")
    y_pred = xgb_model.predict(X_test)

    # Print the predictions or use them for further analysis
    # print("Predictions:", y_pred)
    # print(type(y_pred))
    return y_pred

def main():
    st.title('Delay Prediction Function')
    # warehouse_id = st.number_input('Enter Warehouse ID', min_value=1)
    pincode_id = st.number_input('Enter Pincode ID', min_value=100000, max_value=999999, key="pincode")
    warehouse_id = st.selectbox(
   'Warehouse ID',
   ("14","28","61","66", "68", "86","96","117","134","150","173","175"),
   index=None,
   placeholder="select from available warehouses",
   key="warehouse"
)
    list_of_codes = st.multiselect(
   'Enter the error codes encountered.',
   ['ST-114','X-UNEX','CS-CSL','DLYLH-105','S-TAT2','S-MAR','EOD-38','FMOFP-101','CS-101','CS-104','DLYSHRTBAG-115','EOD-6O','EOD-11','DLYLH-126','DLYLH-133','DLYLH-136','DLYMR-118','DLYRG-125','X-OLL2F','DTUP-205','EOD-105','EOD-137','EOD-86','DLYLH-106','X-DBFR','DLYLH-115','EOD-3','DLYLH-152','DTUP-219','DLYB2B-108','FMEOD-152','RT-108','ST-108','ST-107','ST-115','DLYDC-107','EOD-138','EOD-6','EOD-111','DLYDC-101','DOFF-128','EOD-74','X-PNP','DTUP-210','RT-113','DLYSOR-101','RT-101','ST-117','DTUP-204','DLYRG-135','ST-110','DLYHD-007','DLYLH-104','DLYSU-100','ST-116','DLYLH-151','ST-NTL','ST-102','DTUP-207','EOD-36','DLYRG-130','X-SC','EOD-37','EOD-104','ST-NT','DTUP-235','ST-105','CL-106','DLYDG-120','DTUP-213','EOD-69','DLYDG-119','EOD-600','S-XIN','FMEOD-103','DLYDC-109','DLYDC-102','EOD-43','DLYLH-146','DLYRG-132','DTUP-ZL','U-FD','L-FD','DLYDC-105','DTUP-209','DTUP-203','X-PROM','DLYRG-120','DLYRPC-417','EOD-15','EOD-40','DLYB2B-101','S-MDIN','DLYLH-101','X-AWD','FMEOD-106','U-PMA','L-PMA','EOD-83','X-RWD','U-EOD','S-MNAR']
)
    
    if st.button('Predict Delay'):
        if warehouse_id and pincode_id:
            delivery_time = predict(warehouse_id, pincode_id,list_of_codes)
            ans = delivery_time[0]
            
            st.success(f'Estimated Delay caused: {ans} days')
        else:
            st.warning('Please enter valid inputs.')

    if(st.button('Display code legend.')):
        df = pd.read_csv("potential red codes.csv")
        st.write(df)


    st.title('Delivery Estimation Function')
    # warehouse_id = st.number_input('Enter Warehouse ID', min_value=1)
    pincode_id = st.number_input('Enter Pincode ID', min_value=100000, max_value=999999)
    warehouse_id = st.selectbox(
   'Warehouse ID',
   ("14","28","61","66", "68", "86","96","117","134","150","173","175"),
   index=None,
   placeholder="select from available warehouses",
)

    if st.button('Predict Delivery Time'):
        if warehouse_id and pincode_id:
            delivery_time = prediction(warehouse_id, pincode_id)
            if delivery_time:
                st.success(f'Estimated Delivery Time: {delivery_time} days')
            else:
                st.warning('No matching data found for the given inputs.')
        else:
            st.warning('Please enter valid inputs.')


if __name__ == '__main__':
    main()