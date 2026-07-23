from dataclasses import dataclass

@dataclass
class DeviceCreateRequestDTO:
    brand_name: str
    resolution: str

    def validate(self) -> list:
        errors = []
        if not self.brand_name or len(self.brand_name) < 3:
            errors.append("Brand name must be at least 3 characters.")
        
        valid_resolutions = ["720p", "1080p", "4k"]
        if self.resolution not in valid_resolutions:
            errors.append(f"Invalid resolution. Must be one of {valid_resolutions}.")
            
        return errors


@dataclass
class DeviceResponseDTO:
    device_id: str
    brand_name: str
    message: str
