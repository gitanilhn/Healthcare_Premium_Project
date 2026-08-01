locals {

  project_name = "healthcare-premium"

  environment = "dev"

  common_tags = {

    Project = local.project_name

    Environment = local.environment

    ManagedBy = "Terraform"

    Owner = "Anil"

  }

}