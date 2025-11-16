WEATHER AND SPACE ALERT SYSTEM
==============================

Author and Contact
------------------
Author: Shandro Mitra  
Contact Email: Shandro.mitra@gmail.com
--------------------------------------
--------------------------------------

Overview
--------
This project integrates data from the Open-Meteo API and NASA's Near Earth Object (NEO) API to monitor and generate alerts for weather and space events.

The system performs the following tasks:

Weather Alert System:
- Fetches weather data from Open-Meteo API
- Cleans and transforms the data
- Validates and loads the data into a database
- Detects extreme weather conditions and sends alert emails

Space Alert System:
- Fetches asteroid and near-earth object data from NASA NEO API
- Cleans, transforms, and validates the data
- Loads data into the database
- Detects potential asteroid threats and sends alert emails

Sample Log Output
-----------------
🟢 Starting the Weather Alert System...

✅ Data fetched successfully from API for weather alert system  
✅ Data cleaning completed successfully for weather alert system.  
✅ Data transformation completed successfully for weather alert system.  
✅ Validation PASSED. Data is ready for downstream for weather alert system.  
✅ Data loaded and 'processing_status' updated in weather_alert.weather_hourly_info_initial for batch_id=20250629195734746 for weather alert system  
✅ Audit trail updated in weather_alert.weather_alert_audit_trail for batch_id=20250629195734746 with record count 10 for weather alert system  
✅ Weather alerts detected: YES for weather alert system  
✅ Weather Alert email sent to ['arghamitra4626@gmail.com']  
✅ WEATHER ALERT SYSTEM EXECUTED SUCCESSFULLY WITH ALL THE STEPS. EXIT CODE-  0  

🟢 Starting the Space Alert System...

✅ Data fetched successfully for space alert system.  
✅ Data cleaning completed successfully for space alert system.  
✅ Data transformation completed successfully for space alert system.  
✅ Validation PASSED. Data is ready for downstream for space alert system.  
🟡 No new records to insert. All nasa_id values already exist.  
✅ Asteroid alerts detected: YES for space alert system  
✅ Space Alert email sent to ['arghamitra4626@gmail.com']  
✅ SPACE ALERT SYSTEM EXECUTED SUCCESSFULLY WITH ALL THE STEPS. EXIT CODE-  0  
--------------------------------------------------------------------------------------

Requirements
------------
- Python 3.10 must be installed
- All Python dependencies are listed in requirements.txt

Environment Configuration (.env)
--------------------------------
# Mail Credentials
GMAIL_APP_PASSWORD=''
SENDER_MAIL_ID=''
RECIPIENT_EMAILS=user1@example.com,user2@example.com

# Database Configuration
db_user=''
db_password=''
db_host=''
db_port=''
db_name=''

weather_schema_name='weather_alert'
weather_table_name='weather_hourly_info_initial'
weather_audit_table='weather_alert_audit_trail'

nasa_schema_name='space_alert'
nasa_table_name='near_earth_objects_data_initial'
nasa_audit_table='space_alert_audit_trail'

NASA_NEO_API_KEY=''
-----------------------------------------------------------


Instructions
------------
1. Clone the repository  
2. Install dependencies:  
   `pip install -r requirements.txt`  
3. Create and populate the `.env` file under the folder - 'Weather and Space Alert System' 
4. Run the main script:  
   `python main.py`  
5. Monitor logs for status and alerts
6. run the following code in postgres- "CREATE DATABASE WEATHER AND SPACE ALERT DB;"

--------------------------------------------------------------------




