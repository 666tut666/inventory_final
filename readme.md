first go to backend
  in terminal
      cd backend
    next install requirements
      pip install -r requirements.txt
    now run backend
      uvicorn main:app --reload

for react app on frontend
(make sure you have latest node.js)
        (src: "https://nodejs.org/en/download/" )
  
  in terminal
    cd frontend
  
  install npm
    npm install
  
  run react
    npm start
  
  
  if you recieve error on frontend
      delete
          /frontend/node_modules
        and
          /frontend/package-lock.json
      now 
      re-install npm and run react
      