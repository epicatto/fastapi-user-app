terraform {
  required_version = "~> 0.12.0"

  backend "remote" {
    organization = "ezedev"
    token = "MEdEGQwuyxPv9g.atlasv1.f9DWi0b6D1vFy6PI3Pp7JQmDYIMT0PgzMhozr2zfvIxKvp3oPK5eWD8mw7M9IaOMNmw"

    workspaces {
      name = "fastapi-test-dev"
    }
  }
}