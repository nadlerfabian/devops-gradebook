# Run Gradebook with Terraform

Terraform manages one local Gradebook container. The Docker provider looks up
the existing image and creates the container from that image ID. The app uses
in-memory storage for this demonstration. The default host port is 8081, so
the Compose app can continue using 8000.

Use Terraform 1.5 or later in the 1.x series and a running Docker engine.
This configuration uses the maintained Docker provider 4.6 series. The
course example uses 3.x. Later 3.x releases had registry signing issues,
so this configuration uses a bounded 4.x version from the Terraform Registry.

Run these commands from the repository root in PowerShell:

```powershell
docker build -t gradebook:local .
$env:TF_VAR_docker_context = docker context show
terraform -chdir=terraform init
terraform -chdir=terraform fmt -check
terraform -chdir=terraform validate
terraform -chdir=terraform plan
```

The first command builds the local image. The second passes the active Docker
context to the provider, typically `desktop-linux` on Windows. Terraform
downloads the provider and writes the lock file during `init`. Formatting
and validation checks inspect the configuration. The plan previews the change
without creating the container. Save the plan output for course evidence.

```powershell
terraform -chdir=terraform apply
$gradebookUrl = terraform -chdir=terraform output -raw app_url
Invoke-RestMethod "$gradebookUrl/health"
terraform -chdir=terraform plan
```

Review the plan in `apply` and enter `yes` to create the container. The
provider waits for the Docker health check. The HTTP response should report
`status: ok` and `version: terraform-local`. A second plan should report no
changes. You can verify port validation with
`terraform -chdir=terraform plan -var="host_port=80"`.

```powershell
terraform -chdir=terraform destroy
docker ps -a --filter "name=gradebook-terraform"
```

Review the destroy plan and enter `yes`. The Docker listing should show no
matching container. The prebuilt image remains available for Compose because
Terraform reads it as a data source.

Defaults are defined in the variable declarations. To override image, name,
or host port, copy the example to `terraform/terraform.tfvars` and edit it.
Commit the generated `.terraform.lock.hcl`. State files, provider downloads,
and local variable files stay out of Git.
