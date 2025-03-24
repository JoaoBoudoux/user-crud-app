Hi, this is my project to Deeper Systems.
I loved this challenge, I would like to thank Deeper Systems for the opportunity to showcase my knowledge.

# User CRUD App

This is a full-stack application for managing users, built with a Vue.js frontend (using Vite) and a Flask backend. The app allows you to create, read, update, and delete (CRUD) users, with data stored in a MongoDB database.

## Prerequisites

Before running the application, ensure you have the following installed:
- **Node.js** (v16 or higher) - For the frontend (client)
- **Python** (v3.8 or higher) - For the backend (server)
- **MongoDB** - For the database
- **Git** - To clone the repository

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:

(PT-BR)
git clone https://github.com/SEU_USUARIO/user-crud-app.git 

(EN-US)
git clone https://github.com/YOU_USER/user-crud-app.git

cd user-crud-app

### 2. Set Up the MongoDB Database

Start the MongoDB server:

bash: mongod --dbpath /path/to/your/data/db

### 3. Populate the Database with Sample Data

The users.json file contains sample user data.

Run the parser.py script to parse the JSON and insert the data into the MongoDB users collection:

bash: python parser.py

### 4. Set Up the Backend (Server)

Navigate to the project root directory (where server.py is located).
Create a virtual environment and activate it:

bash: python -m venv venv
bash: .\venv\Scripts\activate  # On Windows
bash: source venv/bin/activate  # On macOS/Linux


# Install the required Python dependencies:

bash: pip install flask pymongo flask-cors

# Start the Flask server:

bash: python server.py

The server will run on http://localhost:5000.



### 5. Set Up the Frontend (Client)

Navigate to the client directory:

bash: cd client

# Install the required Node.js dependencies:

bash: npm install

# Start the Vite development server:

bash: npm run dev

The frontend will run on http://localhost:5173.


### 6. Access the Application

Open your browser and navigate to http://localhost:5173.

You should see the "Users Management" page with a table of users.

You can create, edit, delete, and view user details.


# Project Structure

client/: Contains the Vue.js frontend (built with Vite).

server.py: The Flask backend server.

parser.py: A script to parse users.json and insert data into MongoDB.

users.json: Sample user data in JSON format.

README.md: This file with setup instructions.

