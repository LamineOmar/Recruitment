from .BaseController import BaseController
from fastapi import UploadFile
from src.models import ResponseSignal
import re
import os

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576 # convert MB to bytes
    
    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.CV_FILE_MAX_SIZE*self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
    
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def validate_uploaded_post(self, post: str):
        if len(post) > self.app_settings.SIZE_OF_POST_DESCRIPTION*self.size_scale:
            return False, ResponseSignal.POST_SIZE_EXCEEDED.value
    
        return True, ResponseSignal.POST_VALIDATED_SUCCESS.value
    
    def generate_unique_filepath(self, orig_file_name: str):

        random_key = self.generate_random_string()
        project_path = BaseController()

        cleaned_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )

        new_file_path = os.path.join(
            self.files_dir,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                self.files_dir,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
    def get_prompt(self):
        return """
        You are an AI front-end developer and an assistant that generates QCM questions strictly to evaluate a candidate's skills and knowledge based on the "Compétences Techniques" and "Responsabilité" sections of the following job description. Please generate 10 advanced 1 answer questions, including the correct answers, formatted as JSON.

        The JSON structure should include:
        - A list of questions.
        - Each question should have:
        - "question": The text of the question.
        - "options": A list of multiple-choice options.
        - "answer": The correct answer is exactly one of the options.

        Strict Guidelines:
        - **Only generate questions that test the candidate's understanding and skills**, based on the technologies and responsibilities mentioned in the "Compétences Techniques" and "Responsabilité" sections.
        - **Do not ask candidates to recall details directly from the job description.** Instead, ask questions that assess their knowledge of how to apply these skills and handle these responsibilities in real-world scenarios.
        - **Questions should be practical and skill-based,** aimed at testing the candidate's competency in the relevant technical areas and responsibilities.
        - Avoid speculative or hypothetical questions.

        Job Description:
        {job_description}

        Generate the JSON:
        """