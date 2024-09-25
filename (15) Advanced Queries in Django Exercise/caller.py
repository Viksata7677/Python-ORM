import os
import django

from main_app.models import VideoGame

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Run and print your queries
# Create instances of VideoGame with real data
