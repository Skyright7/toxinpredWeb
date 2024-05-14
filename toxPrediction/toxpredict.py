import numpy as np
import pandas as pd
import joblib

output_path = './data/outputData'

def toxPredictionOne(task_id,base_file_path,Threshold):
    data = pd.read_csv(base_file_path,index_col=0)
    thr = Threshold
    # acc calculation
    std = list("ACDEFGHIKLMNPQRSTVWY")
    dd = []
    for j in data['sequence']:
        cc = []
        for i in std:
            count = 0
            for k in j:
                temp1 = k
                if temp1 == i:
                    count += 1
                composition = (count/len(j))*100
            cc.append(composition)
        dd.append(cc)
    data['ACC']= dd
    # dpc calculation
    dd = []
    zz = data.sequence
    q = 1
    for i in range(0, len(zz)):
        cc = []
        for j in std:
            for k in std:
                count = 0
                temp = j + k
                for m3 in range(0, len(zz[i]) - q):
                    b = zz[i][m3:m3 + q + 1:q]
                    b.upper()
                    if b == temp:
                        count += 1
                    composition = (count / (len(zz[i]) - (q))) * 100
                cc.append(composition)
        dd.append(cc)
    data['DPC'] = dd
    # concatenate
    acc = np.array(data['ACC'].tolist())
    dpc = np.array(data['DPC'].tolist())
    X_test = np.concatenate([acc, dpc], axis=1)
    print(X_test)
    # load model
    clf = joblib.load('./modelWeight/toxinpred3.0_model.pkl')
    # prediction
    y_p_score1 = clf.predict_proba(X_test)
    y_p_s1 = y_p_score1.tolist()
    # select last row(toxin) (first row mean un_toxin) as result
    tempdf = pd.DataFrame(y_p_s1)
    df_1 = tempdf.iloc[:, -1]
    data['tox_score'] = df_1
    cc = []
    for i in range(len(data)):
        if data['tox_score'][i]>=float(thr):
            cc.append('Toxin')
        else:
            cc.append('Non-Toxin')
    data['tox_prediction'] = cc
    # calculate PPV
    data['tox_PPV'] = (data['tox_score'] * 1.2341) - 0.1182
    # drop the ACC and DPC which do not need output
    data = data.drop(columns=['ACC', 'DPC'])
    # output as file
    out_file_path = f'{output_path}/id_{task_id}_tox_out.csv'
    data.to_csv(out_file_path)
    return out_file_path

# if __name__ == '__main__':
#     base_file_path = '../data/inputData/id_2.csv'
#     out = toxPredictionOne(4,base_file_path,0.5)
#     print(out)