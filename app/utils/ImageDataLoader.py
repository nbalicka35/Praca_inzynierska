import os


class ImageDataLoader:
    """Handles loading and organizing file paths from dataset directories"""

    def __init__(self, train_dir=None, val_dir=None, test_dir=None):
        self.train_dir = train_dir
        self.val_dir = val_dir
        self.test_dir = test_dir
        self.file_paths = []

    def set_train_dir(self, train_dir):
        """Set training directory path"""
        self.train_dir = train_dir

    def set_val_dir(self, val_dir):
        """Set validation directory path"""
        self.val_dir = val_dir

    def set_test_dir(self, test_dir):
        """Set testing directory path"""
        self.test_dir = test_dir

    def load_all_images(self):
        """
        Load all .jpg image paths from training and testing directories

        Returns:
            List of file paths
        """
        try:
            file_paths = []

            # Load from training directory
            train_subdirs = [f.path for f in os.scandir(self.train_dir) if f.is_dir()]
            for subdir in train_subdirs:
                for filename in os.listdir(subdir):
                    if filename.lower().endswith((".jpg", ".jpeg")):
                        file_paths.append(os.path.join(subdir, filename))

            if self.val_dir is not None:
                # Load from validation directory
                val_subdirs = [f.path for f in os.scandir(self.val_dir) if f.is_dir()]
                for subdir in val_subdirs:
                    for filename in os.listdir(subdir):
                        if filename.lower().endswith((".jpg", ".jpeg")):
                            file_paths.append(os.path.join(subdir, filename))

            # Load from testing directory
            test_subdirs = [f.path for f in os.scandir(self.test_dir) if f.is_dir()]
            for subdir in test_subdirs:
                for filename in os.listdir(subdir):
                    if filename.lower().endswith((".jpg", ".jpeg")):
                        file_paths.append(os.path.join(subdir, filename))

            self.file_paths = file_paths
        except Exception as e:
            print(
                f"An error has occured during DataLoader.load_all_images() method execution: {e}"
            )
            return ""

        return file_paths

    def print_dataset_class_count(self):
        """
        Print dataset structure with class counts for training and testing directories

        Displays:
            - Number of images per class in Training folder
            - Number of images per class in Testing folder
        """
        out = ""
        if self.val_dir is not None:
            subdirs = [self.train_dir, self.val_dir, self.test_dir]
        else:
            subdirs = [self.train_dir, self.test_dir]

        for subdir in subdirs:
            folder_name = os.path.basename(subdir)
            out += f"{folder_name} folder details:\n"

            classes = os.listdir(subdir)

            for cl in classes:
                class_path = os.path.join(subdir, cl)

                if not os.path.isdir(class_path):
                    continue

                files = os.listdir(class_path)
                counter = sum(
                    1
                    for f in files
                    if os.path.isfile(os.path.join(class_path, f))
                    and (f.endswith((".jpg", ".jpeg")))
                )

                out += f"\t{cl}: {counter} images\n"

        print(out)
