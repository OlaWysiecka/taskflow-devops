# TaskFlow - DevOps Diploma Project

---

## 1. Description

TaskFlow is a web application for task management, allowing users to create, edit, delete, and track tasks and their
completion status.

The project demonstrates practical DevOps practices, including automated testing, containerization, CI/CD,
Infrastructure as Code (IaC), and application monitoring.

The application will run in two separate environments: development (DEV) and production (PROD). The infrastructure will
be hosted locally, without relying on paid cloud services.

---

## 2. Technology Stack

- Application: Python, Flask, HTML, Jinja2
- Testing: pytest
- Version Control: Git, GitHub
- IDE: Visual Studio Code
- CI/CD: GitHub Actions
- Containerization: Docker, Docker Compose
- Infrastructure as Code: Terraform
- Container Registry: GitHub Container Registry (GHCR)
- Monitoring: Prometheus, Grafana
- Deployment Environment: Ubuntu Server, VirtualBox

---

## 3. Application Overview

TaskFlow is a web-based task management application built with Python and Flask. It allows users to create, view, edit,
delete, and track tasks through a simple web interface.

The application uses SQLAlchemy for database operations and Jinja2 to render dynamic HTML pages. Its modular structure
separates request handling, database models, and presentation logic.

The application supports standard CRUD operations and provides a /health endpoint for checking application availability.

The initial development version uses SQLite, with PostgreSQL planned for the separate DEV and PROD environments.

---

## 4. Environments

### DEV - Development Environment

The development environment is used for implementing new features, testing changes, and debugging the application.

Planned configuration:

* Runs locally on Windows using Docker Compose.
* Uses a dedicated PostgreSQL database and separate data volumes.
* Supports application development and automated tests.
* Does not share application data or database volumes with PROD.

### PROD - Production Environment

The production environment hosts the stable version of TaskFlow on a local Ubuntu Server virtual machine.

#### Planned configuration:

* Runs the application and its dependencies in Docker containers.
* Uses a separate PostgreSQL database and persistent data volumes.
* Receives application updates through the automated deployment pipeline.
* Uses Prometheus and Grafana for monitoring.
  Performs health checks after deployment.

---

## 5. CI/CD Pipeline

GitHub Actions will automate the build, testing, artifact publication, and deployment processes.

### Continuous Integration (CI)

On pushes to branches and pull requests:

* Check out the source code.
* Run code quality checks using Ruff.
* Execute automated tests using pytest.
* Build the Docker image.
* Publish the image to GHCR after successful checks, for eligible branch pushes.
* Send a notification about the pipeline result.

### Continuous Deployment (CD)

After a successful build and publication from the main branch:

* Deploy the published Docker image to the PROD environment.
* Verify application health.
* Send a notification about the deployment result.

Deployment will use a self-hosted GitHub Actions runner or another securely configured mechanism
with access to the local virtual machine.

--- 

## 6. Infrastructure as Code

Terraform will be used to define and manage deployment resources. Docker Compose will define the application
services and their configuration.

The goal is to make the deployment environment reproducible, minimize manual configuration, and verify
the idempotency of infrastructure changes.

---

## 7. Monitoring

Prometheus will collect application and infrastructure metrics. Grafana will visualize the metrics using
dashboards and support alerting.

Planned monitoring capabilities include:

* Application availability.
* HTTP request and error counts.
* Application response times.
* Container and infrastructure metrics.
* Health checks and alerts.

---

## 8. Repository Structure

The repository will contain:

* app/ - Flask application source code.
* tests/ - automated tests.
* infra/ - Terraform configuration and infrastructure automation.
* monitoring/ - Prometheus and Grafana configuration.
* .github/workflows/ - CI/CD workflows.
* Dockerfile - application image definition.
* compose.yaml and environment-specific Compose files - service configuration.
* README.md - project documentation.

---

## 9. Project Goals

- Develop a functional task management application.
- Automate code testing and Docker image builds.
- Publish application images to GHCR.
- Implement automated deployment from the main branch.
- Manage infrastructure using Terraform.
- Monitor application health and performance.
- Document the deployment and recovery process.

---

## 10. Current Status

The initial Flask application with CRUD functionality, automated tests, and code quality checks is implemented. The application is containerized using Docker and Docker Compose, with PostgreSQL configured for the DEV environment.

PostgreSQL integration tests have been implemented using a dedicated test database and a separate Docker Compose configuration. Gunicorn has been configured as the production application server.

CI/CD automation, infrastructure provisioning, production deployment, and monitoring are still in progress.