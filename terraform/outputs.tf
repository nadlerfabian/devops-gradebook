output "app_url" {
  description = "Local URL of the Terraform-managed Gradebook instance."
  value       = "http://127.0.0.1:${var.host_port}"
}
