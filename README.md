# Title: ArtInfoDump
> __Description__: An automated pipeline that extracts data about artworks, including their urls from the _API_ of __Art Institure Chicago__, performs a simple manipulation on the extracted data, then loads it to Postgres.  
The entire process is orchestrated and run in *Docker*

> _I want the maximum number of entries to be 10000_

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
    - Docker-compose.  
        &nbsp; _Services_  
            &nbsp;&nbsp;&nbsp;&nbsp;- postgres.  
            &nbsp;&nbsp;&nbsp;&nbsp;- pgadmin coonnection   
            &nbsp;&nbsp;&nbsp;&nbsp;- python script.  

> __Todo__ : Build a simple GUI to display random images and their properties  
__Current state of the project__: _Incomplete_