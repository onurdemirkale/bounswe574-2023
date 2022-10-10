# The folder structure of the folders that contain this file is necessary
# to generate custom Django management commands.

import time 

# Errors that can be thrown if a connection to the database is attempted
# before it is fully initialized.
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError

# BaseCommand is the base class for creating custom Django 
# management commands.
from django.core.management.base import BaseCommand

# Waits for database to be available before Django attempts to connect
# to the database to avoid unexpected crashes.
class Command(BaseCommand):
  # The entroy methord for the command. Django management
  # framework automatically checks for handle method.
  def handle(self, *args, **options):
    self.stdout.write('Waiting for database to be available...')
    db_up = False
    while db_up is False:
      try:
        # self.check is a method that is available in the base command class 
        # to check if the Django app is ready. It is used here to check if 
        # the database is ready.
        # If we call self.check before the database is fully ready (database is fully initialized),
        # then it will throw an error which will be the Psycopg2OpError or OperationalError.
        self.check(databases=['default']) 
        db_up = True
      # These errors are checked for in the except block and then the connection
      # is retried in a second.
      except(Psycopg2OpError, OperationalError):
        self.stdout.write('Database currently unavailable, attempting connection again in one second...')
        time.sleep(1)

    self.stdout.write(self.style.SUCCESS('Database ready, establishing connection!'))


    
