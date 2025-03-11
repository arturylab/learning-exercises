# 📊 Sentiment Analysis in Mental Health with Scikit-Learn

## 📝 Project Description  
This project performs sentiment analysis on texts related to mental health, classifying them into seven categories:  

- **Normal**  
- **Depression**  
- **Suicidal**  
- **Anxiety**  
- **Stress**  
- **Bipolar**  
- **Personality Disorder**  

The goal is to train a Machine Learning model to predict the mental health status of a given text using `Scikit-Learn`, `TfidfVectorizer` for text vectorization, and a classifier like `LogisticRegression` or `RandomForestClassifier`.

---

## 📂 Program Workflow  

### 📥 Data Loading  
- `kagglehub` is used to download the dataset from Kaggle.  
- The file is loaded into a `pandas` DataFrame.  

### 🔄 Text Preprocessing  
- Special characters are removed, text is converted to lowercase, and irrelevant words (*stop words*) are filtered.  
- **TF-IDF (Term Frequency - Inverse Document Frequency)** is applied to transform text into numerical vectors.  

### 🎯 Model Training  
- The dataset is split into **training** and **test** data.  
- A classification model (e.g., `RandomForestClassifier`) is trained.  

### 📊 Model Evaluation  
- A **Classification Report** is generated with metrics such as **precision, recall, and F1-score**.  
- A **confusion matrix** is built to analyze model errors.  

### 🔍 New Text Prediction  
- The user can input a text, and the model will attempt to predict its mental health category.  

---

## 🚀 Technologies Used  
- Python 🐍  
- Scikit-Learn  
- Pandas  
- TfidfVectorizer  
- RandomForestClassifier  

---

## 📎 Related Links  
🔗 [Kaggle Notebook & Dataset](https://www.kaggle.com/code/arturylab/sentiment-analysis-for-mh-scikit-learn)

---

### 🎯 Future Improvements  
- Incorporate **Deep Learning models** (e.g., LSTMs, Transformers).  
- Expand dataset diversity.  
- Develop a **web app** for interactive predictions.  

---

## 🛠 Installation & Usage  

1️⃣ Clone the repository:  
```bash
git clone https://github.com/arturylab/learning-exercises/tree/4de5657e98b16c525a1a4797cd3083399b958267/data-analysis-ml/sentiment-analysis-for-mental-health
cd sentiment-analysis-for-mental-health
