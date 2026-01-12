class Translator:
    CLASSES = {
        "Meningioma Tumor": "Oponiak",
        "Glioma Tumor": "Glejak",
        "Pituitary Tumor": "Guz Przysadki",
        "No Tumor": "Brak Guza",
    }

    def __init__(self, language, window):
        self.current_lang = language
        self.current_window = window
        print(f"Translator init with language: {language}")

        if self.current_lang == "PL":
            print("Calling set_polish()")
            self.set_polish()

        elif self.current_lang == "EN":
            print("Calling set_english()")
            self.set_english()

    def set_polish(self):
        print("set_polish() executing")
        self.current_window.card.step1_label.setText("Krok 1")
        self.current_window.card.step1_desc.setText(
            "Wybierz plik(i) JPG lub ścieżkę z obrazami"
        )

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
        self.current_window.card.step1_desc.setText("Select .jpg file or directory")

        self.current_window.card.file_button.setText("Choose file")
        self.current_window.card.dir_button.setText("Choose directory")

        self.current_window.card.preview_label.setText(
            "Preview of selected image(s) will appear below"
        )
        self.current_window.card.clear_button.setText("Clear")

        self.current_window.card.step2_label.setText("Step 2")
        self.current_window.card.step2_desc.setText("Examine photo(s)")

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
