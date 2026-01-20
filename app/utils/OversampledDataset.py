from torch.utils.data import Dataset
from torchvision import datasets
from PIL import Image


class OversampledDataset(Dataset):
    """Dataset with oversampling for minority classes"""

    def __init__(self, root_dir, transform, indices=None):
        self.transform = transform

        original = datasets.ImageFolder(root_dir)
        self.classes = original.classes

        if indices is not None:
            base_samples = [original.samples[i] for i in indices]

        else:
            base_samples = original.samples

        class_counts = [0] * len(self.classes)
        for _, label in base_samples:
            class_counts[label] += 1

        max_count = max(class_counts)

        self.samples = []
        for path, label in base_samples:
            repeat = max_count // class_counts[label]

            for _ in range(repeat):
                self.samples.append((path, label))
         
        lbl = "no_tumor"       
        current_count = sum(1 for _, l in self.samples if l == lbl)
        need = max_count-current_count
        
        if need > 0:            
            lbl_paths = [p for p, l in base_samples if l == lbl]
            for i in range(need):
                self.samples.append((lbl_paths[i % len(lbl_paths)], lbl))

        print(f"Before oversampling: {len(base_samples)}")
        print(f"After oversampling: {len(self.samples)}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        path, label = self.samples[index]
        img = Image.open(path).convert("RGB")
        img = self.transform(img)

        return img, label

    def print_class_distribution(self):
        """Print number of samples per class after oversampling"""
        class_counts = [0] * len(self.classes)

        for _, label in self.samples:
            class_counts[label] += 1

        print("Class distribution after oversampling:")
        for idx, count in enumerate(class_counts):
            print(f"  {self.classes[idx]}: {count} images")
