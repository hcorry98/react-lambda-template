locals {
  project_name = "ProjectName"
  app_name     = "app-name"
}

resource "aws_ecr_repository" "ecr_repo" {
  name = "${local.app_name}-repo"

  image_scanning_configuration {
    scan_on_push = true
  }
}

module "react_lambda" {
  source = "github.com/byuawsfhtl/terraform-react-lambda?ref=prd"

  project_name = local.project_name
  app_name     = local.app_name
  env          = var.env

  ecr_repo  = aws_ecr_repository.ecr_repo
  image_tag = var.image_tag

  lambda_environment_variables = { "TAG" = var.image_tag } # Optional
  lambda_endpoint_definitions = [
    {
      path_part       = "endpoint-path"
      allowed_headers = "Custom-Function-Header1,Custom-Function-Header2" # Optional
      method_definitions = [
        {
          http_method = "GET"
          command     = ["file_name.function_name"]
          timeout     = 15  # Optional
          memory_size = 256 # Optional
        }
      ]
    }
  ]

  lambda_policies = [

  ]
}
