# -*- coding: utf-8 -*-
"""ensembleBreast_Cancer_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Okz_-mWeM4gZEshCUa08d4-1xSvTCt0e

# Loading all the necessary packages
"""

import os
import shutil, sys
from os import listdir
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import imread

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import zipfile

from google.colab import drive
drive.mount('/content/drive')

zip_path = '/content/drive/MyDrive/IDC_regular_ps50_idx5.zip'
unzip_dir = '/content/unzipped'
os.makedirs(unzip_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(unzip_dir)

filename2 = '/content/unzipped/IDC_regular_ps50_idx5'
breastHist_imgs2 = listdir(filename2)
print("Length of the folder: ", len(breastHist_imgs2))
print("Five five files and directories: ",breastHist_imgs2[0:5])

# This would print first five of the files and directories

print(breastHist_imgs2[0:5])

total_imgs = 0 # set count to 0;
subdision = [0,1]

for i in range(len(breastHist_imgs2)):
    patient_folder = breastHist_imgs2[i]
    # Check if the item is a directory before proceeding
    if os.path.isdir(os.path.join(filename2, patient_folder)):
        for x in subdision:
            # Use os.path.join to correctly concatenate paths
            patients = os.path.join(filename2, patient_folder)
            classes_path = os.path.join(patients, str(x)) # concanating file path
            subdivision_imgs = listdir(classes_path)
            sub_tot_imgs = len(subdivision_imgs)
            print(patient_folder + "/" + str(x), "Number of images:",  + sub_tot_imgs)
            total_imgs += len(subdivision_imgs)

print("The total number of images:", total_imgs)

"""# Started Copying from here"""

breastcancer_ds = pd.DataFrame(index=np.arange(0, total_imgs), columns=["patient_id", "path", "target"])

n = 0 # set count to 0;
subdision = [0,1]

for i in range(len(breastHist_imgs2)):
    patient_folder = breastHist_imgs2[i]
    # Check if the item is a directory before proceeding
    # This condition now also excludes '.DS_Store'
    if os.path.isdir(os.path.join(filename2, patient_folder)) and patient_folder != '.DS_Store':
        patients = os.path.join(filename2, patient_folder) # Corrected path concatenation
        for x in subdision:
            # Use os.path.join to correctly concatenate paths
            classes_path = os.path.join(patients, str(x)) # Corrected path concatenation
            subdivision_imgs = listdir(classes_path)
            for m in range(len(subdivision_imgs)):
                image_path = subdivision_imgs[m]
                breastcancer_ds.iloc[n]["path"] = classes_path + "/" + image_path # Added missing '/' in path
                breastcancer_ds.iloc[n]["target"] = x
                breastcancer_ds.iloc[n]["patient_id"] = patient_folder
                n += 1

breastcancer_ds.tail()

breastcancer_ds.head()

cancer_perc = breastcancer_ds.groupby("patient_id").target.value_counts() / breastcancer_ds.groupby("patient_id").target.size()
canxer_perc = cancer_perc.unstack()

canxer_perc.head()

cancer_class_perc = breastcancer_ds.groupby(["patient_id", "target"]).target.size().groupby(level=0).apply(
    lambda x: 100*x/float(x.sum()))

# Drop the existing 'patient_id' column
cancer_class_perc = cancer_class_perc.droplevel(0)

cancer_class_perc = cancer_class_perc.reset_index(name='percentage')

cancer_class_perc.head()

breastcancer_ds.groupby("target").size()

fig, [ax1, ax2] = plt.subplots(nrows=1, ncols=2, figsize=(20,5))

sns.countplot(x='target', data=breastcancer_ds,
              facecolor = (0,0,0,0),
              linewidth = 2,
              edgecolor = sns.color_palette("deep", 5), ax=ax1)
ax1.set_title("How many patches depict the level of IDC?")
ax1.set_xlabel("levels \n\n Note: 0(no) and 1(yes)")
ax1.set_ylabel("levels vs count")


sns.distplot(cancer_class_perc.iloc[:,-1:], color="red", kde=False, bins=25, ax=ax2)
ax2.set_title("Percentage of image covered by IDC?")
ax2.set_xlabel("percent of patches with IDC")
ax2.set_ylabel("count")

cancer_cells = np.random.choice(breastcancer_ds[breastcancer_ds.target == 1].index.values, size=20, replace=False)

fig, ax = plt.subplots(4, 5, figsize=(10, 10))

for a in range(4):
    for b in range(5):
        index = cancer_cells[b + 5*a]
        imgs = imread(breastcancer_ds.loc[index, 'path'])
        ax[a,b].imshow(imgs)
        ax[a,b].grid(False)

non_cancer_cells = np.random.choice(breastcancer_ds[breastcancer_ds.target == 0].index.values, size=20, replace=False)

fig, ax = plt.subplots(4, 5, figsize=(10, 10))

for a in range(4):
    for b in range(5):
        index = non_cancer_cells[b + 5*a]
        imgs = imread(breastcancer_ds.loc[index, 'path'])
        ax[a,b].imshow(imgs)
        ax[a,b].grid(False)

"""## Preparing the dataset

"""

images_cancer = 'root_cancerIDC_dir'
verify_folder = os.path.isdir(images_cancer)

if not verify_folder:
    os.makedirs(images_cancer)
else:
    pass

import glob
patients = breastHist_imgs2

for patient in patients:
    path_0 = 0
    path_1 = 1
    path = "/content/unzipped/IDC_regular_ps50_idx5/" # Added trailing slash and corrected path

    # Using os.path.join to construct paths correctly
    source = os.path.join(path, str(patient), str(path_0))
    dest = os.path.abspath(images_cancer)
    for file in glob.iglob(os.path.join(source, '**', '*.png'), recursive=True):
        shutil.copy(file, dest)

    source2 = os.path.join(path, str(patient), str(path_1))
    dest2 = os.path.abspath(images_cancer)
    for file in glob.iglob(os.path.join(source2, '**', '*.png'), recursive=True):
        shutil.copy(file, dest2)

print("Total number of images:", len(listdir(images_cancer)))

all_images = os.listdir(images_cancer)
df_all_images = pd.DataFrame(all_images, columns=['img_id'])

df_all_images.head()

df_all_images.tail()

import re

def retrieve_lastDigit(x):
    y = x[x.rindex('_')+1:]
    result = re.sub("\D", "", y)

    return result

# creating new column named patient_id
df_all_images['patient_num'] = df_all_images['img_id'].map(lambda x: x.split('_')[0])
df_all_images['target'] =  df_all_images['img_id'].apply(retrieve_lastDigit)

df_all_images.head()

df_all_images['target'] =df_all_images['target'].astype(str).astype(int)

df_all_images['target'].value_counts()

n = 78786

df_all_images_0 = df_all_images[df_all_images['target'] == 0].sample(n, random_state=234)
df_all_images_1 = df_all_images[df_all_images['target'] == 1].sample(n, random_state=234)

#del df_sample_images
df_all_images = pd.concat([df_all_images_0, df_all_images_1], axis=0).reset_index(drop=True)

#count
df_all_images['target'].value_counts()

# Making folders

base_split_dir = 'base_split_dir'
base_test_dir = 'base_test_dir'
base_train_dir = 'base_train_dir'
no_idc = 'no_idc'
yes_idc = 'yes_idc'


verify_folder2 = os.path.isdir(base_split_dir)

if not verify_folder2:
    os.makedirs(base_split_dir)
else:
    pass

os.makedirs(os.path.join(base_split_dir, base_train_dir))
os.makedirs(os.path.join(base_split_dir, base_test_dir))

os.makedirs(os.path.join(base_split_dir + '/' + base_train_dir, yes_idc))
os.makedirs(os.path.join(base_split_dir + '/' + base_train_dir, no_idc))

os.makedirs(os.path.join(base_split_dir + '/' + base_test_dir, yes_idc))
os.makedirs(os.path.join(base_split_dir + '/' + base_test_dir, no_idc))

Y = df_all_images['target']
df_train, df_test = train_test_split(df_all_images, test_size=0.25, random_state=123, stratify=Y)
print(df_train.shape)
print(df_test.shape)

train_lst = list(df_train['img_id'])
test_lst = list(df_test['img_id'])

# Transfering the train images
for img in train_lst:
    try:
        target = df_all_images.loc[df_all_images['img_id']==img,'target'].values[0]
        label = 'no_idc' if (target == 0) else 'yes_idc'
        x = os.path.abspath(images_cancer)
        src = os.path.join(x, img)
        y = os.path.abspath(base_split_dir)
        dest = os.path.join(y, base_train_dir, label, img)
        shutil.move(src, dest)
    except:
        continue

for img in test_lst:
    try:
        target = df_all_images.loc[df_all_images['img_id']==img,'target'].values[0]
        label = 'yes_idc' if (target == 1) else 'no_idc'
        a = os.path.abspath(images_cancer)
        src1 = os.path.join(a, img)
        b = os.path.abspath(base_split_dir)
        dest1 = os.path.join(b, base_test_dir, label, img)
        shutil.move(src1, dest1)
    except:
        continue





print(len(os.listdir('base_split_dir/base_train_dir/no_idc')))
print(len(os.listdir('base_split_dir/base_test_dir/yes_idc')))

num_train_samples = len(df_train)
num_test_samples = len(df_test)

batch_size = 32
IMAGE_SIZE = 50

train_steps = int(np.ceil(num_train_samples / batch_size))
test_steps = int(np.ceil(num_test_samples / batch_size))

datagen = ImageDataGenerator(rescale = 1.0 / 255,
                             rotation_range=40,
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             shear_range=0.2,
                             zoom_range=0.2,
                             horizontal_flip=True,
                             vertical_flip=True,
                             fill_mode='nearest')

train_gen = datagen.flow_from_directory('base_split_dir/base_train_dir',
                                        target_size=(IMAGE_SIZE,IMAGE_SIZE),  # all images will be resized to 50x50
                                        batch_size=batch_size,
                                        class_mode='categorical')


val_gen = datagen.flow_from_directory('base_split_dir/base_test_dir',
                                        target_size=(IMAGE_SIZE,IMAGE_SIZE),
                                        batch_size=batch_size,
                                        class_mode='categorical')

validation_generator = datagen.flow_from_directory('base_split_dir/base_test_dir',
                                                        target_size=(IMAGE_SIZE,IMAGE_SIZE),
                                                        batch_size=1,
                                                        class_mode='categorical',
                                                        shuffle=False)

import torch
import torch.nn as nn
import timm
import numpy as np
import random
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score

# ------------------------------
# Setup
# ------------------------------
def set_seed(seed=42):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True

class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.ce = nn.CrossEntropyLoss(reduction='none')
    def forward(self, inputs, targets):
        ce_loss = self.ce(inputs, targets)
        pt = torch.exp(-ce_loss)
        return self.alpha * ((1 - pt) ** self.gamma * ce_loss).mean()

# ------------------------------
# Soft Voting Ensemble Evaluation
# ------------------------------
def evaluate_ensemble_soft(models, dataloader, device):
    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            logits_sum = sum([model(images) for model in models]) / len(models)
            preds = torch.argmax(logits_sum, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    acc = accuracy_score(all_labels, all_preds)
    return acc

# ------------------------------
# Training Function
# ------------------------------
def train_model(model_name, train_loader, val_loader, save_path, device, epochs=20):
    model = timm.create_model(model_name, pretrained=True, num_classes=2).to(device)
    criterion = FocalLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'max', patience=3, factor=0.5)
    best_val_acc = 0

    for epoch in range(epochs):
        model.train()
        correct, total = 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
        train_acc = correct / total

        model.eval()
        val_correct = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, preds = torch.max(outputs, 1)
                val_correct += (preds == labels).sum().item()
        val_acc = val_correct / len(val_loader.dataset)
        scheduler.step(val_acc)

        print(f"{model_name} | Epoch {epoch+1} - Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), save_path)
            print(f"Saved best model for {model_name} with Val Acc: {val_acc:.4f}")
    return model

# Setup
set_seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Transforms
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomRotation(30),
    transforms.ColorJitter(0.2, 0.2),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.ToTensor(),
    transforms.RandomErasing(p=0.2),
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Load Datasets
train_dataset = datasets.ImageFolder("base_split_dir/base_train_dir", transform=train_transform)
val_dataset = datasets.ImageFolder("base_split_dir/base_test_dir", transform=val_transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)

models = []
model_names = ["efficientnet_b3", "convnext_tiny", "swin_tiny_patch4_window7_224"]
model_paths = ["efficientnet_b3_soft.pth", "convnext_tiny_soft.pth", "swin_tiny_soft.pth"]

# Train each model and save
for name, path in zip(model_names, model_paths):
    model = train_model(name, train_loader, val_loader, path, device)
    models.append(model)

# Final ensemble evaluation
ensemble_acc = evaluate_ensemble_soft(models, val_loader, device)
print(f"\n✅ Ensemble Accuracy (Soft Voting): {ensemble_acc:.4f}")

from torchvision.transforms.functional import hflip, vflip, rotate
def tta_predict(model, image, device):
    image = image.unsqueeze(0).to(device)
    variants = [
        image,
        hflip(image),
        vflip(image),
        rotate(image, 90),
        rotate(image, 180),
        rotate(image, 270)
    ]
    with torch.no_grad():
        outputs = [model(v) for v in variants]
        return torch.stack(outputs).mean(0)

def evaluate_ensemble_tta(models, dataloader, device):
    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in dataloader:
            for i in range(images.size(0)):
                img = images[i]
                label = labels[i].item()
                logits = sum([tta_predict(model, img, device) for model in models]) / len(models)
                pred = torch.argmax(logits, dim=1).item()
                all_preds.append(pred)
                all_labels.append(label)
    acc = accuracy_score(all_labels, all_preds)
    return acc

# Data loader (same transform as training except no augmentation)
val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])
val_dataset = datasets.ImageFolder("base_split_dir/base_test_dir", transform=val_transform)
val_loader = DataLoader(val_dataset, batch_size=32)

