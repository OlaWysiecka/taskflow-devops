# TaskFlow Terraform

## Purpose

This directory contains Terraform configuration for checking connectivity
to the Docker Engine used by the TaskFlow environment.

The current configuration does not provision the VirtualBox VM or manage
the application's containers.

## Requirements

- Terraform >= 1.6
- Docker Engine running on the Ubuntu server
- Permission to access the Docker socket

## Usage

Initialize Terraform:

```bash
terraform init