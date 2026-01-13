class ThemesManager:
    THEMES = {
        "Light": {
            "background": "#FFFAF2",
            "card": "#FFFFFF",
            "text": "black",
            "button": "rgba(148, 211, 255, .72)",
            "button-hover": "rgba(148, 211, 255, .9)",
            "res-card-background": "rgba(148, 211, 255, .2)",
            "vscroll-background": "rgb(148, 211, 255)",
            "vscroll-handle-background": "rgba(148, 211, 255, .5)"
        },
        "Dark" : {
            "background": "#1B2037",
            "card": "#376281",
            "text": "#FFFAF2",
            "button": "rgba(27, 32, 55, .72)",
            "button-hover": "rgba(27, 32, 55, .9)",
            "res-card-background": "rgba(27, 32, 55, .15)",
            "vscroll-background": "rgb(27, 32, 55)",
            "vscroll-handle-background": "rgba(27, 32, 55, .5)"
        }
    }
    
    def __init__(self, window): 
        self.window=window
        self.scale_manager = self.window.scale_manager
        self.current_theme="Light"
        
    def apply_theme(self, theme):
        self.current_theme = theme
        colors = self.THEMES[self.current_theme]
        self._apply_main_window_style(colors=colors)
        self._apply_button_style(colors=colors)
        self._apply_res_card_style(colors=colors)
        self._apply_labels_style(colors=colors)
        
    def _apply_main_window_style(self, colors):
        self.window.setStyleSheet(
        f"background-color: {colors["background"]}; color: {colors["text"]}"
        )
        self.window.card.setStyleSheet(
            f"""
            #card {{
                background-color: {colors["card"]};
                color: {colors["text"]};
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
            }}
            """
        )
        
        self.window.card.preview_container.setStyleSheet(f"background-color: {colors["card"]};")
        self.window.card.thumbnails_container.setStyleSheet(f"background-color: {colors["card"]};")

        
    def _apply_button_style(self,colors):
        text_size = self.scale_manager.scale_font(18)
        border_radius = self.scale_manager.scale_value(10)
        
        button_style = f"""
            QPushButton {{
                background-color: {colors["button"]};
                color: {colors["text"]};
                border: 0px;
                border-radius: {border_radius}px;
                font-size: {text_size}px;
            }}
            QPushButton:hover {{
                background-color: {colors["button-hover"]};
            }}
            """
        self.window.card.file_button.setStyleSheet(
            button_style
        )
        self.window.card.dir_button.setStyleSheet(
            button_style
        )
        self.window.card.clear_button.setStyleSheet(
            button_style
        )
        self.window.card.predict_button.setStyleSheet(
            button_style
        )
        
    def _apply_res_card_style(self, colors):
        self.window.card.results_card.setStyleSheet(
        f"""
        #results_card {{
                background-color: {colors["res-card-background"]};
                color: {colors["text"]};
                border-radius: 10px;
                border: none;
            }}
            QScrollBar:vertical {{
                background: {colors["vscroll-background"]};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {colors["vscroll-handle-background"]};
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
        )
        
        self.window.card.results_container.setStyleSheet(
            f"background-color: transparent;"
        )
        
    def _apply_labels_style(self, colors):
        font_large = self.scale_manager.scale_font(20)
        font_medium = self.scale_manager.scale_font(18)
        font_small = self.scale_manager.scale_font(14)
        
        self.window.card.step1_label.setStyleSheet(f"font-weight: bold; font-size: {font_large}px; color: {colors["text"]}; background-color: {colors["card"]};")
        self.window.card.step1_desc.setStyleSheet(f"font-size: {font_medium}px; color: {colors["text"]}; background-color: {colors["card"]};")
        
        self.window.card.preview_label.setStyleSheet(f"background-color: {colors["card"]}; color: {colors["text"]}; font-size: {font_small}px;")
        self.window.card.file_name_label.setStyleSheet(f"background-color: {colors["card"]}; font-size: {font_small}px; color: {colors["text"]};")
        
        self.window.card.step2_label.setStyleSheet(
            f"font-weight: bold; font-size: {font_large}px; color: {colors["text"]}; background-color: {colors["card"]};"
        )
        self.window.card.step2_desc.setStyleSheet(f"font-size: {font_medium}px; color: {colors["text"]}; background-color: {colors["card"]};")
        
        self.window.card.disclaimer_icon.setStyleSheet(f"background-color: {colors["card"]}; font-size: {font_medium}px;")
        self.window.card.disclaimer_text.setStyleSheet(f"background-color: {colors["card"]}; color: {colors["text"]}; font-size: {font_medium}px;")
        
        self.window.card.step3_label.setStyleSheet(
            f"font-weight: bold; font-size: {font_large}px; color: {colors["text"]}; background-color: {colors["card"]};"
        )
        self.window.card.step3_desc.setStyleSheet(f"font-size: {font_medium}px; color: {colors["text"]}; background-color: {colors["card"]};")
        
        self.window.card.sort_label.setStyleSheet(f"background-color: {colors["card"]}; font-size: {font_medium}px;")
        
        self.window.card.sort_by.setStyleSheet(
            f"""
                QComboBox {{
                    background-color: {colors["background"]};
                    padding: 5px 10px;
                    font-size: {font_medium}px;
                }}
                QComboBox QAbstractItemView {{
                    background-color: {colors["background"]};
                    color: {colors['text']};
                    font-size: {font_medium}px;
                }}
            """
        )