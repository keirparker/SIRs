# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 19:57:42 2019

@author: keir9
"""
#Import
import numpy as np
import matplotlib.pylab as plt
from collections import Counter
import sys
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation
#from GOL_Class import GO

#Class containing methods for simulating the Game of Life
class GOL(object):

#Initialises an instance based on user defined arguments. Square array of size dimension and initial conditions
    def __init__(self,dimension,initial):
        self.dimension = dimension
        self.N = dimension**2.
        self.initial = initial
        
        #If random initial condition then array randomly filled with live and dead cells
        if initial == 'random':
            self.array = np.random.choice([-1,1],size=(dimension,dimension))
        
        elif initial == 'absorbing':
            index1 = int((np.random.uniform()*dimension))
            index2 = int((np.random.uniform()*dimension))
            self.array = np.full((dimension,dimension),-1)
            self.array[index1,index2] = 1
        
        #If blinker condition is selected then randomly creates an oscillator
        elif initial == 'blinker':
            self.array = np.full((dimension,dimension),-1)
            blink1 = int((np.random.uniform())*dimension)
            blink2 = int((np.random.uniform())*dimension)
            for i in range(3):
                blink1 += 1
                if blink1 >= dimension:
                    blink1 = 0
                self.array[blink2,blink1] = 1
    
        #Randomly creates a moving glider if user selects.
        elif initial == 'glider':
            self.array = np.full((dimension,dimension),-1)
            #g1 = int(np.random.uniform()*(dimension-1))
            #g2 = int(np.random.uniform()*(dimension-1))
            g1 = 1
            g2 = 1
            
            self.array[g1-1,g2] = 1
            self.array[g1+1,g2] = 1
            self.array[g1,g2+1] = 1
            self.array[g1+1,g2+1] = 1
            self.array[g1+1,g2-1] = 1
            
        else: print("No such initial condition installed. Enter either 'random', 'blinker', 'glider'")

    #Instance method which returns the 8 nns of a given index while employing periodic boundary conditions
    def NNs(self,i,j):
        max = self.dimension-1
        iup = (i+1)%self.dimension
        idown = (i-1)%self.dimension
        jup = (j+1)%self.dimension
        jdown = (j-1)%self.dimension
        
        nn1 = self.array[idown,j]
        nn2 = self.array[idown,jup]
        nn3 = self.array[i,jup]
        nn4 = self.array[iup,jup]
        nn5 = self.array[iup,j]
        nn6 = self.array[iup,jdown]
        nn7 = self.array[i,jdown]
        nn8 = self.array[idown,jdown]
        
        return [nn1,nn2,nn3,nn4,nn5,nn6,nn7,nn8]
    
    #Algorithm containing the rules for the GOL and imposes them on a given index. An 'alive' cell(1) will 'die' (-1) if it has less than 2 or greater than 3 'alive' neighbours. A 'dead' cell will come alive if it has 3 'alive' neighbours.
    def Rules(self,i,j):
        nn_list = self.NNs(i,j)
        c = Counter(nn_list)
        
        if self.array[i,j] == 1:
            if c[1]==2 or c[1]==3:
                return 1
            else: return -1

        elif self.array[i,j] == -1 and c[1]==3: return 1
        else: return -1

    #Instance method which sweeps the entire array sequentially and then updates all in parallel
    def Sweep(self):
        temp_latt = np.copy(self.array)
        for i in range(self.dimension):
            for j in range(self.dimension):
                value = self.Rules(i,j)
                temp_latt[i,j] = value
        self.array = np.array(temp_latt)

    #Instance method which finds the Center of Mass of the live cells in the array. Returns the index of the CoM
    def CoM(self):
        coors = np.argwhere(self.array==1)
        xcom = int(np.average(coors[:,0]))
        ycom = int(np.average(coors[:,1]))
        return [xcom,ycom]

    #Static method which takes as arguments a list of time and position and returns the velocity using numpy linear regression.
    @staticmethod
    def Glider_Velocity(time,position):
        coeffs = np.polyfit(time,position,1)
        return coeffs[0]


#Create an instance of GOL
A = GOL(int(sys.argv[1]),str(sys.argv[2]))

#Animates the simulation of GOL if user selects
if sys.argv[3]=='viz':

    #Update plot function which sweeps the array and simulates the GOL
    def UpdatePlot(*args):
        image.set_array(A.array)
        A.Sweep()
        return image,

    #Animating the simulation. plt.imshow creates much faster moving animations so it is used here.
    GLImage = plt.figure()
    image = plt.imshow(A.array,animated=True)
    model = FuncAnimation(GLImage,UpdatePlot,interval=10,blit=True)
    plt.show()

#If user selects, simulates GOL for 200 Sweeps and calculates the velocity of the glider. NOTE: only works if initial condition is "glider"
elif sys.argv[3]=='data':
    t = 0
    tlist = []
    positionlist = []
    #Function to calculate absolute distance
    sq_dist = lambda x,y: np.sqrt(x**2. + y**2.)
    
    #Sweeps for 200 iterations and calculates COM
    for i in range(1000):
        A.Sweep()
        CoM = A.CoM()
        #If the COM of the glider is not near the boundaries, the time value and position are appended to lists
        if 3<CoM[0]<(A.dimension-3) and 3<CoM[1]<(A.dimension-3):
            t+=1
            if t%200==0:
                t = 0
            tlist.append(t)
            positionlist.append(sq_dist(CoM[0],CoM[1]))
            
    #Calculates the velocity of the glider
    vel = A.Glider_Velocity(tlist[0:170],positionlist[0:170])
    print("The velocity of the glider is: {0:1.3f}".format(vel)+" indices/timestep")


    #Plots the position of the glider vs timestep.
    plt.plot(tlist[0:170],positionlist[0:170],'r:')
    plt.xlabel("Time (timesteps)")
    plt.ylabel("X Position in Array")
    plt.title("Plot of the X position of a Glider vs Timesteps")
    plt.text(2, 50., "The velocity of the glider\n is: {0:1.3f}".format(vel)+" indices/timestep", family="monospace")
    plt.savefig("Plot of the X position of a Glider vs Timesteps")
    plt.show()


