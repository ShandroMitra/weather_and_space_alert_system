# main.py
print("\n🟢 Starting the Weather Alert System...\n")
from weather_alert_system.step07_generate_alert_weather_data import run_weather_alert_system

if __name__ == "__main__":
    
    run_weather_alert_system()
    print('✅ WEATHER ALERT SYSTEM EXECUTED SUCCESSFULLY WITH ALL THE STEPS. EXIT CODE-  0')

    # Import only after weather alert is done
    print("\n🟢 Starting the Space Alert System...\n")
    from space_alert_system.step07_generate_alert_neo_data import run_space_alert_system

    run_space_alert_system()
    print('✅ SPACE ALERT SYSTEM EXECUTED SUCCESSFULLY WITH ALL THE STEPS. EXIT CODE-  0')
