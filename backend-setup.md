```markdown
# Flask Project Setup Guide

This guide will walk you through the process of setting up your Flask project environment, configuring your database, and installing dependencies to get your backend up and running.

---

## 🌱 Step 1: Create and Configure the `.env` File

Your Flask application uses environment variables to manage configuration settings securely and flexibly. Here's how to create your `.env` file:

1. Open your project directory in your code editor.
2. Create a new file named `.env`.
3. Copy and paste the following content into it:

   ```env
   FLASK_DEBUG=True
   FLASK_RUN_HOST=0.0.0.0
   FLASK_RUN_PORT=8080
   SECRET_KEY="dsfsdffdsfsdfsdfdsfsdfsdf"
   DATABASE_URL=postgresql://project_user:password@localhost/project_db
   UPLOAD_FOLDER="./uploads"
   ```


## 🐍 Step 2: Set Up a Python Virtual Environment

To keep dependencies isolated and manageable, you should use a virtual environment:

1. Open your terminal in the project directory.
2. Run the following command to create a virtual environment named `venv`:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

---

## 📦 Step 3: Install Flask and Other Dependencies

With your virtual environment activated, install the project dependencies using:

```bash
pip install -r requirements.txt
```

This will install Flask and any other required libraries listed in your `requirements.txt` file.

---

## 🛢️ Step 4: Set Up PostgreSQL with pgAdmin

1. Open **pgAdmin** (or any PostgreSQL GUI).
2. Create a **new user**:
   - Username: `project_user`
   - Password: `password`

3. Create a **new database**:
   - Database name: `project_db`
   - Owner: `project_user`

This matches the settings you defined in your `.env` file.

---

## 🛠️ Step 5: Apply Database Migrations

If your project uses Flask-Migrate (commonly used with SQLAlchemy), you can apply all existing migrations to the new database:

```bash
flask db upgrade
```

This will create the necessary tables and schema in `project_db` based on the migration history.

---

## ✅ That's It!

Your Flask backend should now be set up and ready for development. If you're planning to run the app, use:

```bash
flask --app app --debug run
```

This will start the development server using the port and host defined in your `.env`.

---

