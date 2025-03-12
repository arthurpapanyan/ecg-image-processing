### This services are very basic example of task based data processing implementation that is described in [TASK](../infrastructure/Readme.md.md)

- without database implementation
- without configuration management
- without environment managemnt

---

This guide provides step-by-step instructions to locally deploy the application using Docker. Follow the steps below to set up and run the application on your machine.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git**: [Install Git](https://git-scm.com/downloads)

---

## Steps to Deploy the Application

### 1. Clone the Repository

Clone the application repository to your local machine using the following command:

```bash
git clone https://github.com/arthurpapanyan/ecg-image-processing
```

### 2. Navigate to the services Directory

Change into the services directory where the docker-compose.yml file is located:

```bash
cd services
```

### 3. SpinUp services

```bash
docker-compose up --build
```

### 4. Execute following api call.

```bash
curl -X POST "http://localhost:8000/users/ecg_submissions/" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "user_id=1" \
-F "ecg_image=@path/to/ecg-image"
```
