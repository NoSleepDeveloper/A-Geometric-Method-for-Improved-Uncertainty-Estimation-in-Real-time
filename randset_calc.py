import numpy as np
import warnings
from utils import *
from calibrators import * 
import pickle
warnings.filterwarnings("ignore")
import torch
import sys
sys.path.append('../')
import time
import copy
from SLURM.sklearn_config import *
from ModelInfo import *
import tensorflow as tf



#random_subset(2-4)
method_name='rand_set'
all_time=[]
for red_param in [2,3,4]:
    for dataset_name in ['Fashion','MNIST','SignLanguage']:
        for model_name in ['RF','GB','pytorch']:
            for shuffle in range(10):
                if model_name=='pytorch':
                    model_info=load_model_pytorch(dataset_name, model_name, shuffle)
                else:
                    model_info= load_model(dataset_name, model_name, shuffle)
                data=model_info.data
                length=model_info.data.X_train.shape[0]
                size=(length//red_param)
                string=np.random.randint(0,length, size=size)
                
                model_info.data.X_train=model_info.data.X_train[string,:]
                model_info.data.y_train=model_info.data.y_train[string]
            
                print(model_info.data.X_train.shape,model_info.data.X_val.shape,model_info.data.X_test.shape)

                num_label=model_info.data.num_labels
                stability,time_all,ex_in_time=new_stability_calc(np.array(model_info.data.X_train),np.array(model_info.data.X_val),model_info.data.y_train,model_info.y_pred_val,num_label)
                stability_test,_,_=new_stability_calc(np.array(model_info.data.X_train),np.array(model_info.data.X_test),model_info.data.y_train,model_info.y_pred_test,num_label)

                all_time.append((model_name,time_all,ex_in_time))
                np.save(f'./stab/{dataset_name}/stab_{method_name}_{red_param}_{dataset_name}_{model_name}_{shuffle}.npy',stability)
                np.save(f'./stab/{dataset_name}/test_stab_{method_name}_{red_param}_{dataset_name}_{model_name}_{shuffle}.npy',stability_test)

all_time