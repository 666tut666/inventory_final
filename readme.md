First, go to the backend directory:

cd backend 

Next, install the required packages:

pip install -r requirements.txt 

Now, run the backend:

uvicorn main:app --reload 

For the React app on the frontend (make sure you have the latest version of Node.js):

(src: "https://nodejs.org/en/download/" )

In the terminal, navigate to the frontend directory:

cd frontend 

Install the required packages:

npm install 

Run React:

npm start 

If you receive an error on the frontend:

Delete the following directories: 

/frontend/node_modules 
/frontend/package-lock.json 

Reinstall npm and run React.
