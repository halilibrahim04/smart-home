from app.entities.device import Device

def register_smart_thermostat():
    thermostat = Device(
        name="Living Room Thermostat", 
        device_type="Climate", 
        ip_address="192.168.1.50"
    )
    
    print(f"Device Name: {thermostat.name}")
    
    status = thermostat.connect()
    print(status)
    
    return thermostat

if __name__ == "__main__":
    register_smart_thermostat()
