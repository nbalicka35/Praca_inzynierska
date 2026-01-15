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
        
    def get_window_size(self):
        """Returns window's size"""
        return self.settings.value("window_size")
    
    def set_window_size(self, size):
        """Sets window's size"""
        self.settings.setValue("window_size", size)
        
    def get_window_position(self):
        """Returns window's position on the screen"""
        return self.settings.value("window_position")
    
    def set_window_position(self, position):
        """Sets window's position on the screen"""
        self.settings.setValue("window_position", position)
        
    def get_window_state(self):
        """Returns window saved state (maximized/normal)"""
        return self.settings.value("window_state", "normal")
    
    def set_window_state(self, state):
        """Sets window state (maximized/normal)"""
        return self.settings.setValue("window_state", state)