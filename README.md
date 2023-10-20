Intermediate IT Challenge Patents

#Solution
The challenge was carried out according to the instructions in the statement. Take into account the following considerations.

-In order to generalize, originalNames.json has been stored in the Data folder. So that the list of original names can be changed at any time.

-The functions.py file only has functions and does not require execution.

-The dataExploring.py file generates an initial inspection of the data that allows the solution approach to be validated or not. Character clouds and word clouds are generated as a visual reference that is helpful when generating the basic cleaning indicated in the statement. It also returns information about whether exact matches exist with the original names, what percentage of the data set, and how many classes are present. The output of this script is stored with the "-exploration" tag, in pdf format.

-The nameCleaner.py file runs an initial basic cleanup stage, then performs labeling of the calculated data on exact matches, for this case it is more than 99% of data labeled due to exact match. With these labels, a Support Vector Machine algorithm is trained, which allows taking into account additional country and city information, as well as the similarity with respect to the "official" names. The output of this file generates a file labeled "-fixed", with the name column normalized.


# Performance and design considerations

-A proper assignment of the corrected name could be verified by doing a random inspection of the corrected data column ("fixed" column). SVM performs well with high dimensionality, making it suitable for this approach, mainly after applying OneHoteEncoding to the 'country' and 'city' features.

-The data exploration pdf can help identify situations where the solution approach may not be the best option, cases such as the following:

-A great class imbalance.

-Zero matches in the data set with any category of "original" names.

-It is necessary to modify originalNames.json in case it is necessary to apply a new solution with a set of different original names.
-As indicated in the statement, it is considered that a company's own abbreviations correspond to those that were in the particular set of data. In the same way, they were acquired with regular expression and are detailed in the pdf of the data exploration.

-By using SVM, the dependence only on orthographic similarity is eliminated and the country and city fields are also allowed to be taken into account for the assignment of the corrected name.

# Opportunities for improvement to solution

 -Find different methods of inference from the original names without them being explicitly indicated. (The degree of uncertainty increases considerably).
 
-Establish validations that raise alarm when the code is executed on a data set that violates the main considerations when executing the SVM-based solution. For example:
        -Class imbalance.
        -Absence of class in original data set, even after basic cleaning.

- Consider validations for defective files or files with a different structure.

-Robust against possible new locations for company names, so that orthographic similarity is also taken advantage of even if there are no examples of the country-city-company combination in the data set.

# About the use of scripts
-It is necessary to run either of the two scripts (namesCleaner.py and dataExploring.py) from the console.

-The output file will be saved in the same location as the input file. In both cases there will be a label that differentiates it from the official file: "-fixed" and "-exploration".

    PythonExploring.py data Data/data.csv