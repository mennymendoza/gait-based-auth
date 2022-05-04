import numpy as np
import pandas as pd

"""
    The way this funcion will run is to pull in a dataframe for each user based on a given list of title sequences
    similar to feature.py it will then authenticate a user and run an authentification test on all other users in the list, logging
    the bool value for each. It will then create a ratio of correct/incorrect readings. It will then increase the tolerance
    and decrease the tolerance by a given N value then run the processes again and compare the different from the increase and decrease
    to the orignal value, we are looking for a better ratio. This process will be repeated until an ideal ratio is reached
"""



def authentification(user,tolerance):
    #run auth process   
    return True 
def tolerancefinder(userlist,tolerance,changeval):
    trues=0
    falses=0
    for i in userlist:
        if authentification(userlist[i],tolerance) == True:
            trues+=1
        else:
            falses+=1
    ratio = trues/falses
    return ratio

def main(file,tol,c):
    tolerancefinder(users,usertol,change)


