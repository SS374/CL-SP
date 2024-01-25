# Datasets to test out, with their intended prediction
#datasets = [[37, 37, 37, 38, 38, 38, 38, 37, 37, 37, 36, 36, 36, 37, 38, 40, 42, 44, 45, 45, 44, 43, 42, 41] ] # Schnectady Hourly forecast on 1/24/24 || For forecasting
#datasets = [[40], [42],[44],[46]] # Example data || For linear prediction || Target of 48
#datasets = [[31,38],[36,45],[36,43]] # Highs and lows from 1/24/24 to 1/26/24 || For non-linear prediciton || Target of 35,41 
datasets = [[1], [1], [2], [3], [5], [8], [13], [21]] # FIBONACCI SEQUENCE || For non-linear prediction || Target of 34
#datasets = [[1],[2],[4],[7]] # LAZY CATERER'S SEQUENCE || For non-linear prediction || Target of 11

# Simple base functions
def findavg(values):
    total = 0
    for value in values:
        total += value
    return total / len(values)

def findhigh(values):
    high = values[0]
    for value in values:
        if high < value:
            high = value
    return high

def findlow(values):
    low = values[0]
    for value in values:
        if low > value:
            low = value
    return low

def findmedian(values):
    if len(values) % 2 == 0:
        return (values[len(values) // 2] + values[len(values) // 2 - 1]) / 2
    else:
        return values[len(values) // 2]

# Finds general dataset trend in multiple datasets
def findtrend(datasets):
    oldavg = findavg(datasets[0])
    switches = 0 # Keeps track of when the trend changes
    trend = None

    for dataset in datasets:
        newavg = findavg(dataset) # Based on the dataset's average
        if newavg > oldavg:
            if trend == "Temperature is decreasing":
                switches += 1
            trend = "Temperature is increasing"
        if newavg < oldavg:
            if trend == "Temperature is increasing":
                switches += 1
            trend = "Temperature is decreasing"
        if newavg == oldavg:
            if trend == None:
                trend = "Temperature remains the same"

        oldavg = newavg

    
    if switches > 2: # Unable to return trend if trend is inconsitent
        trend = "Too much variation in temperaure to find a trend"
    elif switches != 0:
        # Finds net trend
        if findavg(datasets[-1]) > findavg(datasets[0]): 
            nettrend = "is increasing"

        if findavg(datasets[-1]) <= findavg(datasets[0]):
            nettrend = "is decreasing"

        trend = "Temperature has ups and downs but overall " + nettrend

    return trend

# Predicts next dataset based on current datasets
# Limitations: Only checks last 3 datasets, no other information other than values provided in datasets, cannot indentify peaks and valleys in temperature
def predict(datasets):
    last_dataset = datasets[-1] # Last dataset 
    secondtl_dataset = datasets[-2] # Second to last dataset
    thirdtl_dataset = datasets[-3] # Third to last dataset
    predictionlist = [None for x in range(len(last_dataset))] # Placeholer list for prediction dataset
    trend = findtrend(datasets)

    if "same" in trend: # If all previous data was identical, assume prediction will be identical
        return (
            "["
            + "".join(str(x) for x in last_dataset)
            + "] "
            + "\nWith confidence of: Absolutely Certain"
        )

    elif "increasing" in trend or "decreasing" in trend:
        deviances = [] # Stores deviances for different index locations
        weightedPercentages = [] # Stores deviance percentage for different index locations
        for i in range(len(last_dataset)): # Looks at each index of datasets, only uses values at the same index location to form prediction
            larger = last_dataset[i]
            smaller1 = secondtl_dataset[i]
            smaller2 = thirdtl_dataset[i]
            difference1 = abs(larger - smaller1)
            difference2 = abs(smaller1 - smaller2)
            factor = larger / smaller1
            factor2 = smaller1 / smaller2

            # Converts factor into a percentage 
            if factor > 1 and factor2 < 1: 
                factor = 2 - factor
            elif factor < 1 and factor2 > 1:
                factor2 = 2 - factor2

            if difference1 == difference2: # Finds if differences between past datasets was linear
                predictionlist[i] = larger + difference1 # Applies linear difference
                deviance = 0
                weightedPercentage = 0
            else:
                predictionlist[i] = round(larger * factor) # Applies non-linear difference
                deviance = abs(round((larger * factor - larger * (factor + factor2)/2))) # Finds predicted potential deviance from the prediction 
                weightedPercentage = deviance/(larger*factor) # Finds the percentage off the deviance is from the prediction
            deviances.append(deviance)
            weightedPercentages.append(weightedPercentage)
    else:
        return "Too much variation to predict"
    
    # Sets deviance and weighted percentages to the highest value for confidence calculation
    deviance = findhigh(deviances)
    weightedPercentages = findhigh(weightedPercentages)

    # Finds confidence in prediction based on deviance or deviance percentage
    if deviance == 0 or weightedPercentage == 0:
        confidence = "Absolutely Certain"
    elif deviance > 0 and deviance <= 1 or weightedPercentage > 0 and weightedPercentage <= 10 :
        confidence = "High"
    elif deviance > 1 and deviance <= 4 or weightedPercentage > 10 and weightedPercentage <= 20:
        confidence = "Moderate"
    elif deviance > 4 and deviance <= 6 or weightedPercentage > 20 and weightedPercentage <= 30:
        confidence = "Moderately Low"
    elif deviance > 6 and deviance <= 7 or weightedPercentage > 30 and weightedPercentage <= 50:
        confidence = "Low"
    else:
        confidence = "Extremely low"

    return (
        "["
        + ", ".join(str(x) for x in predictionlist)
        + "] "
        + "\nWith confidence of: "
        + confidence
        + "\nWith deviances of: "
        + aligndeviances(deviances, predictionlist)
    )

def aligndeviances(deviances, dataset):
    output = ""
    for i in range(len(deviances)):
        output += str(dataset[i]) + " +/- " + str(deviances[i]) + "  "
    return output

# Utilizes basic functions to create a weather forcast
def forecast(dataset):
    print(
        "Highs of",
        findhigh(dataset),
        "degrees\nLows of",
        findlow(dataset),
        "degrees \nAverage temperatures around",
        round(findavg(dataset)),
        "degrees\nMedian temperature is",
        float(findmedian(dataset)),
        "degrees",
    )
    input("Enter key to return to home: ")

# Home screen and user flow control
def homescreen():
    global datasets

    print("\n" * 100)
    printasdays(datasets)
    userchoice = input(
        "Options: \n'C' to create new day\n'X' to clear days\n'F' to forecast a day\n'A' to analyze all days\n'E' to exit the model: "
    )
    if userchoice == "C":
        print("\n" * 100)
        if len(datasets) == 0:
            while True:
                try:
                    values = int(
                        input(
                            "How many values are in your days? \n(This will be constant across all days): "
                        )
                    )
                    break
                except ValueError:
                    print("Value is not an integer")
        else:
            values = len(datasets[0])
        datasets.append(createnewdataset(datasets, values))
    if userchoice == "X":
        print("\n" * 100)
        datasets = []
    if userchoice == "F" and len(datasets) > 0:
        print("\n" * 100)
        printasdays(datasets)
        while True:
            try:
                forecast(
                    datasets[int(input("Which day would you like to forecast? ")) - 1]
                )
                break
            except ValueError:
                print("Value is not an integer")
            except IndexError:
                print("Dataset at such location doesn't exsist")
    if userchoice == "A" and len(datasets) >= 3:
        print("\n" * 100)
        printasdays(datasets)
        print(
            "\nUsing data from all days, the trend is: \n"
            + findtrend(datasets)
            + "\n\nThe model predicts the next day to be: "
        )
        print(predict(datasets), "\n")
        input("Enter key to return to home: ")
    if userchoice != "E":
        homescreen()
    else:
        return

# Prints datasets as days (more readable)
def printasdays(datasets):
    print("Days:")
    for i in range(len(datasets)):
        print("Day " + str(i + 1) + ": ", str(datasets[i]))
    print("\n")

# Creates new dataset manually via the user
def createnewdataset(datasets, values):
    newdataset = []
    for i in range(values):
        while True:
            try:
                value = int(
                    input(
                        "Value "
                        + str(i + 1)
                        + " (out of "
                        + str(values)
                        + ") of the of day: "
                    )
                )
                break
            except ValueError:
                print("Value is not an integer")
        newdataset.append(value)

    return newdataset


print("\n" * 100)
print("Welcome to an interactive model of a \nPython program a Climatologist would use!")

input("Enter key to start: ")
