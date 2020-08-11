terraform {
  required_version = "0.12.29"

  backend "remote" {
    organization = "ezedev"

    workspaces {
      name = "fastapi-test-dev"
    }
  }
}