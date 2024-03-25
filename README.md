# 🦕 LMNH-Pipeline 
An automated pipeline for a fictional Natural History Museum (LMNH), aiming to  combine, store, and analyse all visitor kiosk data automatically in realtime.

## 📝 About 
LMNH is a fictionl natural history museum, who have recently added "Smiley Face Survey Kiosks" at the exits of the exhibitions, where visitors are asked to rate their experience of the exhibition on a five-point scale (from 😡 to 😀). Each kiosk features two other buttons: an "assistance" button, for general enquiries, and an "emergency" button for immediate support.

While the kiosks are currently operational, nothing is actually being done with the visitor data yet. LMNH wants to develop an automated pipeline that would combine, store, and analyse all the kiosk data automatically, allowing museum staff to access continually-updating information on the museum's operation.

This project aims to achieve the above, and serves as a chance for me to design and implement my own data models, create analytics dashboards, and work with industry-standard tools such as Kafka, Docker, and Tableau.

## 🛠️ Setup
### Installation
- `pip3 install -r requirements.txt`
- create a `.env` file with the required details (see `.env.example`)

### RDS Setup
To setup an RDS and the necessary security groups for your VPC, work through the following:
- Navigate to the `terraform` folder
- Create a `terraform.tfvars` file with the following keys filled in:
  - `DB_USERNAME = XXXXX`
  - `DB_PASSWORD = XXXXX`
  - `VPC_ID = XXXXX`
- Run the command `terraform init` followed by `terraform apply`

### Schema Setup
To setup your schema for the project, run the command `bash scripts/db_setup.sh`
- To reset the database, simply run `python3 reset_database.py`

## 🏃 Running the Pipeline
- To start the pipeline, simply enter `python3 pipeline.py`
- Optional argument `--log [-l]`
  - if used, errors will be logged to the file `data_errors.log`
- To run in the background, run the command `nohup python3 pipeline.py &`
