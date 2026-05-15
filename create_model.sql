-- Create or replace the machine learning model
CREATE OR REPLACE MODEL `data-eng-bootcamp-494311.salaries_ml_region_us.Salary_Model`
OPTIONS(
  -- Use Boosted Tree Regressor for high accuracy with tabular data
  MODEL_TYPE='BOOSTED_TREE_REGRESSOR', 
  
  -- Set the target column we want to predict (Salary in Saudi Riyals)
  INPUT_LABEL_COLS=['salary_in_sar'],  
  
  -- Automatically split the data into training and evaluation sets for better validation
  DATA_SPLIT_METHOD='AUTO_SPLIT',      
  
  -- Define the maximum number of training rounds (iterations)
  MAX_ITERATIONS=50                    
) AS

SELECT 
  -- Include all relevant features for training
  -- We exclude 'job_title' specifically to avoid noise, as it has 317+ unique values
  * EXCEPT(job_title) 
FROM 
  `data-eng-bootcamp-494311.salaries_ml_region_us.Data_ML`
WHERE 
  -- Ensure the model only trains on rows that have a valid target value
  salary_in_sar IS NOT NULL;
