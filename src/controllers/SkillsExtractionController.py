from fastapi import UploadFile
from .BaseController import BaseController
import os
import re
import csv
import pdfplumber
import spacy
import logging
import logging

class SkillsExtractionController(BaseController):

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm")
        self.data_list = []
        logging.basicConfig(level=logging.INFO) 
    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    def extract_contact_number_from_resume(self, text):
        pattern = r"\+?\d[\d -]{8,15}\d"
        match = re.search(pattern, text)
        return match.group() if match else None

    def extract_email_from_resume(self, text):
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, text)
        return match.group() if match else None

    def extract_skills_from_resume(self, text, skills_list):
        doc = self.nlp(text)
        skills = [token.text for token in doc if token.text in skills_list]
        return list(set(skills))  # Remove duplicates

    def extract_name_from_resume(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def process_resume(self, pdf_path, skills_list, id_counter):
        text = self.extract_text_from_pdf(pdf_path)
        name = self.extract_name_from_resume(text)
        phone = self.extract_contact_number_from_resume(text)
        email = self.extract_email_from_resume(text)
        extracted_skills = self.extract_skills_from_resume(text, skills_list)

        logging.info(f"Processed resume: {name}, Phone: {phone}, Email: {email}, Skills: {extracted_skills}")

        filename = os.path.basename(pdf_path)
        return [id_counter, filename, name, phone, email, ', '.join(extracted_skills) if extracted_skills else "Aucune compétence trouvée"]



    def process_all_resumes_in_folder(self, folder_path, skills_list, output_csv):
        id_counter = 1
        data_list = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
                data = self.process_resume(pdf_path, skills_list, id_counter)
                data_list.append(data)
                id_counter += 1
        self.save_to_single_csv(data_list, output_csv)

    def save_to_single_csv(self, data_list, output_csv):
        header = ['id', 'nom_fichier', 'nom', 'téléphone', 'email', 'compétences']
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for data in data_list:
                writer.writerow(data)