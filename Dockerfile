# Use an official Python runtime as a parent image
#FROM hub.hamdocker.ir/library/python:3.10
FROM python:3.10-alpine
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN touch /etc/resolv.conf
#RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Set the working directory in the container
WORKDIR /code
# Copy the requirements file into the container at /code/
COPY ./requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/

# Expose port 8000 to allow communication to/from server
EXPOSE 8000

# Define the command to run the application
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "core.wsgi:application"]
CMD ["sh", "/code/migrate_run.sh"]
