# ML Dataset Attributions

## Approved Datasets

### hf_100crops — Open-Source Crop/Plant Object Detection Dataset

- **Dataset ID**: hf_100crops
- **Source**: Hugging Face / devshaheen
- **URL**: https://huggingface.co/datasets/devshaheen/100_crops_plants_object_detection_25k_image_dataset
- **License**: MIT
- **Attribution Required**: No (MIT does not require attribution, but preserving copyright notice is good practice)
- **Domain**: CROP / PLANT ID
- **Approved Images**: 3,489
- **Notes**: Object detection dataset with 100 crop/plant classes. Images are primarily real-world photographs.

### hf_digigreen — Crop Disease Expert Annotations

- **Dataset ID**: hf_digigreen
- **Source**: Hugging Face / DigiGreen
- **URL**: https://huggingface.co/datasets/DigiGreen/Crop_Disease_Images
- **License**: CC BY 4.0
- **Attribution Required**: Yes
- **Attribution Text**: DigiGreen / Digital Green
- **Domain**: DISEASE / DISORDER
- **Approved Images**: 414
- **Notes**: Expert annotations over farmer-submitted photographs from India. Real-world field images.

### hf_food_ingredients_v2 — Food Ingredients Dataset

- **Dataset ID**: hf_food_ingredients_v2
- **Source**: Hugging Face / Sunny
- **URL**: https://www.kaggle.com/datasets/sunnyagarwal427444/food-ingredient-dataset-51
- **License**: CC BY 4.0
- **Attribution Required**: Yes
- **Attribution Text**: Sunny Agarwal
- **Domain**: CROP / PLANT ID
- **Approved Images**: 493
- **Notes**: Food ingredient images. Some classes are food items rather than garden plants.

### hf_food_veg — Fruits and Vegetables Dataset

- **Dataset ID**: hf_food_veg
- **Source**: Hugging Face / Sunny Agarwal
- **URL**: https://huggingface.co/datasets/SunnyAg/fruits_and_vegetables_dataset
- **License**: Apache-2.0
- **Attribution Required**: No (Apache-2.0 preserves copyright notice but does not require attribution)
- **Domain**: CROP / PLANT ID
- **Approved Images**: 1,099
- **Notes**: Fruits and vegetables classification dataset. Mix of food and garden-relevant classes.

### hf_veg_bangladesh — Vegetable Classification Banglades

- **Dataset ID**: hf_veg_bangladesh
- **Source**: Hugging Face / Ahmed et al.
- **URL**: https://huggingface.co/datasets/MdJobayerAhmed/BanglaVeg
- **License**: CC BY 4.0
- **Attribution Required**: Yes
- **Attribution Text**: Ahmed, Md Jobayer; Saha, Ratu; Dutta, Arpon Kishore; Mojumdar, Mayen Uddin; Chakraborty, Narayan Ranjan
- **Domain**: CROP / PLANT ID
- **Approved Images**: 3,066
- **Notes**: Vegetable images from Bangladesh. Real-world field/garden photographs.

### zenodo_vegann — VegAnn Dataset

- **Dataset ID**: zenodo_vegann
- **Source**: Zenodo / VegAnn
- **URL**: https://zenodo.org/records/8105154
- **License**: CC BY
- **Attribution Required**: Yes
- **Attribution Text**: See Zenodo record for authors
- **Domain**: DISEASE / DISORDER
- **Approved Images**: 407
- **Notes**: Vegetation segmentation dataset. RGB images with binary masks. Useful for vegetation/plant detection, but primary purpose is segmentation.

## Rejected Datasets

### hf_plantvillage — PlantVillage Dataset

- **License**: CC BY-SA 3.0
- **Reason for Rejection**: Share-alike license is incompatible with commercial distribution.
- **Note**: Contains 24,723 valid images of plant diseases. High quality but license prevents commercial use.

### hf_food_ingredients — Food Ingredients Dataset

- **License**: Unknown
- **Reason for Rejection**: No license information found. Commercial use cannot be established.

### hf_fruit_veg — Fruit and Vegetables Dataset

- **License**: Unknown
- **Reason for Rejection**: No license information found in README or metadata.

### hf_smartharvest — SmartHarvest

- **License**: Unknown
- **Reason for Rejection**: No license information found. Only Apple class with 744 images.

## No-Image Datasets (Placeholders Only)

These datasets were downloaded as placeholders or have no extractable images:

- bangladesh_veg — manifest only, needs manual download
- early_stage_crops — manifest only, needs manual download
- hf_better_imagenet — no images extracted
- hf_cache — Hugging Face cache, not a dataset
- hf_food27 — no images extracted (parquet format not processed)
- hf_pick_veg — no images extracted
- hf_pick_veg_outlined — no images extracted
- smartphone_veg — manifest only, needs manual download
- USDA_ARS — manifest only, needs manual download
- zenodo_olid — no images extracted
