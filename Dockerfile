# ===================================================================
# --- Stage 1: The Foundation ("Set up the Operating Room") ---
# ===================================================================
# Start from an official, lightweight Python 3.10 image. 
# The "-slim" version is smaller and good for production.
FROM python:3.10-slim

# ===================================================================
# --- Stage 2: The Dependencies ("Stock the Instrument Tray") ---
# ===================================================================
# 1. Set the working directory inside the container.
#    This is where all our subsequent commands will run from.
WORKDIR /app

# 2. Copy the "prescription list" (requirements.txt) into the container.
COPY requirements.txt .

# 3. Install all the required Python libraries.
#    --no-cache-dir makes the final image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# ===================================================================
# --- Stage 3: The Application ("Place the Patient Chart") ---
# ===================================================================
# 1. Copy all of our project files (app.py, .pkl, .csv, etc.) into the container.
COPY . .

# ===================================================================
# --- Stage 4: The Final Protocol ---
# ===================================================================
# 1. Expose the port that Streamlit runs on (8501) to the outside world.
EXPOSE 8501

# 2. Define the command that will be executed when the container starts.
#    This runs our Streamlit application.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]