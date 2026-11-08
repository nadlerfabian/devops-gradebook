variable "docker_context" {
  description = "Docker CLI context to use. Null lets the provider choose its default."
  type        = string
  default     = null
}

variable "image_name" {
  description = "Tag of the Gradebook image already built on the Docker host."
  type        = string
  default     = "gradebook:local"
}

variable "container_name" {
  description = "Name of the container managed by Terraform."
  type        = string
  default     = "gradebook-terraform"
}

variable "host_port" {
  description = "Local port that forwards to Gradebook on container port 8000."
  type        = number
  default     = 8081

  validation {
    condition     = var.host_port == floor(var.host_port) && var.host_port > 1024 && var.host_port <= 65535
    error_message = "The host port must be a whole number between 1025 and 65535."
  }
}
