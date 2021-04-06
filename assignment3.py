# -*- coding: utf-8 -*-
"""
Spyder Editor

mohamed sherif
"""
import pandas as pd
import numpy as np
def read_data():
    car_data=pd.read_csv("car.data.csv")
    car_data.columns=["buying_price","maintenance_price","num_of_doors","capacity_of_persons",
                      "size_of_luggage_boot","car_safety","car_acceptability"]
    return car_data 

def divide_data(data):
    training_data=data.sample(frac=.7)
    testing_data=data.drop(training_data.index)
    return training_data,testing_data
def calculate_probability(l,column,labels,data):
    
   c={} 
   for label in labels:
        y=data[data["car_acceptability"]==label]
        
       
        #for i in range(len(columns)-1):#columns ->"buying_price","maintenance_price","num_of_doors","capacity_of_persons",   "size_of_luggage_boot","car_safety"
        d={}   
        for x in l:#l->[med,high,vhigh,low]
            f=y[y[column]==x]
            prob=len(f)/len(y)
            d[x]=prob
            #print(prob)
        c[label]=d     
   return c
def get_unique_values(df):
    unique_values_list=[]
    for col in df:
        u=df[col].unique()
        unique_values_list.append(u)  
    return unique_values_list
def get_item_probabilties(index,item,model_data):
   #columns=model_data.columns 
   #print(columns)
   l=[]
   for x in model_data.iloc[index]:
      l.append(x[item])
   return l  
#calssify row
def calsify_row(c,data,model_data):
    m={}
    columns=model_data.columns
    labels_prob=class_label_prob(data)
    c.append(labels_prob)
    df=pd.DataFrame(c,columns=columns)
    
    for col in columns:
       df_list=list(df[col])
       m[col]=np.prod(df_list)
    maximum=max(m, key=m.get) 
    return maximum

#get accuracy
def get_accuracy(list1):
    list2=pd.read_csv("test_data.csv")
    list2=list(list2["car_acceptability"])
    count=0
    
    for i in range(len(list1)):
        if list1[i]==list2[i]:
            count=count+1
    accuracy=count/len(list1)*100                
    print( accuracy ,'%')
    #print(list1," \n ","--------------",list2)
def testing_model(testing_data,training_data):
      model_data=building_model(training_data)
      columns=testing_data.columns
      new_labels=[]
   #len(testing_data)len(testing_data.iloc[i])
   
      for i in range(len(testing_data)):#loop on each row of testing_data
        c=[]
        for j in range(len(columns)):#loop on each column
             c.append(get_item_probabilties(j,testing_data.iloc[i][j],model_data))
        new_labels.append(calsify_row(c,training_data,model_data)) 
      #testing_data=testing_data['label']=new_labels
      get_accuracy(new_labels)
      
def class_label_prob(data):
    l=[]
    class_label=get_unique_values(data)
    class_label=class_label[6]
    for label in class_label:
        x=data[data["car_acceptability"]==label]
        l.append(len(x)/len(data))
    return l    
def building_model(data):
    n=[]
    columns=data.columns
    index=columns[0:6]
    unique_values=get_unique_values(data)
    labels=unique_values[6]
    for i in range(len(unique_values)-1):
    #for i in range(3):
       column=columns[i]
       n.append((calculate_probability(unique_values[i],column,labels,data)))
    n=pd.DataFrame(n,index=index)
      
      
    n.to_csv("new.csv")
      
        #calculate_probability(unique_values[i],columns,labels,data)
    return n    

car_data=read_data()
training_data,testing_data=divide_data(car_data) 
#save testing data to test_data file
testing_data.to_csv("test_data.csv")
testing_data=testing_data.iloc[:,testing_data.columns != "car_acceptability"]

testing_model(testing_data,training_data)
#print(class_label_prob(training_data))
