# Recruitement using NLP

This project aims to digitize the recruitment process by matching candidates' CVs with job descriptions and generating questions for these candidates, among other tasks.

## Requirements
- Python 3.10.14 

#### install Python using Miniconda

1) Downloadand install Miniconda from [here](https://docs.anaconda.com/miniconda/#quick-command-line-install)

or on WSL:

```bash 
wget [link]
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
 5) Navigate to http://localhost:8080/