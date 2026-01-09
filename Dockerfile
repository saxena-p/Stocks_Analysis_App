# 1️⃣ Start from a small Linux image with Python installed
FROM python:3.13-slim

# 2️⃣ Set a working directory inside the container
WORKDIR /app

# 3️⃣ Copy dependency list first (important for caching)
COPY requirements.txt .

# 4️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy the rest of the application code
COPY . .

# 6️⃣ Expose the port FastAPI will run on
EXPOSE 8000

# 7️⃣ Command to start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]