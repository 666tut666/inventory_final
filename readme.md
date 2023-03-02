## Project Setup

### Backend

1. Navigate to the backend directory:

    ```
    cd backend
    ```

2. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

3. Run the backend:

    ```
    uvicorn main:app --reload
    ```

### Frontend

1. Make sure you have the latest version of Node.js installed. You can download it from [https://nodejs.org/en/download/](https://nodejs.org/en/download/).

2. Navigate to the frontend directory:

    ```
    cd frontend
    ```

3. Install the required packages:

    ```
    npm install
    ```

4. Run React:

    ```
    npm start
    ```

If you receive an error on the frontend:

1. Delete the following directories:

    ```
    /frontend/node_modules
    /frontend/package-lock.json
    ```

2. Reinstall npm and run React.

