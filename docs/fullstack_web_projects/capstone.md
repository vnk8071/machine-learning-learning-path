---
sidebar_label: 'Capstone Full Stack'
sidebar_position: 6
---

# Capstone Full Stack

Source code: [vnk8071/capstone_fullstack_web](https://github.com/vnk8071/machine-learning-in-production/tree/main/projects/capstone_fullstack_web)

## Full Stack Capsone Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## Database Setup
### Create Postgres Database
```bash
dropdb drink
createdb drink
```
![database](../../projects/capstone_fullstack_web/images/database.png)

## Auth0 Setup
### Create Auth0 Application
![application](../../projects/capstone_fullstack_web/images/application.png)

### Create Auth0 API and Permissions
![api_permission](../../projects/capstone_fullstack_web/images/api_permissions.png)

### Create Auth0 Roles and Users
![role](../../projects/capstone_fullstack_web/images/role.png)

Barista: `get:drinks-detail`, `get:drinks`, `get:ingredients`
![permission_barista](../../projects/capstone_fullstack_web/images/permission_barista.png)

Manager: Full Access
![permission_manager](../../projects/capstone_fullstack_web/images/permission_manager.png)

## Backend
### Install Dependencies
```
cd backend
pip install -r requirements.txt
```

## Run Backend Server
```
python api.py
```

URL backend: http://localhost:5000/

## Test Backend
```bash
dropdb drink_test
createdb drink_test
python test_api.py
```

Results:
```
.
----------------------------------------------------------------------
Ran 29 tests in 8.607s

```

## Frontend
### Install Dependencies
```
cd frontend
npm install
```

### Run Frontend Server
```
ionic serve
```

URL frontend: http://localhost:8100/

### Sign In Page
![signin_page](../../projects/capstone_fullstack_web/images/signin_page.png)

### Redirect to Auth0
![auth0_page](../../projects/capstone_fullstack_web/images/auth0_page.png)

### Create Drink
![create_drink](../../projects/capstone_fullstack_web/images/create_drink.png)

### Home Page
![homepage](../../projects/capstone_fullstack_web/images/homepage.png)

## Documentation
### API Reference

URL: http://localhost:5000/

`GET /drinks`

- Fetches a list of drinks in the database
- No permission required
- Request Arguments: None
- Returns: An object with a single key, drinks, that contains an array of drinks objects.
```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "Water"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                },
                {
                    "color": "yellow",
                    "parts": 1
                }
            ],
            "title": "Lemonade"
        }
    ],
    "success": true
}
```

`GET /drinks-detail`

- Fetches a list of drinks in the database
- Permission required: `get:drinks-detail`
- Request Arguments: None
- Returns: An object with a single key, drinks, that contains an array of drinks objects.
```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "Water"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                },
                {
                    "color": "yellow",
                    "name": "lemon",
                    "parts": 1
                }
            ],
            "title": "Lemonade"
        }
    ],
    "success": true
}
```

`POST /drinks`

- Creates a new drink in the database
- Permission required: `post:drinks`
- Request Arguments: None
- Returns: An object with a single key, drinks, that contains an array of drinks objects.
```
{
    "drinks": [
        {
            "id": 3,
            "recipe": [
                {
                    "color": "green",
                    "name": "matcha",
                    "parts": 3
                }
            ],
            "title": "Matcha"
        }
    ],
    "success": true
}
```

`PATCH /drinks/<id>`
- Updates a drink in the database
- Permission required: `patch:drinks`
- Request Arguments: None
- Returns: An object with a single key, drinks, that contains an array of drinks objects.
```
{
    "drinks": [
        {
            "id": 3,
            "recipe": [
                {
                    "color": "green",
                    "name": "matcha",
                    "parts": 3
                }
            ],
            "title": "Matcha"
        }
    ],
    "success": true
}
```

`DELETE /drinks/<id>`
- Deletes a drink in the database
- Permission required: `delete:drinks`
- Request Arguments: None
- Returns: An object with a single key, drinks, that contains an array of drinks objects.
```
{
    "delete": 3,
    "success": true
}
```

`GET /ingredients`
- Fetches a list of ingredients in the database
- Permission required: `get:ingredients`
- Request Arguments: None
- Returns: An object with a single key, ingredients, that contains an array of ingredients objects.
```
{
    "ingredients": [
        {
            "density": "100%",
            "id": 1,
            "name": "water"
        },
        {
            "density": "60%",
            "id": 2,
            "name": "lemon"
        }
    ],
    "success": true
}
```

`POST /ingredients`
- Creates a new ingredient in the database
- Permission required: `post:ingredients`
- Request Arguments: None
- Returns: An object with a single key, ingredients, that contains an array of ingredients objects.
```
{
    "ingredients": [
        {
            "density": "80%",
            "id": 3,
            "name": "coffee"
        }
    ],
    "success": true
}
```

`PATCH /ingredients/<id>`
- Updates an ingredient in the database
- Permission required: `patch:ingredients`
- Request Arguments: None
- Returns: An object with a single key, ingredients, that contains an array of ingredients objects.
```
{
    "ingredients": [
        {
            "density": "90%",
            "id": 3,
            "name": "coffee"
        }
    ],
    "success": true
}
```

`DELETE /ingredients/<id>`
- Deletes an ingredient in the database
- Permission required: `delete:ingredients`
- Request Arguments: None
- Returns: An object with a single key, ingredients, that contains an array of ingredients objects.
```
{
    "delete": 3,
    "success": true
}
```


### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return three error types when requests fail:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Resource Not Found
- `422`: Not Processable

### Users and Roles
`Public`
- Can view drinks and drink details

`Barista`
- All permissions a Public user has and…
- Can view drink details

`Manager`
- All permissions a Barista has and…
- Can create new drinks
- Can delete drinks

### Frontend

URL: http://localhost:8100/

`GET /tabs/drink-menu`
- Home page
- Public
- Shows drinks

`GET /tabs/user-page`
- Login page
- Public
- Redirects to Auth0

Configuration in `./src/environments/environments.ts`:
```javascript
export const environment = {
    production: false,
    apiServerUrl: 'http://127.0.0.1:5000',
    auth0: {
    url: 'dev-t1o1gxv473b4dc8o.us',
    audience: 'http://localhost:5000/login',
    clientId: 'KzQb4fWbJ0bDOwo3MOdG0ucz0Tvtu2SZ',
    callbackURL: 'http://localhost:8100',
    }
};
```

## Test Postman Collection
### Import Postman Collection
1. Open Postman
2. Click on Import
3. Click on Choose Files
4. Select the file `./backend/udacity-fsnd-udaspicelatte.postman_collection.json`

### Get JWT Tokens
Access the following link to get the JWT tokens for the users:
```
https://dev-t1o1gxv473b4dc8o.us.auth0.com/authorize?audience=http://localhost:5000/login&response_type=token&client_id=KzQb4fWbJ0bDOwo3MOdG0ucz0Tvtu2SZ&redirect_uri=http://localhost:8100/tabs/user-page
```

Then, import Bearer Tokens into Postman.

### Test Endpoints
1. Click on the arrow next to the collection name to expand the collection
2. Choose folder `public`, `barista`, or `manager` and run tests on the endpoints

Results:
- All tests should pass for `public` folder
![test_public](../../projects/capstone_fullstack_web/images/test_public.png)
- All tests should pass for `barista` folder
![test_barista](../../projects/capstone_fullstack_web/images/test_barista.png)
- All tests should pass for `manager` folder
![test_manager](../../projects/capstone_fullstack_web/images/test_manager.png)

Export the collection overwriting the `./backend/udacity-fsnd-udaspicelatte.postman_collection.json` file.

## Deployment
![render_services](../../projects/capstone_fullstack_web/images/render_services.png)

### Postgres Database
![render_postgres](../../projects/capstone_fullstack_web/images/render_postgres.png)

Endpoint: `postgres://macos:Lvqb6jAbNSlbpFbsRkYPpcTeS0tHvR2U@dpg-cki2moke1qns73dbmfa0-a/drink_41ri`

### Server
![render_server](../../projects/capstone_fullstack_web/images/render_server.png)

Endpoint Render: https://khoivn-capstone-fullstack.onrender.com/

Token manager: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNPUU5pMmNQbHFkSk1BajFjczhaNCJ9.eyJpc3MiOiJodHRwczovL2Rldi10MW8xZ3h2NDczYjRkYzhvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzMxNDg5MTg4MDQwNjU0ODA3OSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9sb2dpbiIsImlhdCI6MTY5Njg3MjA0MiwiZXhwIjoxNjk3ODc5MjQyLCJhenAiOiJLelFiNGZXYkowYkRPd28zTU9kRzB1Y3owVHZ0dTJTWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImRlbGV0ZTppbmdyZWRpZW50cyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsImdldDppbmdyZWRpZW50cyIsInBhdGNoOmRyaW5rcyIsInBhdGNoOmluZ3JlZGllbnRzIiwicG9zdDpkcmlua3MiLCJwb3N0OmluZ3JlZGllbnRzIl19.ZzBWYYUJ88BX7or6Miu0GuUmNawjxyTBEHhP19N_nnkoOx6lWNmxKYC6HmxZWqrExRPyUHEKzSJtRsGm36V6BJKXK3CiUOzJ-zSTuAN2bn-CwQFqHLLLuF7JDQPkE8Jd3NPD_fkE98bPxFpI7kEif0tOw46TZaCJ4MZqfAiP82Je5C8tnqmwaktqC_34HMrdVgU80gHR5geAeccZdVLGKHTZgaoRp_6G5rhbmseb-UY6rVWXgNmOxarHU7-4IREXRRZ7Is-FJM9f07-031CLYIWX_NEAh7pMkCgZsVXa-9Qcfgf8pN-V212j9e1MLeuHFvQ5y7Ke9OG-kmZfkHJGwQ`

![request_manager](../../projects/capstone_fullstack_web/images/request_manager.png)

TOKEN barista: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNPUU5pMmNQbHFkSk1BajFjczhaNCJ9.eyJpc3MiOiJodHRwczovL2Rldi10MW8xZ3h2NDczYjRkYzhvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTIxMjlkMjQxOTkzYmQ4ODgwMmJkNmQiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAvbG9naW4iLCJpYXQiOjE2OTY4NjAzMTcsImV4cCI6MTg5Njg5NzUxNywiYXpwIjoiS3pRYjRmV2JKMGJET3dvM01PZEcwdWN6MFR2dHUyU1oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsImdldDppbmdyZWRpZW50cyJdfQ.aULs60rKj97d1kzPkx6CFWdAjhhF7kYC-fNCm7zOUECFg_blYQBN89hWvIyyTB8hDVFn_uV0fO4RzHB87TKlEBkdve3otK1CSDOEuRril7vzlyU_sGHBnD-MgQocvttunYOLxSKZhEhOsn0AZ0jlIzoK1azLI3lb5oaRNCl5VCNV10qv1HEOMRQXFJSQKf-alZwlsa1J-Q8QpO06fvWAAfmKIPU4u3zkDj6hzNEiuSXga-0BVfM5MaVKKnwMi4v8mK-Cud4xn0Vn3XUBsqlIRLmAZGts8d9uexWufqzeBHFSWJr6YwIARKMv48pSdOaNBT3v7LxIkg_8cL0VNWbE4g`

![request_barista](../../projects/capstone_fullstack_web/images/request_barista.png)

If the token is expired, please access the following link to get the new token:
```
https://dev-t1o1gxv473b4dc8o.us.auth0.com/authorize?audience=http://localhost:5000/login&response_type=token&client_id=KzQb4fWbJ0bDOwo3MOdG0ucz0Tvtu2SZ&redirect_uri=http://localhost:8100/tabs/user-page
```

Account manager:
```
Email: manager@gmail.com
Password: Manager8071
```

Account barista:
```
Email: barista@gmail.com
Password: Barista8071
```

Return URL with bearer token:
```
http://localhost:8100/tabs/user-page#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNPUU5pMmNQbHFkSk1BajFjczhaNCJ9.eyJpc3MiOiJodHRwczovL2Rldi10MW8xZ3h2NDczYjRkYzhvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzMxNDg5MTg4MDQwNjU0ODA3OSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9sb2dpbiIsImlhdCI6MTY5Njg3NDc2NiwiZXhwIjoxNjk2ODgxOTY2LCJhenAiOiJLelFiNGZXYkowYkRPd28zTU9kRzB1Y3owVHZ0dTJTWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImRlbGV0ZTppbmdyZWRpZW50cyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsImdldDppbmdyZWRpZW50cyIsInBhdGNoOmRyaW5rcyIsInBhdGNoOmluZ3JlZGllbnRzIiwicG9zdDpkcmlua3MiLCJwb3N0OmluZ3JlZGllbnRzIl19.pXe2HFDF4rUdyW564ssLavlG18UNWR70x-yGgHsBqfzzy1MoUWYzo1dQiSKiPumBpG4uv9TCN8rwWJLBofYDkV9UwV6bxM7gzAoWbsbEeqGw43nLMtlBvy5WS0fT1tHHNvaRKO9Swa0ZCHxYflXLOEEyTUx4IAaafT8tgptEnX1a3mUuADN5j6mla6Yk_BrqKPSAJTXVfYR3StgPCp3AucICMAQkTcVOuh-HyD0fYWje7AViRwghRqQAKnjdFcfLGGnY-MjttSbgnDefPoBpJbLfuBRQiFHzvGsHk_NUqEyXny97Kg-Nr-Pqlq9-h2E9Pyvi4qP7cU9J5rogz83IZA&expires_in=7200&token_type=Bearer
```

### Log Server
![log_server](../../projects/capstone_fullstack_web/images/log_server.png)

## Containerization
### Build Docker Image
```
docker build -t capstone-fullstack .
```

### Run Docker Container
```
docker run -p 5000:5000 capstone-fullstack
```

## Kubernetes on AWS
Follow the instructions in the repository [**vnk8071/pipeline-deploy-kubernetes-on-aws**](https://github.com/vnk8071/pipeline-deploy-kubernetes-on-aws) to deploy the application on AWS.
