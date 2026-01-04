import filecmp
import os
import cv2
import matplotlib.pyplot as plt


class DuplicateDetector:
    """Detect and manage duplicate images using file comparison"""

    def __init__(self, file_paths=None):
        self.file_paths = file_paths or []
        self.duplicates = []

    def detect_duplicates(self, show_first_n=10):
        """
        Detect duplicate files

        Args:
            show_first_n: Number of duplicate pairs to visualize
        """

        duplicates = []
        counter = 0
        total_files = len(self.file_paths)

        print(f"\nChecking {total_files} files for duplicates...")

        for file1 in self.file_paths:
            if file1 in duplicates:
                continue

            counter += 1
            if counter % 100 == 0:
                print(f"Checked {counter} out of {total_files} files")

            for file2 in self.file_paths:
                if file1 != file2 and file2 not in duplicates:
                    if filecmp.cmp(file1, file2, shallow=False):
                        duplicates.append(file2)

                        if len(duplicates) <= show_first_n:
                            self._show_duplicate_pair(file1, file2)

        self.duplicates = duplicates

        print("=" * 60)
        print(f"SUMMARY: Found {len(self.duplicates)} duplicate files")
        print("=" * 60)

    def get_unique_files(self):
        """Get list of files with duplicates removed"""
        return [f for f in self.file_paths if f not in self.duplicates]

    def remove_duplicates_from_disk(self):
        """
        PERMANENTLY delete detected duplicates from the disk.
        Before executing this method, files backup is recommended. Otherwise, duplicate files will be lost.
        """

        if not self.duplicates:
            print("No duplicates to remove")
            return

        res = input(
            f"You're about to remove {len(self.duplicates)} files from the disk.\n \
            Would you like to proceed? (yes/no):"
        )

        if res.lower() == "no" and res.lower() == "n":
            print("Operation cancelled")

        elif res.lower() == "yes" or res.lower() == "y":
            print(f"Removing {len(self.duplicates)} duplicate files...")

            for filepath in self.duplicates:
                try:
                    os.remove(filepath)
                    print(f"{filepath} removed")

                except Exception as e:
                    print(f"Error removing {filepath}: {e}")

            print("Duplicates removed")

        else:
            print("Sorry, unknown response. Operation cancelled")

    def _show_duplicate_pair(self, original_path, duplicate_path):
        """Display original and duplicate images side by side"""

        # Read images
        img1 = cv2.imread(original_path)
        img2 = cv2.imread(duplicate_path)

        _, axs = plt.subplots(1, 2, figsize=(12, 5))  # 1 row, 2 cols

        # Display original image with the title and no axis
        axs[0].imshow(img1, cmap="gray")
        axs[0].set_title("Original image")
        axs[0].axis("off")

        # Display duplicate image with the title and no axis
        axs[1].imshow(img2, cmap="gray")
        axs[1].set_title("Duplicate image")
        axs[1].axis("off")

        plt.tight_layout()
        plt.show()
