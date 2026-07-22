"""
Bu senaryoda, bir "Akıllı Termostat" sisteminden gelen sıcaklık (temperature) 
verilerinin kontrol edilmesini (Validation) sağlayan bir Python betiği (script) yazıyoruz.
"""

device_name = "Akıllı Termostat"
maxTemperature = 35.5
is_active = True
port_number = 8080
sensor_logs = [22.5, 23.0, 36.1, 21.0]

def check_device_temperatures(temperature_list, limit_temp):
    warning_count = 0
    is_safe = True

    for current_temp in temperature_list:
        if current_temp > limit_temp:
            warning_count += 1
            is_safe = False
        else:
            pass
            
    return warning_count, is_safe


warnings, device_safe = check_device_temperatures(sensor_logs, maxTemperature)


class DummyDevice:
    def turn_on(self):
        self.is_active = True
        return self.is_active
