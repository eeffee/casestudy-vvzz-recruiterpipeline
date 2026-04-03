import pandas as pd
import re
import ast

# Date time should be in year-month-day format 
# Date function
def clean_date(date_str):
    if pd.isna(date_str):
        return None
    try:
        return pd.to_datetime(date_str).date()
    except:
        return None

# Reed dataset Clean Currency, Salary Functions
#------------------------------
# for the missing or dirty currency; infer from country or set to unknown 
def clean_currency(currency, country):
    if pd.notna(currency) and isinstance(currency, str) and len(currency) == 3 and currency.isalpha():
        return currency.upper()
    country_currency = {
        'United Kingdom': 'GBP', 'UK': 'GBP', 'England': 'GBP',
        'Netherlands': 'EUR', 'Belgium': 'EUR', 'Germany': 'EUR', 'Ireland': 'EUR',
        'Canada': 'CAD', 'US': 'USD', 'USA': 'USD', 'United States': 'USD',
        'India': 'INR', 
    }
    if pd.notna(country):
        for key, curr in country_currency.items():
            if key.lower() in str(country).lower():
                return curr
    return None

# Salary parsing only keep min and max, no need for exact salary field
def parse_reed_salary(row):
    if pd.notna(row['salaryMin']) and pd.notna(row['salaryMax']):
        return row['salaryMin'], row['salaryMax']
    return None, None

def reed_salary_period(unit):
    if pd.isna(unit):
        return None
    u = str(unit).lower()
    if 'annum' in u or 'year' in u:
        return 'annual'
    if 'hour' in u:
        return 'hour'
    return None
#------------------------------


# Naukri dataset Salary Functions 
#-------------------------------
def parse_naukri_salary(s):
    if pd.isna(s):
        return None, None, None
    d = ast.literal_eval(s)
    min_sal = d.get('minimumSalary')
    max_sal = d.get('maximumSalary')
    if min_sal == 0 and max_sal == 0:
        return None, None, None
    return min_sal, max_sal, d.get('currency')

# Dice dataset Salary Functions
#----------------------------------
def parse_dice_salary(s):
    if pd.isna(s):
        return None, None, None
    nums = re.findall(r'([\d,]+\.?\d*)', str(s))
    if len(nums) >= 2:
        min_sal = float(nums[0].replace(',',''))
        max_sal = float(nums[1].replace(',',''))
        curr = 'USD' if 'USD' in s else None
        return min_sal, max_sal, curr
    return None, None, None

def dice_salary_period(unit):
    if pd.isna(unit):
        return None
    u = str(unit).lower()
    if 'annual' in u or 'year' in u:
        return 'annual'
    if 'hour' in u:
        return 'hour'
    return None
#---------------------------------

# Mapper functions for Reed dataset
#--------------------------------
def map_remote_status_reed(value):
    if pd.isna(value):
        return None
    v = str(value).lower()
    if 'remote' in v: return 'remote'
    if 'hybrid' in v: return 'hybrid'
    if 'onsite' in v or 'on-site' in v: return 'onsite'
    return None

def map_contract_reed(value):
    if pd.isna(value):
        return None
    v = str(value).lower()
    if 'permanent' in v:
        return 'permanent'
    if 'contract' in v:
        return 'contract'
    return None

def map_time_reed(value):
    if pd.isna(value):
        return None
    v = str(value).lower()
    if 'full' in v:
        return 'full_time'
    if 'part' in v:
        return 'part_time'
    return None

# Mapper functions for Dice dataset 
#------------------------------
# return job location type based on the boolean fields for remote, hybrid and onsite. If multiple are true, remote > hybrid > onsite in priority.
def map_remote_status_dice(remote_bool, hybrid_bool, onsite_bool):
    if remote_bool: return 'remote'
    if hybrid_bool: return 'hybrid'
    if onsite_bool: return 'onsite'
    return None

# In Dice dataset, permanent contract labeled as direct 
def map_contract_dice(contract_type):
    if pd.isna(contract_type):
        return None
    ct = str(contract_type).lower()
    if 'direct' in ct:
        return 'permanent'
    if 'contract' in ct:
        return 'contract'
    return None

def map_time_dice(position_schedule):
    if pd.isna(position_schedule):
        return None
    ps = str(position_schedule).lower()
    if 'full' in ps:
        return 'full_time'
    if 'part' in ps:
        return 'part_time'
    return None
