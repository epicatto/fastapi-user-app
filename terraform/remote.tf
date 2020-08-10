terraform {
  required_version = "~> 0.12.0"

  backend "remote" {
    organization = "ezedev"

    workspaces {
      name = "fastapi-test-dev"
    }
  }
}