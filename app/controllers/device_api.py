from app.dtos.device_dto import DeviceCreateRequestDTO, DeviceResponseDTO

class DeviceAPIController:
    
    def get_devices(self, request):
        if request.get("method") != "GET":
            return {"status_code": 405, "message": "Method Not Allowed"}
            
        return {
            "status_code": 200,
            "data": []
        }

    def create_device(self, request):
        if request.get("method") != "POST":
            return {"status_code": 405, "message": "Method Not Allowed"}
            
        payload = request.get("body", {})
        dto = DeviceCreateRequestDTO(
            brand_name=payload.get("brand_name", ""),
            resolution=payload.get("resolution", "")
        )
        
        validation_errors = dto.validate()
        if validation_errors:
            return {
                "status_code": 400, 
                "message": "Bad Request - Validation Failed", 
                "errors": validation_errors
            }
            
        response_dto = DeviceResponseDTO(
            device_id="CAM_9X01", 
            brand_name=dto.brand_name, 
            message="Device created successfully."
        )
        
        return {
            "status_code": 201, 
            "data": response_dto.__dict__
        }
