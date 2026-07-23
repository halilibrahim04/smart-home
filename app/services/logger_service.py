class LoggerService:
    def log(self, message: str):
        # Sistemin loglarını (veritabanı veya dosyaya) yazan servis.
        print(f"[LOG] {message}")
