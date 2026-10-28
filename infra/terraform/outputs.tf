
output "docker_network_name" {
  description = "Name of the Docker network managed by Terraform"
  value       = docker_network.taskflow.name
}

output "docker_network_id" {
  description = "ID of the Docker network managed by Terraform"
  value       = docker_network.taskflow.id
}
