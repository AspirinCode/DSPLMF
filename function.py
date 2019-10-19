# -*- coding: utf-8 -*-
"""
Created on  2018

@author: asus
"""


from __future__ import division
import os
import numpy as np
import pandas as pd
import scipy.stats
import math
from sklearn import metrics
from sklearn.metrics import confusion_matrix, precision_score, recall_score,roc_auc_score
from sklearn import metrics

def score_to_exact_rank(s):
    #s=(-1*s)
    p=np.argsort(s)[::-1]
    #p=np.argsort(s)
    return np.argsort(p)



def load_matrices(folder):
   
        
    with open(os.path.join(folder, "matrix of 0 and 1.txt"), "r") as raw:
        
        observation_mat = [line.strip("\n").split() for line in raw]
        
    with open(os.path.join(folder, "similarity matrix of drugs.txt"), "r") as raw:
        raw.next()
        
        drug_matt = [line.strip("\n").split()[1:] for line in raw]
        
     
    with open(os.path.join(folder, "Liu_similarity_For_drugs.txt"), "r") as raw:
        #raw.next()
        drug_matt_liu = [line.strip("\n").split()[0:] for line in raw]
        
        

    with open(os.path.join(folder, "Similarity matrix based on gene expression profile.txt"), "r") as raw:
        #raw.next()
        cell_sim_1 = [line.strip("\n").split()[0:] for line in raw]
        
    with open(os.path.join(folder, "Similarity matrix based on copy number alteration.txt"), "r") as raw:
        #raw.next()
        cell_sim_2 = [line.strip("\n").split()[0:] for line in raw]
        
        
    with open(os.path.join(folder, "Similarity matrix based on single nucloetid mutation.txt"), "r") as raw:
        #raw.next()
        cell_sim_3 = [line.strip("\n").split()[0:] for line in raw]
        
        
    with open(os.path.join(folder, "Liu_similarity of IC50 values.txt"), "r") as raw:
        #raw.next()
        cell_sim_4 = [line.strip("\n").split()[0:] for line in raw]
        
        
    with open(os.path.join(folder, "Matrix of k-nearest neighbr.txt"), "r") as raw:
        #raw.next()
        cell_sim_new = [line.strip("\n").split()[0:] for line in raw]
        
       
    with open(os.path.join(folder, "matrix of IC50 values.txt"), "r") as raww:
        raww.next()
        print('****************************')
        observation_mat_IC50 = [line.strip("\n").split()[1:] for line in raww]
        
 
    observation_mat = np.array(observation_mat, dtype=np.float64)    
    cell_sim_1 = np.array(cell_sim_1, dtype=np.float64)      
    drug_mat=np.array(drug_matt, dtype=np.float64) 
    drug_matt_liu=np.array(drug_matt_liu, dtype=np.float64)
    cell_sim_2 = np.array(cell_sim_2, dtype=np.float64)
    cell_sim_3 = np.array(cell_sim_3, dtype=np.float64) 
    cell_sim_4 = np.array(cell_sim_4, dtype=np.float64) 
    cell_sim_new=np.array(cell_sim_new, dtype=np.float64)
    
    #train:
    proteins_sim = ((1* cell_sim_1) + (5*cell_sim_4 )+(1* cell_sim_2)+(1* cell_sim_3)) / (8)  #compute weighted average of similarities
   
    proteins_sim_2=cell_sim_new
   
    drug_mat_main=drug_mat
    
    return observation_mat, proteins_sim,proteins_sim_2,observation_mat_IC50,drug_mat_main




def apply_threshold(scores, thre):
    
    prediction = np.zeros_like(scores)
    for i in range(len(scores)):
        threshold = max(scores[i]) - ((max(scores[i]) - min(scores[i])) * (thre))
        for j in range(len(scores[i])):
            if (scores[i][j] <= threshold):
                prediction[i][j] = 0
            else: 
                prediction[i][j] = 1
            
    
    return prediction

def apply_threshold_median(scores):
    count=0
    #print(len(scores[0]))  :98
   # print(len(scores))
    prediction = np.zeros_like(scores)
    for i in range(0, len(scores[0])):
        threshold = np.median ((scores[:,i]))
        print(threshold)
        for j in range(0, len(scores)):
            if scores[j][i] < threshold:
                prediction[j][i] = 0
                
            else: 
                prediction[j][i] = 1
                
   # print(count)
    return prediction
    


