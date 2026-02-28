Controlling for PCA factors and trade the reversal in PCA residuals rather than the returns. 


We optimize the lookback and number of day reversals using Optuna (https://optuna.org/). Thus:

	- Define the objective function to be optimized -> Sharpe Ratio
	
	- Suggest hyperparameter values using trial object -> 0.5 and 1 year for lookback and 1 - 3 for Number of days reversals. 
	
	- Create a study object and invoke the optimize method over n trials, where n >= 2

	
The results suggest that the positive cumulative returns are more consistent for the bottom factors either with or w/o lag added. 

