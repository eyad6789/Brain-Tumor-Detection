# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

This project runs on **Kaggle** (or a compatible environment with GPU). The dataset paths are hardcoded to Kaggle's input directory structure:

```
/kaggle/input/brain-tumor-mri-images/archive (5)/Training/
/kaggle/input/brain-tumor-mri-images/archive (5)/Testing/
/kaggle/input/brain-tumor-mri-images/Prediction check images/...
```

To run locally, update these three path variables at the top of the notebook (`trainpath`, `testpath`, `pred`).

## Running the Notebook

```bash
jupyter notebook brain-tumor.ipynb
# or
jupyter lab brain-tumor.ipynb
```

Run cells sequentially — later cells depend on variables defined in earlier ones (e.g., `X_train`, `X_test`, `x_pred`, `model`).

## Architecture

Single Jupyter notebook (`brain-tumor.ipynb`) with this pipeline:

1. **Data loading** — reads MRI `.jpg` images from class-named subdirectories using `glob`, resizes to 224×224, encodes labels as integers (`pituitary=0, notumor=1, meningioma=2, glioma=3`)
2. **Model** — ResNet50 pretrained on ImageNet (`include_top=False`), first 80 layers frozen, remaining layers fine-tuned. Custom head: `Flatten → Dropout(0.5) → Dense(512, relu) → Dropout(0.3) × 2 → Dense(4, softmax)`
3. **Training** — Adam (lr=0.0001), `sparse_categorical_crossentropy`, 7 epochs, batch size 32. Callbacks: `ModelCheckpoint` (saves best to `model_class.h5`), `CSVLogger` (writes `model_log.csv`), `EarlyStopping(patience=5)`
4. **Prediction** — loads saved `model_class.h5`, runs inference on `X_test` and the 16 standalone prediction images in `x_pred`

## Dataset

Kaggle: [Brain Tumor MRI Images](https://www.kaggle.com/) — 4 classes: `glioma`, `meningioma`, `notumor`, `pituitary`. Training set: 5712 images; test set: 1311 images.

## Key Results

Best validation accuracy: **~98.47%** | Test accuracy: **98.47%** | Test loss: **0.0475**

## Dependencies

```
numpy, pandas, matplotlib, opencv-python (cv2), pillow (PIL), tensorflow (≥2.x)
```