#-----------------------------
def parse_location(location_raw):
    """Simple split by comma to get city and region."""
    if pd.isna(location_raw):
        return None, None
    parts = str(location_raw).split(',')
    if len(parts) >= 2:
        city = parts[0].strip()
        region = parts[1].strip()
        return city, region
    return location_raw.strip(), None

# Common functions for all datasets to infer Seniority, Industry and Skills using description
#------------------------------

def extract_seniority(description):
    text = str(description).lower()
    if any(word in text for word in ['senior', 'sr.', 'lead', 'principal', 'staff', 'manager', 'director']):
        return 'senior'
    if any(word in text for word in ['junior', 'jr.', 'entry', 'associate', 'trainee']):
        return 'junior'
    if any(word in text for word in ['mid', 'intermediate', 'experienced']):
        return 'mid'
    return None

def extract_industry(description, original_industry):
    if pd.notna(original_industry):
        return original_industry
    if pd.isna(description):
        return None
    desc_lower = str(description).lower()
    industry_keywords = {
        'healthcare': ['health', 'medical', 'clinical', 'hospital'],
        'finance': ['finance', 'banking', 'investment', 'insurance'],
        'technology': ['software', 'it', 'cloud', 'data', 'ai', 'machine learning'],
        'retail': ['retail', 'ecommerce', 'merchandise'],
        'manufacturing': ['manufacturing', 'production', 'assembly'],
        'defense': ['defense', 'military', 'aerospace'],
        'education': ['education', 'school', 'university', 'academic']
    }
    for industry, keywords in industry_keywords.items():
        if any(kw in desc_lower for kw in keywords):
            return industry
    return None
#-------------------------------
#dummy list can be enhanced for real use case
COMMON_SKILLS = ['pandas','python', 'sql', 'excel', 'tableau', 'aws', 'java', 'javascript',
                 'react', 'node.js','machine learning', 'nlp', 'tensorflow',
                 'agile', 'scrum', 'project management', 'leadership']

def extract_skills_from_text(text):
    if pd.isna(text):
        return None
    text_lower = str(text).lower()
    found = [skill for skill in COMMON_SKILLS if skill in text_lower]
    return ', '.join(found) if found else None
#------------------------------



reed = pd.read_csv('/Users/efeoztufan/Downloads/dataset_reed_jobs.csv')
naukri = pd.read_csv('/Users/efeoztufan/Downloads/dataset_naukri_jobs.csv')
dice = pd.read_csv('/Users/efeoztufan/Downloads/dataset_dice_jobs.csv')
print(f"Reed: {len(reed)} rows, Naukri: {len(naukri)} rows, Dice: {len(dice)} rows")



# Transform Reed Dataset 
#------------------------------
reed_clean = reed[['title', 'companyName', 'jobLocation', 'jobLocationCountry',
                   'jobLocationType', 'employmentType', 'datePosted', 'descriptionText',
                   'currency', 'salaryMin', 'salaryMax', 'salaryTimeUnit']].copy()

reed_clean['source'] = 'reed'
reed_clean.rename(columns={'companyName':'company', 'jobLocation':'location_raw',
                           'jobLocationCountry':'country', 'datePosted':'date_posted',
                           'descriptionText':'description'}, inplace=True)

reed_clean[['city', 'region']] = reed_clean['location_raw'].apply(
    lambda x: pd.Series(parse_location(x)))

reed_clean['remote_status'] = reed_clean['jobLocationType'].apply(map_remote_status_reed)
reed_clean['employment_contract'] = reed_clean['employmentType'].apply(map_contract_reed)
reed_clean['employment_time'] = reed_clean['employmentType'].apply(map_time_reed)

reed_clean[['salary_min','salary_max']] = reed_clean.apply(parse_reed_salary, axis=1, result_type='expand')
reed_clean['salary_currency'] = reed_clean.apply(lambda r: clean_currency(r['currency'], r['country']), axis=1)
reed_clean['salary_period'] = reed_clean['salaryTimeUnit'].apply(reed_salary_period)

reed_clean['date_posted'] = reed_clean['date_posted'].apply(clean_date)
reed_clean['skills'] = reed_clean['description'].apply(extract_skills_from_text)
reed_clean['industry'] = reed_clean.apply(
    lambda r: extract_industry(r['description'], r.get('industry')), axis=1)

