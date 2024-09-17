import os
from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
from helpers.config import get_settings, Settings
from controllers import SkillsExtractionController, DataController
from models import ResponseSignal
from fastapi import HTTPException
from controllers.SkillsExtractionController import SkillsExtractionController

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
    print("Début de la fonction submit_form")  # Log de début de fonction
    
    data_controller = DataController()  # Instance de DataController
    print("Instance de DataController créée")
    
    skills_extraction_controller = SkillsExtractionController()  # Instance de SkillsExtractionController
    print("Instance de SkillsExtractionController créée")
    
    # Assurez-vous que le répertoire existe
    upload_directory = "assets/files"
    os.makedirs(upload_directory, exist_ok=True)
    print(f"Répertoire d'upload vérifié/créé : {upload_directory}")
    
    file_ids = []  # Liste pour stocker les IDs des fichiers traités
    extracted_data = []  # Liste pour stocker les données extraites

    try:
        for file in files:
            print(f"Traitement du fichier : {file.filename}")
            is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
            print(f"Validation du fichier : {is_valid}")
            is_valid_post, result_signal_post = data_controller.validate_uploaded_post(post=user_input)
            print(f"Validation du post : {is_valid_post}")

            if not (is_valid and is_valid_post):
                print("Validation échouée")
                return templates.TemplateResponse(
                    "index.html",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    context={
                        "request": request,
                        "signal": result_signal,
                        "signal_post": result_signal_post,
                        "file_ids": file_ids
                    }
                )
            
            # Générer le chemin du fichier et l'ID unique
            file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename)
            print(f"Chemin généré : {file_path}, ID : {file_id}")

            # Enregistrer le fichier
            try:
                with open(file_path, "wb") as f:
                    print(f"Enregistrement du fichier {file.filename} au chemin {file_path}")
                    content = await file.read()
                    f.write(content)
            except Exception as e:
                print(f"Erreur lors de l'enregistrement du fichier : {str(e)}")
                raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement du fichier : {str(e)}")
            
            # Enregistrer la description post
            file_post = os.path.join(data_controller.files_dir, "post_description.txt")
            try:
                with open(file_post, 'w', encoding='utf-8') as fichier:
                    print(f"Enregistrement de la description post dans {file_post}")
                    fichier.write(user_input)
            except Exception as e:
                print(f"Erreur lors de l'écriture du texte : {str(e)}")
                raise HTTPException(status_code=500, detail=f"Erreur lors de l'écriture du texte : {str(e)}")
                
            # Ajouter l'ID du fichier à la liste
            file_ids.append(file_id)
            print(f"ID de fichier ajouté : {file_id}")
            
            # Appel à SkillsExtractionController pour extraire les informations
            extracted_info = skills_extraction_controller.process_resume(
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

        # Enregistrement des données extraites dans un CSV
        output_csv = os.path.join(upload_directory, "extracted_skills.csv")
        print(f"Enregistrement des données extraites dans {output_csv}")
        skills_extraction_controller.save_to_single_csv(extracted_data, output_csv)
    except Exception as e:
        print(f"Erreur générale : {str(e)}")
        return JSONResponse(
            content={"message": f"Une erreur est survenue : {str(e)}"},
            status_code=500
        )

    print("Fin de la fonction submit_form, retour du TemplateResponse")
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "signal_post": ResponseSignal.POST_UPLOAD_SUCCESS.value,
            "file_ids": file_ids
        }
    )
