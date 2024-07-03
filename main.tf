locals {
  demoflageval_fname    = "${var.unique_identifier}_lambda_demoflageval"
  demoflageval_loggroup = "/aws/lambda/${local.demoflageval_fname}"
}

provider "aws" {
  region = var.aws_region
}

provider "archive" {}
