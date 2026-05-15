import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import re

# 1. Define the Transformation Logic (User Defined Function)
class SalaryDataTransform(beam.DoFn):
    def process(self, element):
        # Create a copy of the row to avoid mutating original data during processing
        row = element.copy()
        
        try:
            # --- Step 1: Currency Conversion & Column Cleanup ---
            # Calculate salary in SAR (Saudi Riyal) from USD
            if 'salary_in_usd' in row and row['salary_in_usd'] is not None:
                row['salary_in_sar'] = float(row['salary_in_usd']) * 3.75
            
            # Remove legacy salary columns that are no longer needed
            row.pop('salary', None)
            row.pop('salary_currency', None)


            # --- Step 2: Company Size Mapping ---
            # Convert shorthand company size codes to full descriptive terms
            size_map = {
            'S': 'Small',
            'M': 'Medium',
            'L': 'Large'
           }
            row['company_size'] = size_map.get(row['company_size'], row['company_size'])


            # --- Step 3: Experience Level Mapping ---
            # Standardize experience codes into readable professional titles
            exp_map = {
                'EN': 'Entry-level',
                'MI': 'Mid-level',
                'SE': 'Senior-level',
                'EX': 'Executive-level'
            }
            row['experience_level'] = exp_map.get(row['experience_level'], row['experience_level'])

            # --- Step 4: Employment Type Mapping ---
            # Convert shorthand employment codes to full descriptive terms
            emp_map = {
                'FT': 'Full-time',
                'PT': 'Part-time',
                'CT': 'Contract',
                'FL': 'Freelance'
            }
            row['employment_type'] = emp_map.get(row['employment_type'], row['employment_type'])

            # --- Step 5: Remote Work Ratio Mapping ---
            # Translate numeric remote ratios into work environment categories
            remote_val = str(row.get('remote_ratio', ''))
            if remote_val == '0': row['remote_ratio'] = 'On-site'
            elif remote_val == '50': row['remote_ratio'] = 'Hybrid'
            elif remote_val == '100': row['remote_ratio'] = 'Remote'

            # --- Step 6: Job Title Categorization ---
            # Use Regex to group specific job titles into broader tech domains
            title = str(row.get('job_title', '')).lower()
            
            if re.search(r'ai|machine learning|ml|nlp|vision|deep learning|robotics|prompt', title):
                row['job_category'] = 'AI & Machine Learning'
            elif re.search(r'data scientist|research scientist|applied scientist|scientist|statistician|decision', title):
                row['job_category'] = 'Data Science'
            elif re.search(r'data engineer|analytics engineer|etl|database|architect|dataops|infrastructure', title) and 'machine learning' not in title:
                row['job_category'] = 'Data Engineering'
            elif re.search(r'analyst|business intelligence|bi|visualization|reporting', title):
                row['job_category'] = 'Data Analysis & BI'
            elif re.search(r'governance|quality|management|strategy|integrity', title):
                row['job_category'] = 'Data Management & Governance'
            elif re.search(r'software|developer|devops|cloud|backend|frontend', title):
                row['job_category'] = 'Software & Cloud Engineering'
            elif re.search(r'product|manager|business analyst|marketing|finance', title):
                row['job_category'] = 'Product & Business'
            else:
                row['job_category'] = 'Other Specialized Tech'

            # --- Step 7: Geographic Region Mapping ---
            # Categorize countries into major global economic regions
            loc = str(row.get('company_location', ''))
            if loc == 'US': row['company_region'] = 'United States'
            elif loc == 'CA': row['company_region'] = 'Canada'
            elif loc in ['SA', 'AE', 'OM', 'QA', 'LB', 'IQ', 'EG', 'DZ', 'MU']: row['company_region'] = 'Middle East & Africa'
            elif loc in ['GB', 'DE', 'FR', 'ES', 'NL', 'IT', 'PT', 'PL', 'GR', 'IE', 'SE', 'AT', 'BE', 'RO']: row['company_region'] = 'Europe'
            elif loc in ['IN', 'CN', 'JP', 'PK', 'SG', 'TH', 'VN', 'ID', 'MY', 'PH', 'KR']: row['company_region'] = 'Asia'
            elif loc in ['BR', 'MX', 'AR', 'CO', 'CL', 'PE']: row['company_region'] = 'Latin America'
            elif loc in ['AU', 'NZ']: row['company_region'] = 'Oceania'
            else: row['company_region'] = 'Other Regions'

            yield row
            
        except Exception as e:
            # Log errors for specific rows while keeping the pipeline running
            print(f"Error processing row: {e}")

# 2. Pipeline Orchestration
def run():
    # Environment Configuration
    project_id = 'data-eng-bootcamp-494311'
    region_name = 'me-central1' # Doha Region
    bucket_name = 'gs://salary_data_qatar_bucket'
    
    # Global Pipeline Options (Centralized temp/staging locations)
    options = PipelineOptions(
        project=project_id,
        region=region_name,
        temp_location=f'{bucket_name}/temp',
        staging_location=f'{bucket_name}/staging',
        runner='DataflowRunner' #For display in data flow
    )
    
    # Define BigQuery source and destination paths
    input_table = f'{project_id}:salary_data_set.global_salaries'
    output_table = f'{project_id}:salary_data_set.global_salaries_cleaned'

    # Build and execute the Apache Beam Pipeline
    with beam.Pipeline(options=options) as p:
        (
            p 
            | 'Read From BigQuery' >> beam.io.ReadFromBigQuery(table=input_table)
            | 'Clean & Transform' >> beam.ParDo(SalaryDataTransform())
            | 'Write To BigQuery' >> beam.io.WriteToBigQuery(
                output_table,
                schema='SCHEMA_AUTODETECT', # Automatically infer table schema
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE # Overwrite existing data
            )
        )

if __name__ == '__main__':
    run()
