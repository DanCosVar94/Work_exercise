# Work_exercise

This script contains a class type generated for this exercise. This script imports an object type API_ree with three own methods (get_array, get_API, plot_results).
To start the object, it is necessary to enter 3 parameters: ID (integer), date (list of dates in ISO8601) and granularity (integer=0,1,2).

At its initialization, the class applies a query API to the self.url defined for downloading data in json, for the ID indicator.
If you want to calculate the matrix, it is necessary to execute the method get_array.This will apply a Fast Fourier Transform normalized
to the date display period. Once its is calculated, you can plot the result with plot_results() function. 

E.g COMMANDS :

AiguaSol = API_ree(1293,["2020-10-02T00:00:00+02:00","2020-10-06T23:59:59+02:00"],1,debug=True)
AiguaSol.get_arrays()
AiguaSol.plot_results()
