Simple data analysis program geared toward predicting weather. For Earth Science project on Climatology.
Simple capabilities:
- Obtain highest value in dataset
- Obtain lowest value in dataset
- Obtain average within dataset
- Obtain median within dataset
- Find the trend in a dataset (increasing/decreasing/stays the same)

Predictive capabilities:
- Predicts next value based on trend (increasing/decreasing), and the last 3 values
- Finds if the differences between the last 3 values are linear --> applies linear value accordingly for prediction
- If not, finds the percent in change between the last 3 values --> takes the latest percent for prediction, applies the average between the second to last percentage and the second to last percentage for deviance

Limitations:
- Only looks at the last 3 values (cannot see overall trends, ups and downs)
- No other data (precipitation, etc)

Examples:
Given: 1, 2, 3, 4 --> Predicts 5 || Pattern: + 1
Given: 1, 10, 100 --> Predicts 1000 || Pattern: * 10
Given: 1, 1, 2, 3, 5, 8 --> Predicts 13 || Pattern: Fibonacci 
Given: 1, 2, 4, 7, --> Predicts 12 +/- 1 || Pattern: Lazy Caterer

Changing the confidence:
Slightly adjust the FACTOR value on line 8 to make the model more/less confident