def compute_evaluation_criteria(true_result, prediction):
    pres = np.zeros(len(true_result))
    recs = np.zeros(len(true_result))
    ACC=0.0
    ACC_new=0.0
    F1_score_new=0.0
    REC_new=0.0
    Specificity=0.0
    MCC_new=0.0
    AUC_new=0.0
    ddd=0.0
    ccc=0
    cccc=0
    PPP=0.0
    fmeas=[]
    
    
   
    
    #on drugs:
    for i in range(len(true_result[0])):
    
        try:
            AUC_new+=roc_auc_score(true_result[:,i], prediction[:,i])
        except ValueError:
            pass
      
      
       
        returned= confusion_matrix(true_result[:,i], prediction[:,i]).ravel()
       # returned= confusion_matrix(true_result[i], prediction[i]).ravel()
      
        if len(returned) == 4:
            tn, fp, fn, tp = returned
            if (math.isnan(tp)==True):
                tp=0
            if (math.isnan(fp)==True):
                fp=0
            if (math.isnan(tn)==True):
                tn=0
            if (math.isnan(fn)==True):
                fn=0
                
                
        if len(returned) == 1:
           tn= returned
           fp=0
           fn=0
           tp=0
                
       
        ACC_new +=((tp+tn)/ (tp + fp + fn+tn))
        F1_score_new +=((2*tp) / ((2*tp)+fp+ fn))
        PPP=((tp)/(tp+fn))
       
        if (math.isnan(PPP)==True):
                PPP=0
                cccc+=1
        REC_new+=PPP
        
        ddd=(((tp*tn)-(fp*fn))/(np.sqrt((tp+fp)*(tp+fn)*(fp+tn)*(fn+tn))))
        if (math.isnan(ddd)==True):
                ddd=0
                ccc+=1
        MCC_new+=ddd
        
        
        
      
        Specificity+=((tn)/(tn+fp))
       
    ACC = ACC / (len(true_result[0]))
    ACC_new=ACC_new/(len(true_result[0]))
    F1_score_new=F1_score_new/(len(true_result[0]))
    REC_new=REC_new/(len(true_result[0])-cccc)
    Specificity=Specificity/(len(true_result[0]))
    MCC_new= MCC_new/((len(true_result[0]))-ccc)
    AUC_new=AUC_new/(len(true_result[0]))
    
    ###########################################################################

    for i in range(0, len(true_result[0])):
     
        recall = 0
        precision = 0
        r_loc = 0
        p_loc = 0
        for j in range(0, len(true_result)):
            if true_result[j][i] == 1:
                recall += recs[j]
                r_loc += 1
            if prediction[j][i] == 1:
                precision += pres[j]
                p_loc += 1
        if r_loc != 0:
            recall = recall / r_loc
        else:
            recall = 0
        if p_loc != 0:
            precision = precision / p_loc
        else:
            precision = 0
        if (precision == 0 and recall == 0):
            fmeas.append(0)
        else:
            fmeas.append(round((2 * recall * precision) / (precision + recall), 4))
    finalF = np.mean(fmeas)
    return round(finalF,2), round(ACC,2),round(ACC_new,2),round(F1_score_new,2),round(REC_new,2),round(Specificity,2),round(MCC_new,2),round(AUC_new,2), fmeas




