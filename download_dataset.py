"""
Downloads the Brain Tumor MRI dataset from Kaggle using kagglehub.
No API key file needed — kagglehub handles auth automatically.
"""

import kagglehub

path = kagglehub.dataset_download("adityakomaravolu/brain-tumor-mri-images")
print("Path to dataset files:", path)

# Expected structure inside path:
#   archive (5)/
#     Training/  -> glioma/, meningioma/, notumor/, pituitary/
#     Testing/   -> glioma/, meningioma/, notumor/, pituitary/
