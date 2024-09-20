from sentence_transformers import SentenceTransformer, util
import pandas as pd

class JobMatchingSystem:

    def __init__(self):
        # Charger le modèle SBERT pour le matching
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    def match_job_description_to_skills(self, job_description_path: str, extracted_skills_csv: str):
        # Lire la description du poste
        with open(job_description_path, 'r', encoding='utf-8') as file:
            job_description = file.read()
        
        # Transformer la description du poste en embedding
        job_description_embedding = self.model.encode(job_description, convert_to_tensor=True)

        # Lire le fichier CSV contenant les compétences extraites
        skills_data = pd.read_csv(extracted_skills_csv)

        # Stocker les similarités entre les descriptions et les compétences extraites
        similarities = []

        for index, row in skills_data.iterrows():
            skills = row['compétences']  # Assurez-vous que la colonne est correcte
            # Transformer les compétences en embedding
            skills_embedding = self.model.encode(skills, convert_to_tensor=True)
            # Calculer la similarité
            similarity_score = util.pytorch_cos_sim(job_description_embedding, skills_embedding)
            similarities.append((row['email'], similarity_score.item()))        
        # Trier les résultats par score de similarité
        top_matches = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Retourner les 10 meilleurs résultats
        return top_matches[:10]
