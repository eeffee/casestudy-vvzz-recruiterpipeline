General Notes

1) Three different dataset provided for use-case, then common fields at least for two dataset has selected for the desired final table integration. All datasets are transformed regarding the desired table schema.

    1.1) For Dice dataset positionSchedule, remote, onsite, hybrid fields are mapped. Location field is parsed using basic regex. Region field was already recorded in the dateset, easily parsed. Salary field were recorded as a messy string, salary values extracted during transformation as a float. Skills, salary unit, contract type fields transformed. Industry information handled using dumy list searching through description field. Seniority extracting function is created to find if any words occurs in the description.
    1.2) For Reed dataset, custom functions apllied to transform fields mentioned above. Differences are since there is no region information in the source and any location extraction function created for this scopre so that field remained null. Incorrect values in the currency field has fixed for some countries such as NL, Ireland etc using custom function. Industry information was already in the source data, directly fetched it.
    1.3) For Naukri dataset, firstly last application date is not defined in this dataset therefore that field removed from other datasets and not used in the final schema to avoid inconsistency. Remote status and contratc type fields are null in the final dataset. These fields are not provided in Naukri. General transformations are applied as mentioned above. Original skills used and industry, seniority extraction applied with dummy custom functions.


2) Further Enhancements
    2.1) NLP techniques, APIs or comprehensive list can be used to extract industry field for Dice and Naukri datasets. This was the optimal choice within a given time.
    2.2) Geoinfo such as region info for Dice and country for Naukri can be found using libraries but integration takes time, validation and cross-checks. 

3) Missing Points (Limited time)
    3.1) Validation is not implemented for data quality such as future date min, max salary etc. 
    3.2) Original data have 3000 rows in total. After transformation, 24 records were lost(2976), not investigated might from salary parsing in Dice dataset. 