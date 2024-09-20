import os
from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
from helpers.config import get_settings, Settings
from controllers import DataController, SkillsExtractionController, JobMatchingSystem
from models import ResponseSignal
import logging

# Create a new APIRouter instance
post_router = APIRouter()

# Set up the static files directory
templates_dir = os.path.abspath("templates")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory=templates_dir)

# Define a GET route to serve the form
@post_router.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@post_router.post("/submit", response_class=JSONResponse)
async def submit_form(
    request: Request,
    user_input: str = Form(...),
    files: List[UploadFile] = File(...),
    app_settings: Settings = Depends(get_settings)
):
    data_controller = DataController()
    skills_extractor = SkillsExtractionController()  # Instancier le contrôleur d'extraction
    matching_system = JobMatchingSystem()  # Instancier le système de matching
    
    # Assurez-vous que le répertoire existe
    upload_directory = "assets/files"
    os.makedirs(upload_directory, exist_ok=True)
    
    file_ids = []  # Liste pour stocker les IDs des fichiers traités
    extracted_data = []  # Liste pour stocker les informations extraites
    extracted_skills_csv = os.path.join(upload_directory, "extracted_skills.csv")

    # Enregistrer la description du poste
    job_description_path = os.path.join(upload_directory, "job_description.txt")
    with open(job_description_path, 'w', encoding='utf-8') as fichier:
        fichier.write(user_input)

    # Process each uploaded file (PDF)
    for file in files:
        # Validation du fichier et de la description du poste
        is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
        is_valid_post, result_signal_post = data_controller.validate_uploaded_post(post=user_input)

        if not is_valid or not is_valid_post:
            return templates.TemplateResponse(
                "index.html",
                status_code=status.HTTP_400_BAD_REQUEST,
                context={
                    "request": request,  # Passez l'objet request au contexte
                    "signal": result_signal,
                    "signal_post": result_signal_post,
                    "file_ids": file_ids
                }
            )
        
        # Générer le chemin du fichier et l'ID unique
        file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename)

        # Enregistrer le fichier PDF
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Appel à SkillsExtractionController pour extraire les informations
        text = skills_extractor.extract_text_from_pdf(pdf_path=file_path)
        contact_number = skills_extractor.extract_contact_number_from_resume(text=text)

        # Extraire les compétences du CV
        extracted_info = skills_extractor.process_resume(
            pdf_path=file_path,
            skills_list=[ # Langages de programmation
                'Python', 'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'TypeScript', 'C', 'C#', 'Go', 'Swift', 'Kotlin', 'Ruby',
                'PHP', 'R', 'MATLAB', 'Scala', 'Perl', 'Rust', 'SQL', 'NoSQL', 'Bash', 'Shell Scripting', 'PowerShell',

                # Développement Web
                'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js', 'Django', 'Flask', 'Spring Boot', 'ASP.NET',
                'Ruby on Rails', 'GraphQL', 'RESTful APIs', 'SOAP', 'WebSockets', 'Next.js', 'Nuxt.js', 'Tailwind CSS', 'Bootstrap',

                # Développement Mobile
                'iOS Development', 'Android Development', 'React Native', 'Flutter', 'SwiftUI', 'Objective-C', 'Xamarin', 'Kotlin', 'Ionic',

                # Frameworks et Librairies de Machine Learning
                'TensorFlow', 'Keras', 'PyTorch', 'Scikit-learn', 'OpenCV', 'XGBoost', 'LightGBM', 'CatBoost', 'NLTK', 'SpaCy',
                'Hugging Face', 'FastAI', 'Theano',

                # Data Science et Analyse de Données
                'Data Analysis', 'Machine Learning', 'Deep Learning', 'Data Visualization', 'Statistics', 'Quantitative Analysis',
                'Qualitative Analysis', 'Pandas', 'Numpy', 'Matplotlib', 'Seaborn', 'Plotly', 'Jupyter Notebook', 'Excel', 'Tableau', 'Power BI',

                # Big Data et Traitement de Données
                'Hadoop', 'Spark', 'MapReduce', 'Hive', 'Pig', 'Kafka', 'Flink', 'Storm', 'HBase', 'Cassandra', 'Redis',
                'Elasticsearch', 'MongoDB', 'Dask',

                # Cloud Computing
                'AWS', 'Azure', 'Google Cloud Platform (GCP)', 'IBM Cloud', 'Oracle Cloud', 'Docker', 'Kubernetes', 'OpenShift',
                'Terraform', 'Ansible', 'Puppet', 'Chef', 'Jenkins', 'CI/CD', 'Serverless', 'Lambda', 'CloudFormation',

                # Gestion de Bases de Données
                'MySQL', 'PostgreSQL', 'SQLite', 'Oracle Database', 'SQL Server', 'MariaDB', 'MongoDB', 'CouchDB', 'Firebase',
                'DynamoDB', 'Neo4j', 'GraphQL',

                # Cybersécurité
                'Network Security', 'Penetration Testing', 'Malware Analysis', 'Encryption', 'Firewalls', 'IDS/IPS', 'VPN',
                'SIEM', 'SOC', 'Incident Response', 'Forensics', 'Vulnerability Assessment', 'OWASP', 'Kali Linux', 'Metasploit',
                # Outils de Gestion de Projets et Méthodologies
                'Project Management', 'Agile', 'Scrum', 'Kanban', 'JIRA', 'Confluence', 'Trello', 'Slack', 'Asana',
                'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Version Control',

                # Design et Développement UI/UX
                'UI/UX Design', 'Adobe XD', 'Figma', 'Sketch', 'InVision', 'Wireframing', 'Prototyping', 'User Testing',
                'Responsive Design', 'Material Design', 'Human-Computer Interaction',

                # DevOps et Automation
                'DevOps', 'CI/CD', 'Jenkins', 'Travis CI', 'GitLab CI', 'Ansible', 'Puppet', 'Chef', 'Docker', 'Kubernetes',
                'Nagios', 'Prometheus', 'Grafana', 'Elastic Stack',

                # Outils de Collaboration et Communication
                'Microsoft Teams', 'Zoom', 'Slack', 'Google Meet', 'Skype', 'Jitsi', 'WebEx',

                # Autres
                'Blockchain', 'Smart Contracts', 'Ethereum', 'Solidity', 'Hyperledger', 'Cryptocurrency', 'Bitcoin',
                'Augmented Reality (AR)', 'Virtual Reality (VR)', 'Unity', 'Unreal Engine', 'Game Development',
                'Natural Language Processing', 'Computer Vision', 'Speech Recognition', 'Reinforcement Learning',
                'Robotic Process Automation (RPA)', 'ETL', 'Data Warehousing', 'Business Intelligence', 'CRM Systems',
                'SAP', 'Salesforce', 'Oracle ERP'
                ],
            id_counter=len(file_ids)
        )

        print(f"Informations extraites pour {file.filename} : {extracted_info}")
        extracted_data.append(extracted_info)

        # Ajouter l'ID du fichier à la liste
        file_ids.append(file_id)

    # Enregistrement des données extraites dans un CSV
    skills_extractor.save_to_single_csv(extracted_data, extracted_skills_csv)

    # Comparer la description du poste avec les compétences extraites
    top_matches = matching_system.match_job_description_to_skills(job_description_path, extracted_skills_csv)

    # Afficher les résultats après la soumission
    return templates.TemplateResponse(
        "results.html",
        context={
            "request": request,
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "signal_post": ResponseSignal.POST_UPLOAD_SUCCESS.value,
            "file_ids": file_ids,
            "top_matches": top_matches  # Résultats du matching
        }
    )
