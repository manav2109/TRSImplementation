import PyPDF2
import pytesseract
from PIL import Image
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score


# Step 1: Extracting Text
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        #num_pages = pdf_reader.numPages
        for page in pdf_reader.pages:
            #page = pdf_reader.getPage(page_num)
            text += page.extract_text()
    return text


# Step 2: Preprocessing
def preprocess_text(text):
    # Perform text cleaning, normalization, etc.
    # Example: Remove special characters and extra spaces
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.lower()


# Step 3: Feature Engineering
def create_tfidf_features(text_data):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)
    return tfidf_matrix


# Step 4: Model Training
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearSVC()
    model.fit(X_train, y_train)
    return model, X_test, y_test


# Step 5: Evaluation
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# # Example usage
# if __name__ == "__main__":
#     # Example PDF path
#     pdf_path = "C:\\Users\\abhij\\PycharmProjects\\TRSImplementation\\TestData\\SampleTRSSheets\\GEN_Pdf_TRS_L26118_07082018_132507.pdf"
#
#     # Step 1: Extract text from PDF
#     text_data = extract_text_from_pdf(pdf_path)
#
#     # Step 2: Preprocess text data
#     cleaned_text = preprocess_text(text_data)
#
#     # Step 3: Create TF-IDF features
#     tfidf_matrix = create_tfidf_features([cleaned_text])
#
#     # Step 4: Train model (example labels y assumed to be available)
#     labels = [0] * len(tfidf_matrix)  # Example labels, replace with actual labels
#     model, X_test, y_test = train_model(tfidf_matrix, labels)
#
#     # Step 5: Evaluate model
#     accuracy = evaluate_model(model, X_test, y_test)
#     print("Accuracy:", accuracy)