# Load saved models
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_names = ["efficientnet_b3", "convnext_tiny", "swin_tiny_patch4_window7_224"]
model_paths = ["efficientnet_b3_soft.pth", "convnext_tiny_soft.pth", "swin_tiny_soft.pth"]

models = []
for name, path in zip(model_names, model_paths):
    model = timm.create_model(name, pretrained=False, num_classes=2)
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device)
    model.eval()
    models.append(model)

# Run TTA Ensemble Evaluation
tta_acc = evaluate_ensemble_tta(models, val_loader, device)
print(f"\n✅ TTA Ensemble Accuracy: {tta_acc:.4f}")

!pip install grad-cam

import torch
import timm
import numpy as np
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget

# ------------------------------------------------------------
# LOAD MODEL FUNCTION
# ------------------------------------------------------------
def load_model(model_name, weight_path):
    model = timm.create_model(model_name, pretrained=False, num_classes=2)
    model.load_state_dict(torch.load(weight_path, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
    model.eval()
    return model

# ------------------------------------------------------------
# GRAD-CAM GENERATOR
# ------------------------------------------------------------
def generate_cam(model, target_layer, input_tensor, raw_np_image):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = model.to(device)
    cam = GradCAM(model=model.to(device), target_layers=[target_layer])
    targets = [ClassifierOutputTarget(1)]  # class 1 = IDC
    grayscale_cam = cam(input_tensor=input_tensor.to(device), targets=targets)[0]
    cam_image = show_cam_on_image(raw_np_image, grayscale_cam, use_rgb=True)
    return cam_image

# ------------------------------------------------------------
# IMAGE LOADING
# ------------------------------------------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


image_path = "base_split_dir/base_test_dir/yes_idc/10253_idx5_x551_y701_class1.png" #/content/base_split_dir/base_test_dir/yes_idc/10253_idx5_x551_y701_class1.png  # class 1 = IDC
raw_image = Image.open(image_path).convert('RGB')
input_tensor = transform(raw_image).unsqueeze(0)
input_np = np.array(raw_image.resize((224, 224))) / 255.0

# ------------------------------------------------------------
# MODEL CONFIGURATIONS
# ------------------------------------------------------------
model_configs = [
    ("efficientnet_b3", "efficientnet_b3_soft.pth"),
    ("convnext_tiny", "convnext_tiny_soft.pth"),
    ("swin_tiny_patch4_window7_224", "swin_tiny_soft.pth")
]

cams = []

# ------------------------------------------------------------
# GENERATE GRAD-CAMs
# ------------------------------------------------------------
for name, path in model_configs:
    model = load_model(name, path)
    if "efficientnet" in name:
        target_layer = model.conv_head
    elif "convnext" in name:
        target_layer = model.stages[-1].downsample
    elif "swin" in name:
        target_layer = model.norm
    cam_image = generate_cam(model, target_layer, input_tensor, input_np)
    cams.append((name, cam_image))

# ------------------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------------------
plt.figure(figsize=(18, 6))
plt.subplot(1, len(cams)+1, 1)
plt.imshow(input_np)
plt.title("Original Image")
plt.axis("off")

for i, (name, cam_img) in enumerate(cams):
    plt.subplot(1, len(cams)+1, i+2)
    plt.imshow(cam_img)
    plt.title(f"{name}")
    plt.axis("off")

plt.tight_layout()
plt.show()

from sklearn.metrics import (
    confusion_matrix, classification_report,
    roc_auc_score, roc_curve, auc,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt
import torch
import timm
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_names = ["efficientnet_b3", "convnext_tiny", "swin_tiny_patch4_window7_224"]
model_paths = ["efficientnet_b3_soft.pth", "convnext_tiny_soft.pth", "swin_tiny_soft.pth"]

models = []
for name, path in zip(model_names, model_paths):
    model = timm.create_model(name, pretrained=False, num_classes=2)
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device).eval()
    models.append(model)

from torchvision import datasets, transforms
from torch.utils.data import DataLoader

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

val_dataset = datasets.ImageFolder("base_split_dir/base_test_dir", transform=val_transform)
val_loader = DataLoader(val_dataset, batch_size=32)

all_labels = []
all_preds = []
all_probs = []

with torch.no_grad():
    for images, labels in val_loader:
        images = images.to(device)
        logits = sum([model(images) for model in models]) / len(models)
        probs = torch.softmax(logits, dim=1)
        preds = torch.argmax(probs, dim=1)

        all_labels.extend(labels.numpy())
        all_preds.extend(preds.cpu().numpy())
        all_probs.extend(probs[:, 1].cpu().numpy())  # Class 1 probabilities for AUC

# Confusion Matrix
cm = confusion_matrix(all_labels, all_preds)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Non-IDC (0)", "IDC (1)"])
disp.plot(cmap='Blues', values_format='d')
plt.title("Confusion Matrix")
plt.show()

# Classification Report
print("📋 Classification Report:\n")
print(classification_report(all_labels, all_preds, target_names=["Non-IDC", "IDC"]))

fpr, tpr, thresholds = roc_curve(all_labels, all_probs)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic")
plt.legend(loc="lower right")
plt.grid()
plt.show()

from sklearn.metrics import precision_recall_curve, average_precision_score
precision, recall, _ = precision_recall_curve(all_labels, all_probs)
avg_precision = average_precision_score(all_labels, all_probs)

plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color="darkorange", lw=2, label=f'AP = {avg_precision:.4f}')
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve for IDC Classification")
plt.legend(loc="lower left")
plt.grid(True)
plt.show()