-- Evaluation of the Salary Prediction Model
-- This query retrieves performance metrics like MAE, MSE, and R-Squared
SELECT
  *
FROM
  ML.EVALUATE(MODEL `data-eng-bootcamp-494311.salaries_ml_region_us.Salary_Model`);
