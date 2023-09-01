# Report: Predict Bike Sharing Demand with AutoGluon Solution
#### Author: KhoiVN

## Initial Training
### What did you realize when you tried to submit your predictions? What changes were needed to the output of the predictor to submit your results?
Remove 2 columns: casual and registered because they are also not present in the test dataset.

### What was the top ranked model that performed?
WeightedEnsemble_L3

## Exploratory data analysis and feature creation
### What did the exploratory analysis find and how did you add additional features?
Data has multiple types such as category, numeric, and datetime. Split datetime into numeric and try to make some combination between columns.

### How much better did your model preform after adding additional features and why do you think that is?
It's better 3 times than inital trainning.

## Hyper parameter tuning
### How much better did your model preform after trying different hyper parameters?
The score decrease into 0.52606 and lower than previos score of 0.63184.

### If you were given more time with this dataset, where do you think you would spend more time?
I will spend time featuring data like split numeric into group, and maybe explore hyperparameter of models.

### Create a table with the models you ran, the hyperparameters modified, and the kaggle score.
|model|searcher|scheduler|num_trials|score|
|--|--|--|--|--|
|initial|default|default|0|1.80095|
|add_features|default|default|0|0.63184|
|hpo|auto|local|2|0.52606|

### Create a line plot showing the top model score for the three (or more) training runs during the project.

![model_train_score.png](images/model_train_score.png)

### Create a line plot showing the top kaggle score for the three (or more) prediction submissions during the project.

![model_test_score.png](images/model_test_score.png)

## Summary
This is a pipeline of Machine Learning project. We need focus on feature engineering and finetune models to have best score. Then we must deep dive into AutoGluon to understand how it works and how to use it effectively. Finally, submit the best score to Kaggle and get the result.
