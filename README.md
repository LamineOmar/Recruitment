# Recruitement using NLP

This project aims to digitize the recruitment process by matching candidates' CVs with job descriptions and generating questions for these candidates, among other tasks.

## Requirements
- Python 3.8 or later

#### install Python using Miniconda

1) Downloadand install Miniconda from [here](https://docs.anaconda.com/miniconda/#quick-command-line-install)

or on WSL:

```bash 
$ wget [link]
```
2) Create a new environment using the following command:
```bash
$ conda create -n recruitement python=3.8
```
3) Activate the environment:
```bash
$ conda activate recruitement
```

## Installation
### Install the required packages
```bash
$ pip install -r requirements.txt
```


### Run the FastAPI server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
