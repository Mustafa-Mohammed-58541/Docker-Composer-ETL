# Run The container
docker-compose up -d --build
# Access the PostgreSQL container 
'''bash
docker exec -it postgres-container psql -U postgres -d employee_db  '''
'''sql
select * from employees;'''


/Docker-Composer-ETL
├── docker-compose.yml      # Docker Compose configuration for PostgreSQL and Python containers
├── etl.py                  # Python script that performs ETL operations (extract, transform, load)
├── requirements.txt        # List of required Python dependencies
└── README.md               # This README file
