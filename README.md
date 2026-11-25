# Hemolysis-CDSS-Project
# Development of a Machine Learning-Based Clinical Decision Support System for Predicting Preanalytical Specimen Hemolysis

## Project Overview
This repository contains the code, trained model, and Streamlit application for an ML-based Clinical Decision Support System (CDSS). The system predicts the likelihood of preanalytical specimen hemolysis *prior* to analysis, shifting laboratory workflows from reactive detection to proactive prevention to reduce costs and patient delays.

## Dataset
This project uses the AACC/ADLM "Help with Hemolysis" Kaggle dataset. 
* Note: The dataset must be downloaded directly from Kaggle (https://www.kaggle.com/competitions/aacc-2023-helpwithhemolysis). Place `hemolysis_index_results.csv` and `redraw_thresholds.csv` in the root directory before running the notebook.

## Methodology & Instructor Feedback Addressed
* **Models:** Logistic Regression, Decision Tree, and Random Forest.
* **Data Handling:** 
  * Grouped high-cardinality `Collector ID` into frequency buckets to prevent overfitting.
  * Implemented **leakage-safe splitting** using `GroupShuffleSplit` (grouped by Patient ID) to ensure no patient appeared in both training and test sets.
  * Applied **SMOTE** (Synthetic Minority Over-sampling Technique) strictly within the training folds to handle the 8% class imbalance.
* **CDSS App:** Built using Streamlit. The alert is precisely aligned with the prediction timing (post-collection, pre-analysis) and provides actionable preventive guidance.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the Jupyter Notebook (`hemolysis_prediction.ipynb`) to train the model and generate the `.pkl` file.
3. Launch the CDSS app: `streamlit run app.py`

## Results
The Random Forest model achieved the best performance (ROC-AUC: 0.79), balancing interpretability with high sensitivity (Recall: 71%), which is critical for clinical decision support where missing a hemolyzed sample is worse than a false alarm.
