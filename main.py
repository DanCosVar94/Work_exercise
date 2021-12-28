#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Lib. to calculations
from scipy.fft import fft
from scipy.fft import fftfreq
from scipy.fft import fftshift
#Lib. to plot
import matplotlib.pyplot as plt
#Lib.
from datetime import datetime
import requests
import numpy as np

class API_ree:


    def __init__(self,ID,date,granularity,debug=False):
        """
        :param ID: int / signal
        :param date: list / [from,to] ISO 8601
        :param granularity: int / 0: 10 minutes, 1: hour, 2: day, 3:month
        """
        ##INI properties
        #Debug mode
        self.debug= debug

        #Set properties ID , Date and granularity
        self.signal_ID = ID
        self.date = date
        self.int_granularity= granularity

        #Set list_granularity
        self.list_granularity= ['minute','hour','month']
        #Set URL to API data webpage
        self.url = "https://api.esios.ree.es/indicators/"
        #Set my token
        self.mytoken= "5fb771910c10cfb84dd668843db610dd0bf832c83b9e2546e6295a2886f5f7c6"

        #GET API from ID indicator---<
        self.API_response= self.get_API()

        #Non calculation performed
        self.calculated = False

    def get_API(self):
       """
       :param self: nothing
       :return: json of data self.date/ID/granurality
       """
       if self.debug: print("get_API Initialitzation...")

       #Set header to GET indicator data
       headers = {'Content-Type': 'application/json', 'Accept': 'application/json',\
                  'Authorization': "Token token=" + self.mytoken, 'Content-Type': 'application/json',
                  'Host': 'api.esios.ree.es'}
       #Conditions
       load = {'start_date': self.date[0], 'end_date': self.date[1],'geo_agg':'sum','locale':'es'}
       #Set granularity
       if self.int_granularity > 0 :
            load['time_trunc'] = self.list_granularity[self.int_granularity]
            load['time_agg']='avg'
       #GET URL data
       response= requests.get(self.url+str(self.signal_ID), params=load,headers=headers)

       #Print info in debug mode
       if self.debug:
           print("API GET Response status: ",response.status_code)
           print(response.request.url)
           print("Properties: ",self.signal_ID,self.date)

       if self.debug: print("get_API Finished...")

       return response

    def get_arrays(self):
        """
        :sets: sets arrays signal, time, signal_fft and signal_freq
        """
        if self.debug: print("get_arrays Initialitzation...")

        #Check if API respones is OK.
        if self.API_response.ok:
            #Transform data to json
            self.data_API = self.API_response.json()

            #Get data signal
            self.signal = np.array([element['value'] for element in self.data_API['indicator']['values']])


            #Get data time
            self.time = np.array([datetime.strptime(element['datetime'],"%Y-%m-%dT%H:%M:%S.%f%z") for element in self.data_API['indicator']['values']])


            #Calcualte Fast Fourier Transf. and freq. normalized
            self.signal_fft = fft(self.signal)/len(self.time)
            self.signal_freq = fftfreq(len(self.signal),1/len(self.time))


            #Set calculated in True
            self.calculated = True
            if self.debug: print("Arrays calculated...")

        else:
            # Set calculated in False
            self.calculated = False
            if self.debug: print("Arrays not calculated...")


        if self.debug: print("get_arrays Finished...")

    def plot_results(self):
        if self.debug: print("print_results Initialitzation...")

        if self.calculated:
            # Initialise the subplot function using number of rows=2
            figure, axis = plt.subplots(2)

            #Original domain (time)
            axis[0].plot(self.time, self.signal,color="red",)

            # Sets title axis[0]
            axis[0].set_title("Time domain")
            axis[0].set_xlabel('[date]')
            axis[0].set_ylabel('Real Power Demand [MW]')
            axis[0].grid()

            #Freq. domain
            # Only uses the positive domain due to its symmetry = [:len(self) // 2]
            axis[1].plot(self.signal_freq[:len(self.signal_freq)//2], abs(self.signal_fft.imag[0:len(self.signal)//2]))
            axis[1].set_title("Freq. domain")
            axis[1].set_xlabel('[Hz]')
            axis[1].set_ylabel('Amplitude [MW]')
            axis[1].grid()

            plt.show()

        else:
            if self.debug: print("No data to plot")

        if self.debug: print("print_results finished...")



if __name__ == '__main__':

    AiguaSol = API_ree(1293,["2020-10-02T00:00:00+02:00","2020-10-06T23:59:59+02:00"],1,debug=True)
    AiguaSol.get_arrays()
    AiguaSol.plot_results()





