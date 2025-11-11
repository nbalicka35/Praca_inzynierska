import filecmp
import os
from exploratory_analysis import *
import matplotlib.image as mpimg
import numpy as np

class DuplicateDetector:
    def __init__(self, files = None):
        self.files = files
        self.duplicates = None

    def _set_duplicates(self, duplicates):
        self.duplicates = duplicates

    def _set_files(self, files):
        self.files = files

    def detect_duplicates(self):
        duplicates = []
        counter = 0
        for file1 in self.files:
            if file1 in duplicates:
                continue
            counter += 1
            print(f"Checking {counter}th file out of {len(self.files)} files")
            for file2 in self.files:
                if file1 != file2 and file2 not in duplicates:
                    res = filecmp.cmp(file1, file2, shallow=False)

                    if res:
                        duplicates.append(file2)
                        if len(duplicates) < 11:
                            show_original_and_duplicated(file1, file2)
        print(f"Detected {len(duplicates)} duplicates")
        self.duplicates = duplicates
        return duplicates

    def clear_file_list(self):
        return [file for file in self.files if file not in self.duplicates]

    def remove_duplicates(self):
        for duplicate in self.duplicates:
            os.remove(duplicate)


def show_image(dir, caption):
    img = cv2.imread(dir)
    cv2.imshow(caption, img)
    cv2.waitKey(0)


def show_original_and_duplicated(dir1, dir2):
    img1 = mpimg.imread(dir1)
    img2 = mpimg.imread(dir2)

    fig, axs = plt.subplots(1, 2)
    axs[0].title.set_text('Original image')
    axs[0].imshow(img1)
    axs[1].title.set_text('Duplicated image')
    axs[1].imshow(img2)
    plt.show()


def print_class_count(dataset_dir):
    out = ""
    subdirs = os.listdir(dataset_dir)

    for subdir in subdirs:
        subdir_path = os.path.join(dataset_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        out += f"{subdir} folder details:\n"

        classes = os.listdir(subdir_path)

        for cl in classes:
            class_path = os.path.join(subdir_path, cl)
            if not os.path.isdir(class_path):
                continue

            files = os.listdir(class_path)
            counter = sum(1 for f in files if os.path.isfile(os.path.join(class_path, f)))

            out += f"\t{cl}: {counter} images\n"

    print(out)


class HelperMethods:
    def __init__(self):
        self.files = None

    def load_all_images(self, test_dir, train_dir):
        files = []

        train_subdirs = [f.path for f in os.scandir(train_dir) if f.is_dir()]
        test_subdirs = [f.path for f in os.scandir(test_dir) if f.is_dir()]

        for subdir in train_subdirs:
            for filename in os.listdir(subdir):
                if filename.endswith('.jpg'):
                    files.append(os.path.join(subdir, filename))

        for subdir in test_subdirs:
            for filename in os.listdir(subdir):
                if filename.endswith('.jpg'):
                    files.append(os.path.join(subdir, filename))
        self.files = files
        return files

    def show_sample(self):
        show_image(self.files[0], 'Brain tumor image')
        show_image(self.files[-1], 'Brain tumor image')
        show_image(self.files[1], 'Brain tumor image')
        print(f"{self.files[0]}\n{self.files[-1]}\n{self.files[1]}\n{len(self.files)}")

    def show_batch_of_images(self, batch_size=64):
        sample_size = 8  # 8 images per one row
        fig, axs = plt.subplots(batch_size // sample_size, sample_size, figsize=(12, 12))

        fig.suptitle(f"{batch_size} MRI images.", fontsize = 20)

        for row in range(batch_size // sample_size):
            for col in range(sample_size):
                image = plt.imread(self.files[row * sample_size + col])
                axs[row][col].imshow(image, aspect='equal')
                axs[row][col].axis('off')
                axs[row][col].set_aspect('equal')

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()


    def convert_images_to_gray(self):
        gray_images = []
        for f in self.files:
            gray_img = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY)
            gray_images.append(gray_img)

        return gray_images
    
def find_brightest_image(gray_images):
    max_brightness = 0
    brightest_image = None

    for image in gray_images:
        brightness = np.mean(image)
        if brightness > max_brightness:
            max_brightness = brightness
            brightest_image = image

    return brightest_image, max_brightness

def find_darkest_image(gray_images):
    min_brightness = gray_images[0]
    darkest_image = None

    for image in gray_images:
        brightness = np.mean(image)
        if brightness < min_brightness:
            min_brightness = brightness
            darkest_image = image

    return darkest_image, min_brightness


def get_dataset_mean(images):
    sum = 0
    count = 0

    for image in images:
        sum += np.sum(image)
        count += 1

    return sum / count

def get_dataset_std(images, mean = None):
    if mean is None:
        mean = get_dataset_mean(images)

    squared_dif = 0
    count = 0

    for image in images:
        squared_dif += np.sum((image - mean) ** 2)
        count += image.shape[0] * image.shape[1]

    return np.sqrt(squared_dif / count)

test_dir = './data/Testing'
train_dir = './data/Training'

helper = HelperMethods()
duplicate_detector = DuplicateDetector()

files = helper.load_all_images(test_dir, train_dir)
duplicate_detector._set_files(files)
helper.show_batch_of_images()
# show_sample(files)

#copies = duplicate_detector.detect_duplicates()
#files = duplicate_detector.clear_file_list()

print_class_count("./data")

explorator = DataExplorer(files)
explorator.retrieve_sample_of_images([0, -1, len(files) // 2])
explorator.plot_histogram(title="Images and their corresponding histograms")