reed_clean['seniority'] = reed_clean['description'].apply(extract_seniority)
#------------------------------


# Transform Dice Dataset
#------------------------------
dice_clean = dice[['title', 'companyName', 'location', 'country', 'remote', 'hybrid', 'onsite',
                   'contractType', 'positionSchedule', 'datePosted', 'skills', 'description', 'salaryRaw', 'salaryRawUnit']].copy()

dice_clean['source'] = 'dice'
dice_clean.rename(columns={'companyName':'company', 'location':'location_raw',
                           'datePosted':'date_posted'}, inplace=True)
dice_clean[['city', 'region']] = dice_clean['location_raw'].apply(
    lambda x: pd.Series(parse_location(x)))
# For this we have separeted fields for job location type as boolean. Therefore a custom mapping functions is created above
dice_clean['remote_status'] = dice_clean.apply(lambda r: map_remote_status_dice(r['remote'], r['hybrid'], r['onsite']), axis=1)
dice_clean['employment_contract'] = dice_clean['contractType'].apply(map_contract_dice)
dice_clean['employment_time'] = dice_clean['positionSchedule'].apply(map_time_dice)
dice_clean['skills'] = dice_clean['skills'].apply(lambda x: ', '.join([s['name'] for s in eval(x)]) if pd.notna(x) else None)
dice_clean[['salary_min','salary_max','salary_currency']] = dice_clean['salaryRaw'].apply(lambda x: pd.Series(parse_dice_salary(x)))
dice_clean['salary_period'] = dice_clean['salaryRawUnit'].apply(dice_salary_period)
dice_clean['date_posted'] = dice_clean['date_posted'].apply(clean_date)
dice_clean['industry'] = dice_clean.apply(
    lambda r: extract_industry(r['description'], None), axis=1)
dice_clean['seniority'] = dice_clean['description'].apply(extract_seniority)

# Transform Naukri Dataset
#------------------------------
naukri_clean = naukri[['title', 'companyName', 'location', 'tagsAndSkills',
                       'createdDate', 'jobDescription', 'salaryDetail']].copy()

naukri_clean['source'] = 'naukri'
naukri_clean.rename(columns={'companyName':'company', 'location':'location_raw',
                             'tagsAndSkills':'skills', 'createdDate':'date_posted',
                             'jobDescription':'description'}, inplace=True)

naukri_clean[['city', 'region']] = naukri_clean['location_raw'].apply(
    lambda x: pd.Series(parse_location(x)))

# while believe that all Naukri data is from India but since there is no country info has given prefer to set as None
naukri_clean['country'] = None

# No info about remote/onsite/hybrid and employment type in the Naukri dataset, so set to unknown
naukri_clean['remote_status'] = None
naukri_clean['employment_contract'] = None
naukri_clean['employment_time'] = None
#Custom function to parse salary details
naukri_clean[['salary_min','salary_max','salary_currency']] = naukri_clean['salaryDetail'].apply(
    lambda x: pd.Series(parse_naukri_salary(x)))
naukri_clean['salary_period'] = None
naukri_clean['date_posted'] = naukri_clean['date_posted'].apply(clean_date)
naukri_clean['industry'] = naukri_clean.apply(
    lambda r: extract_industry(r['description'], None), axis=1)
naukri_clean['seniority'] = naukri_clean['description'].apply(extract_seniority)
#------------------------------


# Concatanete and finalize with selected columns 
print(f"Cleaned rows: Reed={len(reed_clean)}, Naukri={len(naukri_clean)}, Dice={len(dice_clean)}")

agg_data = pd.concat([reed_clean, dice_clean, naukri_clean], ignore_index=True)
agg_data = agg_data.drop_duplicates(keep='first')
agg_data.insert(0, 'id', range(1, len(agg_data)+1))

final_cols = ['id', 'title', 'company', 'city', 'region', 'country',
              'remote_status', 'employment_contract', 'employment_time',
              'salary_min', 'salary_max', 'salary_currency', 'salary_period',
              'date_posted', 'skills', 'industry', 'seniority', 'description', 'source']

agg_data = agg_data[final_cols]
agg_data.to_csv('allset_jobs.csv', index=False)
print(f"Total unified rows: {len(agg_data)}")
