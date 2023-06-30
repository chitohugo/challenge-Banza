## Challenge for Banza

### Running with docker

#### Pre-requisites:
- docker
- docker compose (New)

#### Steps:
1. Create a file called `.env` with environment variables in the root of the project
2. Build with `docker compose build`
3. Run with `docker compose up`
4. Run Tests `docker compose exec app pytest`
5. Restore dump.sql in docker (postgres) 

#### How to use: 
- Test credentials: `email:test@gmail.com`, `password: testing123`
- You can test the endpoints with your preferred rest client. (Postman/Insomnia)

#### Environment Variables (.env)
```
SECRET_KEY = 'Generate secret key'
DATABASE_PORT=5432
POSTGRES_PASSWORD='postgres''
POSTGRES_USER=postgres
POSTGRES_DB=challenge
POSTGRES_HOST=postgres
POSTGRES_HOSTNAME=db

ACCESS_TOKEN_EXPIRES_IN=1440
JWT_ALGORITHM=RS256

CLIENT_ORIGIN=http://localhost:3000
```