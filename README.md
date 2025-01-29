# Run The container
docker-compose up -d --build
# Run postgres container 
docker exec -it postgres-container psql -U postgres -d employee_db
select * from employees;
