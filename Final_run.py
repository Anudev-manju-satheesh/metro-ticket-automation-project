#!/usr/bin/env python
# coding: utf-8

# ## Please read the attached pdf document and the limitations of this program before proceeding further.

# ### 1. Importing the necessary packages to run the whole program
# Using open cv for image capture. Keras and tensorflow to load the model that was trained on google colab.
# 

# In[1]:


import numpy as np
import pandas as pd
import cv2 as cv
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import os
from tensorflow import keras
import tensorflow as tf
from datetime import datetime
from time import sleep


# ### 2. Loading the pretrained model
# The model was trained using google colab (Tesla T4 GPU). Further details of model training are provided in the model training ipynb file and a clear function to clear the screen.

# In[2]:


mod = tf.keras.models.load_model('currency_det.H5')


# In[5]:


clear = lambda: os.system('cls')


# ### 3. System initialization
# This cell below will ask the input while initializing the system. The number of transactions expected per day should be given while initialization. So that the whole program will loop that many times meaning if 5 is given as input, we can get 5 tickets. After the 5 tickets are taken the program will be terminated.

# In[6]:


print("SYSTEM INITIALIZATION")
daily_rep = int(input("Enter the expected number of Transactions for the day: "))
clear()


# ### 4. Station details
# This code block defines the current station. I have opted the JLN Stadium station since it is on of the middle station of the whole metro rail. The further information on stations and charges were fetched from https://kochimetro.org/ .

# In[7]:


current_station = 'JLN Stadium'
stations = ['Aluva','Pulinchodu','Companypady','Ambattukavu','Muttom','Kalamassery','Cochin University',
            'Pathadipalam','Edapally','Changampuzha Park','Palarivattom','Kaloor','Town hall','MG Road',
            'Maharaja’s College','Ernakulam South','Kadavanthra','Elamkulam','Vyttila','Thaikoodam']
charges = [40,40,40,40,30,30,30,20,20,20,10,10,20,20,20,30,30,30,40,40]


# ### 5. Ticket function
# The purpose of this function is to generate the ticket after every other parameters are provided.

# In[8]:


def ticket(a): 
    print('-'*40)
    print("          TICKET           ")
    print("Time :"+str(c_time))
    print("Date :"+str(c_date))
    print("From :"+str(current_station))
    print('To   :'+str(station))
    print("charge is: Rs "+str(a))
    print("Platform number is :"+ str(plat))
    print('-'*40)
    print(''*20)


# ### 6. Introduction screen
# This will be introduction screen for the customers where the customer have to give the station numeber as the input and the program will display the fair and the platform.

# In[9]:


def user_inp1():
    print("*********WELCOME TO KOCHI METRO*********")
    print("You are at "+current_station)
    print("Selet your destination: ")
    print('-'*20)
    for i in range(len(stations)):
        print(str(i+1) + ' : '+ stations[i] )
    print('-'*20)
    a = int(input('Enter the destination number: '))
    global plat
    plat = ''
    if a > 12:
        plat = " 2 (towards Pettah)"
    else:
        plat = '1 (towards Aluva)'
    global charge
    global station
    charge = charges[a-1]
    station = stations[a-1]
    print('*'*30)
    print('Selected destination is '+ stations[a-1]+' Fare is Rs: '+ str(charges[a-1]))


# ### 7. Currency input
# The program will ask the number of notes the user is going to input

# In[10]:


def user_inp2():
    global notes
    print('-'*30)
    notes = int(input("Please enter the number of notes:"))
    print('-'*30)
    print("Place the money at the slot")


# ### 8. Image capture
# This function opens up the camera of the device or the registered camera. In real case scenario these functions will be happening inside the machine. Since this is only just the code the notes have to be shown infornt of the camera one by one. 1st note should be shown and spacebar should be pressed to capture the image. If number of notes is more than 1 then other notes also have to be shown infront of the camera and spacebar should be pressed. The number of frames that can be captured is only equal to the user input of "number of notes".

# file path have to be detemined by the admin before running the program and have to be changed accordingly.
# 

# In[12]:


def user_inp3():
    cam = cv.VideoCapture(0)
    count = 0
    while True:
        ret,img = cam.read()
        cv.imshow("Test",img)
        if not ret:
            break
        k=cv.waitKey(1)

        if k%256==27:
            print('Closed')
            break
        if k%256==32:
#             print('image '+str(count)+' saved')
            file = r'D:\AI ML DL\Metro ticket project\Kochi metro ticket\my_test\img'+str(count)+'.jpg'
            cv.imwrite(file,img)
            if count<notes-1:
                count +=1
            else:
                break
    cam.release()
    cv.destroyAllWindows()


# ### 9. Using the model to calculate the input money by user
# This function will use the trained model to predict the user input notes and finds the total amount of money input by the user.

# Image path also have to be changed by the admin accordingly to the system.

# In[13]:


def user_inp4():
    tot_money = []
    for i in range(notes):
        img_path = r'D:\AI ML DL\Metro ticket project\Kochi metro ticket\my_test\img'+str(i)+'.jpg'
        img = image.load_img(img_path, target_size=(224, 224))
#         plt.imshow(img)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x/255.0
#         print('Input image shape:', x.shape)
        a = mod.predict(x)
        pred = []
        for i in a[0]:
          pred.append(i)
#         print(pred)
        op = [10,100,20,200,2000,50,500,'background']
        b = pred.index(max(pred))
        global c
        c = op[b]
        if os.path.exists(img_path):
            os.remove(img_path)
#             print('file removed')
        else:
            print('file does not exist')
            
        if c=='background':
            print("No amount detected please try from beginning")
            break
        else:
            tot_money.append(c)
#     print(tot_money)
    global s_total
    s_total = sum(tot_money)


# ### 10. Using datetime module
# This functiom helps to capture the live date and time. This is used while printing the ticket.

# In[14]:


def dtime():
    time = datetime.now()
    global c_time
    global c_date
    c_time = time.strftime('%H:%M:%S')
    c_date = time.strftime('%d/%m/%y')


# ### 11. User output function
# This function is used to give the user output that is the ticket. If the user provided the correct money it will print the tickt or extra money was provided then the balance amount will be shown. And the charges will be appended to the total_collection list. If the money provided is less than the charge the system provides an error message to put the correct money.

# In[15]:


total_collection = []
def op():
    if charge== s_total:
        ticket(s_total)
        total_collection.append(charge)
    elif charge>s_total:
        print('x'*20)
        print("Please provide the correct money.")
    else:
        print('*'*20)
        print("Your balance is Rs: "+str(s_total-charge))
        print('*'*20)
        total_collection.append(charge)
        ticket(charge)


# ### 12. Final function
# This is the for loop where evry function in this program is called. This will loop for the input of system initializer. After every customer ticket will be shown for 15 seconds and then will move on to next customer. If in case the program has to be stopped before the given iteration at the input a password can be set which is known by only admin staffs (in this program its "quit1234"). And they can use this to terminate the run. Pressing any other key will result in continuation of the program.

# In[16]:


for i in range(daily_rep):
    x = input("Press any key to continue :")
    if x== "quit1234":
        break
    else:
        user_inp1()
        user_inp2()
        user_inp3()
        user_inp4()
        dtime()
        op()
        sleep(15)
        clear()


# ### 13. Final collection 
# In the real case scenario after every day the system should save the overall amount it has recieved. This is done with the help of appending charge of every customer to the total_collection list. After looping "daily_rep" number of times the total amount collected for the day will be shown on the screen.

# In[17]:


print("Total money collected for the day is:"+str(sum(total_collection)))

