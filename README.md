  # BREAD Calculator, JWT Auth, and CI/CD

  This repository contains a FastAPI application that implements a simple calculator with user management (registration, login, and JWT-based authentication). It provides full BREAD functionality for calculations (Browse, Read, Edit, Add, Delete), a front-end UI demonstrating the flows, unit/integration/Playwright E2E tests, and a GitHub Actions CI workflow.

  ---

  ## What this project includes

  - FastAPI application (`main.py` & `app/`)
    - `app/routers/users.py` — register, login and `GET /users/me`
    - `app/routers/calculations.py` — calculator BREAD endpoints (user-scoped)
    - `app/security.py` — password hashing and JWT helpers
    - `app/crud.py`, `app/models.py`, `app/db.py` — DB access and models
  - Front-end templates in `templates/`:
    - `index.html` — calculator UI and CRUD pages (create/list/edit/delete)
    - `register.html` and `login.html` with client-side validation and token storage in `localStorage`
  - Tests in `tests/`:
    - Unit tests, integration tests, and Playwright E2E tests (`tests/e2e/`)
  - CI workflow at `.github/workflows/ci.yml` that runs tests and can build/push a Docker image
  - `generate_secret.py` — helper to generate a secure `SECRET_KEY`

  ---

  ## Quick local setup

  1. Create and activate a virtual environment (recommended):

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  ```

  2. Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

  3. (Optional) Install Playwright browsers for E2E tests:

  ```bash
  python -m playwright install --with-deps
  ```

  4. (Recommended) Generate and set a strong SECRET_KEY for JWT signing:

  ```bash
  # generate a URL-safe secret and copy it
  python3 generate_secret.py --bytes 32 --format urlsafe

  # export into your shell session (replace with the generated value)
  export SECRET_KEY='paste-generated-value-here'
  ```

  Note: If `SECRET_KEY` is not set the app falls back to an insecure default—do not use that in production.

  ---

  ## Run the application (development)

  Start the app with Uvicorn from the project root:

  ```bash
  uvicorn main:app --reload
  ```

  Open these pages:

  - `http://127.0.0.1:8000/` — index page (calculator + BREAD UI)
  - `http://127.0.0.1:8000/register` — registration page
  - `http://127.0.0.1:8000/login` — login page
  - `http://127.0.0.1:8000/docs` — OpenAPI (Swagger) UI

  ---

  ## Calculation (BREAD) endpoints (high-level)

  All `/calculations` endpoints require `Authorization: Bearer <token>` and are scoped to the logged-in user.

  - GET `/calculations/` — Browse: list all calculations for the authenticated user.
  - GET `/calculations/{id}` — Read: get a calculation by id (404 if missing or not owned).
  - POST `/calculations/` — Add: create a calculation. Example body: `{ "operation": "add", "a": 1, "b": 2 }`.
  - PUT `/calculations/{id}` — Edit: update an existing calculation.
  - DELETE `/calculations/{id}` — Delete: remove an existing calculation.

  Server-side validation is provided via Pydantic schemas; the front-end also validates numeric inputs and allowed operations before sending requests.

  ---

  ## Testing

  Run the test suite locally from the project root (with your venv active):

  ```bash
  pytest -q
  ```

  - Run only e2e tests:

  ```bash
  pytest -q -m e2e
  ```

  Notes:
  - Playwright E2E tests require browser binaries (`python -m playwright install --with-deps`).
  - `tests/conftest.py` starts the FastAPI server for E2E tests and prepares the DB before tests run.
  - Coverage report: the pytest configuration produces an HTML report in `htmlcov/`.

  ---

  ## CI / GitHub Actions

  The workflow at `.github/workflows/ci.yml` runs the test matrix (unit, integration, e2e). If configured with Docker Hub secrets it can also build and push an image. Add these repository secrets to enable Docker push:

  - `SECRET_KEY` — secure JWT signing key
  - `DOCKERHUB_USERNAME` — Docker Hub username
  - `DOCKERHUB_TOKEN` — Docker Hub token

  Tip: use an explicit `TEST_DATABASE_URL` secret in CI to avoid filesystem permission issues with SQLite.

  ---

  ## Docker

  A `Dockerfile` is included for building the application image. To build and run locally:

  ```bash
  # build
  docker build -t yourusername/is601_app:local .

  # run
  docker run -e SECRET_KEY="$SECRET_KEY" -p 8000:8000 yourusername/is601_app:local
  ```

  DockerHub link: https://hub.docker.com/r/libertyquinzel/is601_app

  ---

