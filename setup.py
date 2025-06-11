# This is a setup script to demonstrate the commands needed
# In a real environment, you would run these commands in your terminal

import os
import subprocess

# Create virtual environment and install dependencies
print("Setting up virtual environment...")
subprocess.run(["python", "-m", "venv", "venv"])
subprocess.run(["pip", "install", "django", "django-crispy-forms", "crispy-tailwind", "pillow", "django-modeltranslation"])

# Create Django project
print("Creating Django project...")
subprocess.run(["django-admin", "startproject", "wms_project"])
os.chdir("wms_project")

# Create Django apps
print("Creating Django apps...")
subprocess.run(["python", "manage.py", "startapp", "dashboard"])
subprocess.run(["python", "manage.py", "startapp", "products"])
subprocess.run(["python", "manage.py", "startapp", "inventory"])
subprocess.run(["python", "manage.py", "startapp", "orders"])
subprocess.run(["python", "manage.py", "startapp", "suppliers"])
subprocess.run(["python", "manage.py", "startapp", "authentication"])

print("Project structure created successfully!")