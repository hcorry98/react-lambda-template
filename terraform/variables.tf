variable "env" {
  type        = string
  description = "The branch being deployed"
}

variable "image_tag" {
  type        = string
  description = "The image tag for the Docker image (the timestamp)."
}
