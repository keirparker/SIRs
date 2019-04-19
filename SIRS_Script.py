# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 23:22:22 2019

@author: keir9
"""
#absorbing state 0.9 0.08 0
#dynamical state 0.98 0.5 0.98
#waves 0.9 0.08 0.01



#Import
import numpy as np
import sys
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation
from SIRS_Class import SIRS

#Defines global variables: number of iterations to collect data for and user defined dimensions and 3 probabilities
iterations = 1000
dimension = int(sys.argv[1])
p1,p2,p3 = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])

#Animates the simulation of the SIRS model by calling on the SIRS class.
if sys.argv[5] == 'viz':
    
    A = SIRS(dimension,p1,p2,p3)
    #A.Set_Fraction(0.3)
    
    def Animate(*args):
        image.set_array(A.array)
        A.Sweep()
        return image,

    SIRS_Image = plt.figure()
    image = plt.imshow(A.array,animated=True)
    model = FuncAnimation(SIRS_Image,Animate,interval=50,blit=True)
    plt.show()

#Simulates the SIRS model for a range of probabilities of S->I and I->R. Samples data and generates graphs of the average infected fraction/N and the variance in the infected fraction per N.
elif sys.argv[5] == 'phase':
    
    #Creates arrays of probabilities to generate contour plots and creates empty square arrays for avg inf/N and avg var/N. Also lists for the same variables for writing to data file.
    p1_list = np.linspace(p1,1,11,endpoint=True)
    p3_list = np.linspace(p1,1,11,endpoint=True)
    avg_inf_array = np.zeros(shape=(len(p1_list),len(p3_list)))
    avg_var_array = np.zeros(shape=(len(p1_list),len(p3_list)))
    avg_inf_list = []
    inf_var_list = []
    f = open('DataFile.txt','w')
    
    
    #For loops to iterate through probabilities
    for i in range(11):
        for j in range(11):
            
            #Reinitialises an instance of SIRS class to simulate with updated probabilities
            A = SIRS(dimension,i/10.,p2,j/10.)
            print (A.p1,A.p3)
            inf_list=[]
            infsq_list = []
            
            #Performs a predefined number of sweeps for each set of probs
            for t in range(iterations):
                A.Sweep()
                #If sufficient sweeps completed so equilibrium is reached, array is sampled for number of infected cells.
                if t>=100:
                    inf = A.InFraction()
                    inf_list.append(inf)
                    infsq_list.append(inf**2.)
        
            #Calculates the variance and average infected fraction. Writes to data lists.
            var, inf_fraction = A.Variance(inf_list,infsq_list)
            avg_inf_list.append(inf_fraction)
            inf_var_list.append(var)
            
            
            
            #Assigns the calculated values to an index the respective arrays for contour plotting
            avg_inf_array[j,i] = inf_fraction
            avg_var_array[j,i] = var

            #Writes to text file
            f.write("{0:1.2}".format(A.p1)+" " +"{0:1.2}".format(A.p3)+" "+str(inf_fraction)+" "+str(var)+"\n")

    f.close()

    #Generates coloured contour plots
    A.Contour(p1_list,p3_list,avg_inf_array,'Avg Infected Fraction')
    A.Contour(p1_list,p3_list,avg_var_array,'Var per N')
    

#Generates the graph for the average fraction of infected cells vs fraction of immune cells
elif sys.argv[5] == 'immune':
    avg_inf_list = []
    immune_list = []
    cerror1list = []
    xerror1list = []
    f = open('ImmunityFile.txt','w')

    #Iterates through lists of immune fractions
    for i in np.linspace(0,1,110,endpoint=True):
        print(i)
        inf_list = []
        A = SIRS(dimension,p1,p2,p3)
        A.Set_Fraction(i)
        for t in range(iterations):
            A.Sweep()
            if t>= 100:
                inf = A.InFraction()
                inf_list.append(inf)
    
        if inf_list[-1]==0:
            avg_inf_list.append(0)
        else:
            avg_inf_list.append((np.average(inf_list))/A.N)
        immune_list.append(i)
        f.write(str(i)+" "+str(np.average(inf_list))+"\n")
        
        #errors
        #cerror1list.append(np.std(inf_list)/np.sqrt(len(inf_list)))
        #xerror1list.append(np.std())

    #cerror1list = (map(lambda x:x/N,cerror1list))
        
   #-Immune fraction curve. Here again N=10,000 sweeps 
   #(measurements every 10 OK as above); resolution of 0.01 in immune fraction .
   #For this plot only, please add error bars.      
        
    cerrorlist = (np.std(avg_inf_list)/np.sqrt(len(inf_list)))

#   plt.plot(immune_list,avg_inf_list)
    plt.figure()
    plt.errorbar(immune_list,avg_inf_list, yerr = cerrorlist)
    plt.xlabel("Fraction of Permanently Immune Cells")
    plt.ylabel("Average Fraction of Infected Cells")
    plt.title("Plot of the Fraction of Infected cells vs Fraction of Immune cells")
    plt.savefig("Plot of the Fraction of Infected cells vs Fraction of Immune cells")
    plt.show()
