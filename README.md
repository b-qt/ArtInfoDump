# Title: ArtInfoDump
> __Description__: An automated pipeline that extracts data about artworks from the _API_ of __Art Institure Chicago__, performs a simple transformation, loads it to Postgres.
The entire process is orchestrated and run in *Docker*

### Technologies used
> Docker, Docker-compose, python, pandas, posgresql
1. PostgreSQL database  
    - Via the _official Postgres Docker image_
2. Python
    - Libraries ... _requirements.txt_
        - requests | wget
        - pandas
        - sqlalchemy
        -psycopg2-binary
    - Script logic ... _Ingestion_
        - ETL
3. Docker
    - Dockerfile
    - Docker-compose