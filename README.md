# Take Home Assessment - Software Engineering Position

## Run the Backend

1. Run Postgres with docker `docker run --name ecovision-db -p 5432:5432 -d postgres`
2. Navigate to backend `cd backend`
3. Create python virtual env `python -m venv venv && source venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. To run the application: `flask run`

These instructions assume you are using a Unix-based machine. If you're using Windows, the syntax may differ slightly but the steps should be the same.

## Run the Frontend
1. Update `API_BASE_URL` in `api.js` to point to the correct URL for backend, if you didn't use the default port for Flask. Otherwise, the URL should work as is.
2. Run `npm run dev`