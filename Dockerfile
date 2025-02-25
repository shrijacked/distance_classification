FROM python:3.11.4

WORKDIR /app

# Copy all files to the container
COPY . .

# Install dependencies
# Update this line to include all packages your project needs
RUN pip install numpy pandas scikit-learn wandb matplotlib jupyter nbformat

# Command to run when container starts
CMD ["python", "distance_classification.py"]