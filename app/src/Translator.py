import os

class Translator:
    TEXTS = {
        "EN": {
            "open_file": "Open File",
            "select_folder": "Select Directory",
            "probability": "probability",
            "original": "Original",
            "heatmap": "GradCAM Heatmap",
            "overlay": "Overlay",
            "prediction": "Prediction",
            "gradcam_title": "GradCAM for",
            "selected": "Selected",
            "selected_images": "Selected {count} images from {folder}",
            "no_jpg": "No .jpg files found in {folder}",
            "thinking": "Thinking...",
            "images": "images",
            "sort_by": "Sort by:",
            "sort_default": "Default order",
            "sort_filename_az": "Filename A-Z",
            "sort_filename_za": "Filename Z-A",
            "sort_class_az": "Class A-Z",
            "sort_class_za": "Class Z-A",
            "sort_prob_asc": "Probability ⬆️",
            "sort_prob_desc": "Probability ⬇️",
            "meningioma_tumor": "Meningioma Tumor",
            "glioma_tumor": "Glioma Tumor",
            "pituitary_tumor": "Pituitary Tumor",
            "no_tumor": "No Tumor",
            "image_load_failed": "Image loading failed",
            "could_not_load": "Could not load the image",
            "visualization_error": "Visualization error has occurred",
        },
        "PL": {
            "open_file": "Wybierz plik",
            "select_folder": "Wybierz folder",
            "probability": "prawdopodobieństwa",
            "original": "Oryginał",
            "heatmap": "Mapa ciepła GradCAM",
            "overlay": "Nałożenie",
            "prediction": "Predykcja",
            "gradcam_title": "GradCAM dla",
            "selected": "Wybrano",
            "selected_images": "Wybrano {count} obrazów z {folder}",
            "no_jpg": "Brak plików .jpg w {folder}",
            "thinking": "Myślę...",
            "images": "obrazów",
            "sort_by": "Sortuj:",
            "sort_default": "Domyślnie",
            "sort_filename_az": "Nazwa pliku A-Z",
            "sort_filename_za": "Nazwa pliku Z-A",
            "sort_class_az": "Klasa A-Z",
            "sort_class_za": "Klasa Z-A",
            "sort_prob_asc": "Prawdopodobieństwo ⬆️",
            "sort_prob_desc": "Prawdopodobieństwo ⬇️",
            "meningioma_tumor": "Oponiak",
            "glioma_tumor": "Glejak",
            "pituitary_tumor": "Guz Przysadki",
            "no_tumor": "Brak guza",
            "image_load_failed": "Załadowanie obrazu nie powiodło się",
            "could_not_load": "Błąd podczas ładowania obrazu",
            "visualization_error": "Wystąpił błąd wizualizacji",
        }
    }

    def __init__(self, language, window):
        self.current_lang = language
        self.current_window = window
        print(f"Translator init with language: {language}")
            
    def apply(self):
        if self.current_lang == "PL":
            print("Calling set_polish()")
            self.set_polish()

        elif self.current_lang == "EN":
            print("Calling set_english()")
            self.set_english()
            
    def get_text(self, key, **kwargs):
        text = self.TEXTS[self.current_lang].get(key)
        if kwargs:
            text = text.format(**kwargs)
            
        return text

    def set_polish(self):
        print("set_polish() executing")
        self.current_window.card.step1_label.setText("Krok 1")
        self.current_window.card.step1_desc.setText(
            "Wybierz plik(i) JPG lub ścieżkę z obrazami"
        )
        
        if self.current_window.selected_file is not None:
            self.current_window.card.file_name_label.setText(f"{self.get_text("selected")}: {os.path.basename(self.current_window.selected_file)}")
        elif len(self.current_window.selected_files) > 0:
            if self.current_window.selected_directory is not None:
                self.current_window.card.file_name_label.setText(
                    self.get_text("selected_images", count = len(self.current_window.selected_files),
                    folder = os.path.basename(self.current_window.selected_directory))
                )
            else:
                self.current_window.card.file_name_label.setText(f"{self.get_text("selected")}: {len(self.current_window.selected_files)} {self.get_text('images')}")

        self.current_window.card.file_button.setText("Wybierz plik(i)")
        self.current_window.card.dir_button.setText("Wybierz folder")

        self.current_window.card.preview_label.setText(
            "Podgląd obrazu/obrazów pojawi się poniżej"
        )
        self.current_window.card.clear_button.setText("Wyczyść")

        self.current_window.card.step2_label.setText("Krok 2")
        self.current_window.card.step2_desc.setText("Poddaj obraz(y) ocenie")

        self.current_window.card.predict_button.setText("Uruchom")

        self.current_window.card.disclaimer_text.setText(
            "Neuron to oprogramowanie stworzone z myślą o wsparciu lekarzy i radiologów w diagnozowaniu\n"
            "guzów mózgu i może popełniać błędy.\n"
            "Zawsze poddawaj pacjentów diagnozie i podejmuj decyzje w oparciu o własną wiedzę i doświadczenie."
        )

        self.current_window.card.step3_label.setText("Krok 3")
        self.current_window.card.step3_desc.setText(
            "Poniżej sprawdź otrzymane wyniki dla obrazu/obrazów"
        )
        
        self.current_window.card.sort_label.setText("Sortuj: ")

    def set_english(self):
        print("set_english() executing")
        self.current_window.card.step1_label.setText("Step 1")
        self.current_window.card.step1_desc.setText("Select JPG file(s) or directory")
        
        if self.current_window.selected_file is not None:
            self.current_window.card.file_name_label.setText(f"{self.get_text("selected")}: {os.path.basename(self.current_window.selected_file)}")
        elif len(self.current_window.selected_files) > 0:
            if self.current_window.selected_directory is not None:
                self.current_window.card.file_name_label.setText(
                    self.get_text("selected_images", count = len(self.current_window.selected_files),
                    folder = os.path.basename(self.current_window.selected_directory))
                )
            else:
                self.current_window.card.file_name_label.setText(f"{self.get_text("selected")}: {len(self.current_window.selected_files)} {self.get_text('images')}")


        self.current_window.card.file_button.setText("Choose file(s)")
        self.current_window.card.dir_button.setText("Choose directory")

        self.current_window.card.preview_label.setText(
            "Preview of selected image(s) will appear below"
        )
        self.current_window.card.clear_button.setText("Clear")

        self.current_window.card.step2_label.setText("Step 2")
        self.current_window.card.step2_desc.setText("Examine image(s)")

        self.current_window.card.predict_button.setText("Predict")

        self.current_window.card.disclaimer_text.setText(
            "Please note that Neuron is a software designed to support physicians and radiologists, and can make mistakes.\n"
            "Always examine patients and make a decision based on the knowledge of yours."
        )

        self.current_window.card.step3_label.setText("Step 3")
        self.current_window.card.step3_desc.setText(
            "Check the result for the photo(s) below"
        )
        
        self.current_window.card.sort_label.setText("Sort by:")
