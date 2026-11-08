terraform {
  required_version = ">= 1.5, < 2.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.6.0"
    }
  }
}

provider "docker" {
  context = var.docker_context
}

data "docker_image" "gradebook" {
  name = var.image_name
}

resource "docker_container" "gradebook" {
  name  = var.container_name
  image = data.docker_image.gradebook.id
  env   = ["APP_VERSION=terraform-local"]
  wait  = true

  ports {
    internal = 8000
    external = var.host_port
    ip       = "127.0.0.1"
  }
}
