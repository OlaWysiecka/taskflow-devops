variable "docker_host" {
  description = "Docker Engine endpoint on the Ubuntu server"
  type        = string
  default     = "unix:///var/run/docker.sock"
}