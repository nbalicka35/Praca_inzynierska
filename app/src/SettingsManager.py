from PyQt5.QtCore import QSettings

class SettingsManager:
    """
    Saves and loads user's app settings
    """
    
    def __init__(self):
        # Create or open registry file \Neuron\Neuron Desktop App
        self.settings = QSettings("Neuron", "Neuron Desktop App")
        
    def get_language(self):
        """Returns language saved in settings"""
        return self.settings.value("language", "EN") # Rollback to English (default) if language is not specified
        
    def set_language(self, language):
        """Saves chosen language"""
        self.settings.setValue("language", language)
        
    def get_theme(self):
        """Returns theme saved in settings"""
        return self.settings.value("theme", "Light") # Rollback to Light (default) if theme is not specified
        
    def set_theme(self, theme):
        """Saves chosen theme"""
        self.settings.setValue("theme", theme)