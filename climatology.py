datasets = []
values = 0
valuesnotfound = True

def findavg(values):
    total = 0
    for value in values:
        total += value
    return total/len(values)

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
        return (values[len(values)//2] + values[len(values)//2 - 1])/2
    else:
        return (values[len(values)//2])

def findtrend(datasets):
    trend = None
    oldavg = findavg(datasets[0])
    switches = 0

    for dataset in datasets:
        newavg = findavg(dataset)
        if newavg > oldavg:
            if trend == 'Temperature is decreasing':
                switches +=1
            trend = 'Temperature is increasing'
        if newavg < oldavg:
            if trend == 'Temperature is increasing':
                switches +=1
            trend = 'Temperature is decreasing'
        if newavg == oldavg:
            trend = 'Temperature remains the same'
        oldavg = newavg

    if findavg(datasets[-1]) > findavg(datasets[0]):
        nettrend = 'is increasing'
    
    if findavg(datasets[-1]) <= findavg(datasets[0]):
        nettrend = 'is decreasing'
    
    if switches > 0 and switches <= 2:
        trend = 'Temperature has ups and downs but generally ' + nettrend

    if switches > 2:
        trend = 'Too much variation in temperaure to find a trend'
    return trend


def predict(datasets):
    if "increasing" in findtrend(datasets):
        greater = datasets[-1]
        lesser = datasets[-2]
        predictionlist = [None for x in range(len(greater))]

        for i in range(len(greater)):
            larger = greater[i]
            smaller = lesser[i]
            predictionlist[i] = larger + (larger - smaller)

    elif "decreasing" in findtrend(datasets):
        greater = datasets[-1]
        lesser = datasets[-2]
        predictionlist = [None for x in range(len(greater))]

        for i in range(len(greater)):
            larger = greater[i]
            smaller = lesser[i]
            predictionlist[i] = larger + (larger - smaller)

    elif "same" in findtrend(datasets):
        return datasets[-1]

    else:
        return "Too much variation to predict"
    
    return predictionlist

def forecast(dataset):
    print("Highs of", findhigh(dataset), "degrees\nLows of", findlow(dataset), "degrees \nAverage temperatures around", round(findavg(dataset)), "degrees\nMedian temperature is", float(findmedian(dataset)), "degrees")
    input("Enter key to return to home: ")
    homescreen()

def homescreen(invalid = False):
    global datasets

    if invalid:
        print("Invalid Input. Try again")

    print("\033c", end='')
    print("Your datasets: ", datasets, "\n")
    userchoice = input("Options: \n'C' to create new dataset\n'X' to clear datasets\n'F' to forecast a dataset\n'A' to analyze all datasets\n'E' to exit the model: ")
    if userchoice == 'C':
        print("\033c", end='')
        if len(datasets) == 0:
            while True:
                try:
                    values = int(input("How many values are in your dataset? (This will be constant across all datasets): "))
                    break
                except ValueError:
                    print("Value is not an integer")
        else:
            values = len(datasets[0])
        datasets.append(createnewdataset(datasets, values))
    if userchoice == 'X':
        print("\033c", end='')
        datasets = []
    if userchoice == "F" and len(datasets) > 0:
        print("\033c", end='')
        print("Datasets:", datasets )
        while True:
            try:
                forecast(datasets[int(input("Which dataset would you like to forecast? ")) - 1])
                break
            except ValueError:
                print("Value is not an integer")
            except IndexError:
                print("Dataset at such location doesn't exsist")
    if userchoice == "A":
        print("\033c", end='')
        print("Datasets:", datasets )
        print("\nUsing data from all datasets, the trend is: \n" + findtrend(datasets) + "\n\nThe model predicts the next dataset to be: ")
        print(predict(datasets), "\n")
        input("Enter key to return to home: ")
    if userchoice != "E":
        homescreen(True)
    else:
        return
    

def createnewdataset(datasets, values):
    newdataset = []
    for i in range(values):
        while True:
            try:
                value = int(input("Value " + str(i+1) + " (out of " + str(values) + ") of the of dataset: "))
                break
            except ValueError:
                print("Value is not an integer")
        newdataset.append(value)
    
    return newdataset

print("\033c", end='')
print("Welcome to an interactive model of a Python program a Climatologist would use!")

while True:
    if input("'S' to start: ") == 'S':
        homescreen()
    break