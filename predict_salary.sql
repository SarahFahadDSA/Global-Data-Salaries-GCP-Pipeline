-- Using ML.PREDICT to generate salary insights from the trained model
SELECT 
  -- Display input features for clarity in the output
  job_category,
  experience_level,
  company_location,
  -- Calculate and round the predicted annual salary in Saudi Riyals (SAR)
  ROUND(predicted_salary_in_sar, 0) AS predicted_annual_salary_SAR
FROM
  ML.PREDICT(MODEL `data-eng-bootcamp-494311.salaries_ml_region_us.Salary_Model`, 
  (
    -- Manually defining input features for a real-world testing scenario
    SELECT 
      'Data Engineering' AS job_category,
      'Entry-level' AS experience_level,
      'Full-time' AS employment_type,
      'SA' AS company_location,
      'Middle East & Africa' AS company_region,
      'SA' AS employee_residence,
      'Medium' AS company_size,
      'On-site' AS remote_ratio 
  ));
