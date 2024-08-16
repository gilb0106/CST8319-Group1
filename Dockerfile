FROM python:3.12.2-slim

WORKDIR /app

COPY . /app

# Install Cython if it's needed
RUN pip install Cython

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
