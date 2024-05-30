# Use an official PHP runtime as a parent image
FROM php:7.4-cli

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Install pyVmomi using pip
RUN pip3 install pyVmomi

# Make port 80 available to the world outside this container
EXPOSE 80

# Run upload.php when the container launches
CMD ["php", "-S", "0.0.0.0:80", "-t", "."]