def compute_evaluation_criteria_across_wholeMatrix(true_result, prediction,scores):
    pres = np.zeros(len(true_result))
    recs = np.zeros(len(true_result))
    ACC=0.0
    ACC_new=0.0
    F1_score_new=0.0
    REC_new=0.0
    Specificity=0.0
    MCC_new=0.0
    AUC_new=0.0
    AUC_neww=0.0
    AUC_new_new=0.0
    precision_new=0.0
    co=0.0
    tp_final=0
    tn_final=0
    fp_final=0
    fn_final=0
    fmeas=[]
    true_auc=[]
    score_auc=[]
    
    
    for i in range(len(true_result[0])):
        
        
        fpr, tpr, thresholds = metrics.roc_curve(true_result[:,i], scores[:,i], pos_label=1)
       
        
        if (math.isnan(metrics.auc(fpr, tpr))!=True):
            co=co+1
            AUC_new_new+= metrics.auc(fpr, tpr)
       
        #print('AUC_new_new',AUC_new_new)
        true_auc.append(true_result[:,i])
        score_auc.append(scores[:,i])
        
        
        
       
        
        returned= confusion_matrix(true_result[:,i], prediction[:,i]).ravel()
        if len(returned) == 4:
            tn, fp, fn, tp = returned
            
        if len(returned) == 1:
           tn= returned
           fp=0
           fn=0
           tp=0
        
        tp_final+=tp
        tn_final+=tn
        fp_final+=fp
        fn_final+=fn
        
   
    ACC = (tp_final / (tp_final + fp_final + fn_final))   
    ACC_new =((tp_final+tn_final)/ (tp_final + fp_final + fn_final+tn_final))
    F1_score_new =((2*tp_final) / ((2*tp_final)+fp_final+ fn_final))
    REC_new=((tp_final)/(tp_final+fn_final))
       # REC_new+=((tp)/(tp+fn))
    precision_new=((tp_final)/(tp_final+fp_final))
   
        
    MCC_new=(((tp_final*tn_final)-(fp_final*fn_final))/(np.sqrt((tp_final+fp_final)*(tp_final+fn_final)*(fp_final+tn_final)*(fn_final+tn_final))))
    
  
        
       # print('fdfdfdfd',MCC_new)
       #print('REC_new' , REC_new)
    Specificity=((tn_final)/(tn_final+fp_final))
    
  
    AA=[]
    for thre in np.arange(0.1,1.0,0.1):
       for i in range(len(true_result[0])):
           prediction = apply_threshold(scores, thre)
           try:
               AUC_new+=roc_auc_score(true_result[:,i], prediction[:,i])
           except ValueError:
               pass
    
       AUC_new=AUC_new/(len(true_result[0]))
       AA.append(AUC_new)
       #print(AA)
      #
    AUC_neww=np.mean(AA)
       
   
    AUC_new_new=AUC_new_new/(co)
    for i in range(0, len(true_result[0])):
      #  print('len(true_result)', len(true_result[0]))
        recall = 0
        precision = 0
        r_loc = 0
        p_loc = 0
        for j in range(0, len(true_result)):
            if true_result[j][i] == 1:
                recall += recs[j]
                r_loc += 1
            if prediction[j][i] == 1:
                precision += pres[j]
                p_loc += 1
        if r_loc != 0:
            recall = recall / r_loc
        else:
            recall = 0
        if p_loc != 0:
            precision = precision / p_loc
        else:
            precision = 0
        if (precision == 0 and recall == 0):
            fmeas.append(0)
        else:
            fmeas.append(round((2 * recall * precision) / (precision + recall), 4))
    finalF = np.mean(fmeas)
  #  print('fffffffffffffffffffffffffff',co)
    return round(precision_new,2),round(finalF,2), round(ACC,2),round(ACC_new,2),round(F1_score_new,2),round(REC_new,2),round(Specificity,2),round(MCC_new,2),round(AUC_neww,2),round(AUC_new_new,2), fmeas


    
    
    
    

def pearson_correlation(list1,list2):
     return np.corrcoef(list1, list2)[0, 1]


def spearman_correlation(xs,ys):
    
    xranks = pd.Series(xs).rank()
    
    # Caclulate the ranking of the y's
    yranks = pd.Series(ys).rank()
    
  
    
    return pearson_correlation(xranks,yranks)
    
    
   
      
    
    
def pearson_correlation_acros_cell_lines(R,pred):
    all_corr=[]
    
    for u in range(len(R)):
        
        
        s_u = R[u]
        s_u=np.array(s_u)
        s_u_float=s_u.astype(np.float)
        s_u_pred = pred[u,:]
       
        
        
        total=pearson_correlation(s_u_float,s_u_pred)
       # print('total',total)
        
        all_corr.append(total)
    return np.mean(all_corr)


def pearson_correlation_acros_drugs(R,pred):
    
    all_corr=[]
    for u in range(len(R)):
        #s_u = R[u]
        R[u]=np.array(R[u])
    
    R = R.transpose()
    pred=pred.transpose()
    
    for u in range(len(R)):
        #print(u)
        s_u = R[u]
        s_u=np.array(s_u)
        s_u_float=s_u.astype(np.float)
        
        s_u_pred = pred[u,:]
        
        total=pearson_correlation(s_u_float,s_u_pred)
        
       
        all_corr.append(total)
    return np.mean(all_corr)

def spearman_correlation_acros_cell_lines(R,pred):
    all_corr=[]
    
    for u in range(len(R)):
        
        s_u = R[u]
        s_u=np.array(s_u)
        s_u_float=s_u.astype(np.float)
        s_u_pred = pred[u,:]
        #print(s_u_float)
        
       
        total=spearman_correlation(s_u_float,s_u_pred)
       # print(s_u_float)
        #print('**********************************')
        #print(s_u_pred)
    
        
       
        all_corr.append(total)
    return np.mean(all_corr)


def spearman_correlation_acros_drugs(R,pred):
    all_corr=[]
    for u in range(len(R)):
        #s_u = R[u]
        R[u]=np.array(R[u])
        
    R = R.transpose()
    pred=pred.transpose()
    
    for u in range(len(R)):
       # print(u)
        s_u = R[u]
        s_u_float=s_u.astype(np.float)
        
        s_u_pred = pred[u,:]
        
        
        total=spearman_correlation(s_u_float,s_u_pred)
        
       
        all_corr.append(total)
    return np.mean(all_corr)

