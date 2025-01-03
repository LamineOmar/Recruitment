from src.helpers.config import get_settings, Settings
import os
import random
import string
import shutil

class BaseController:
    
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.files_dir = os.path.join(
            self.base_dir,
            "assets/files"
         )
        if not os.path.exists(self.files_dir):
            # Create a new directory
            os.makedirs(self.files_dir)

    def generate_random_string(self, length: int=12):
        return  ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))