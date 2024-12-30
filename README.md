# Recruitement using NLP

This project aims to digitize the recruitment process by matching candidates' CVs with job descriptions and generating questions for these candidates, among other tasks.

### Prerequisites

Before you begin, ensure you have the following:

- `Docker` & `Python` installed on your system
- `API Keys` for Gemini LLM  

#### install Python using Miniconda

We recommend that developers create a new Conda virtual environment to isolate dependencies (for WSL):
1) Install Miniconda in WSL:
```bash 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
2) Create a new environment using the following command:
```bash
conda create -n recruitement python=3.10.14
```
3) Activate the environment:
```bash
conda activate recruitement
```
4) Create a .env file in the src directory, copy the contents of .env.example into .env, and then add the necessary values.
```bash
cp src/.env.example src/.env

```

### Run docker-compose after starting Docker Desktop
```bash
docker-compose up --build
```
Navigate to http://localhost:8080/

![image](https://github.com/user-attachments/assets/559726b2-9103-4a4f-8be9-04ec811ad0ee)

