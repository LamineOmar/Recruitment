import re
import string
from nltk.corpus import stopwords
import nltk

# Télécharger les stopwords si ce n'est pas déjà fait
nltk.download('stopwords')

class Clean:
    def __init__(self):
        print("Clean instance created")
        
    def clean_text(self, text):
        stop_words = stopwords.words('english')

        text = str(text)
        #text = text.lower()
        #text = re.sub(r'[^\x00-\x7f]', r' ', text)  # Remplace les caractères non-ASCII par un espace
        text = re.sub('\s+', ' ', text)  # Remplace les espaces multiples par un seul espace
        #text = "".join([char for char in text if char not in string.punctuation])  # Retire la ponctuation
        #text = re.sub("\d+", " ", text)  # Retire les chiffres
        #text = ' '.join([word for word in text.split() if word not in stop_words])  # Retire les stopwords
        return text.strip()
