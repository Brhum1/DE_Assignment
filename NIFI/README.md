# Data Engineering Pipeline (NiFi, PostgreSQL, HDFS)

## Overview
This repository contains my data engineering assignment. The goal was to build an end-to-end data pipeline that ingests messy data from a Python generator and a PostgreSQL database, cleans it using Apache NiFi, and finally stores the processed data into HDFS.

Because I ran NiFi inside a Docker container while Hadoop was installed locally on my Debian machine, I couldn't connect them directly due to Docker's network isolation. To solve this, I wrote a custom Python orchestrator to bridge the gap between the Docker container and the host file system.

## Technologies Used
* **Python:** For data generation (mocking messy CSVs) and orchestrating data movement.
* **PostgreSQL:** To act as a relational data source for incremental loading.
* **Apache NiFi (Docker):** For data routing, transformation, and cleaning.
* **Hadoop (HDFS):** The final distributed storage.

## How the Pipeline Works

### 1. Data Ingestion
* **CSV Files:** My Python script generates CSVs with intentional errors (duplicates, missing IDs, bad formats) and pushes them directly into the NiFi Docker container. NiFi picks them up using `ListFile` and `FetchFile`.
* **Database:** NiFi connects to a local PostgreSQL instance and extracts new records incrementally using `QueryDatabaseTable` (tracking the `id` column), then converts the Avro output to CSV via `ConvertRecord`.

### 2. Transformation (Data Cleaning)
* Both data streams are merged and sent to a `QueryRecord` processor.
* I used a custom SQL query inside NiFi (`SELECT DISTINCT * FROM FLOWFILE WHERE CustomerID IS NOT NULL`) to automatically drop invalid records and remove any duplicates.

### 3. Loading & The Docker Workaround
* Since NiFi is isolated in Docker, I used a `PutFile` processor to write the cleaned data to an internal output folder inside the container.
* My Python script continuously monitors this internal folder, pulls the clean files out to my local machine, and runs `hdfs dfs -put` to load them safely into HDFS.

## Repository Structure
* `data_generator.py`: The main Python script that generates data and handles the Docker <-> Local <-> HDFS transfers.
* `schema.sql`: The SQL queries used to set up the PostgreSQL table and insert dummy data.
* `nifi_assignment_flow.json`: The exported NiFi template containing my complete pipeline design.
* `screenshots/`: Proof of execution, including the NiFi canvas, Python terminal output, and the final HDFS directory listing.

## How to Run This Project
1. Start the Hadoop daemons on the host machine (`start-dfs.sh`).
2. Set up the PostgreSQL table using `schema.sql`.
3. Import `nifi_assignment_flow.json` into NiFi and enable the Controller Services (CSVReader, CSVWriter, DBCPConnectionPool).
4. Start all NiFi processors.
5. Run the orchestrator script: `python3 data_generator.py`.
