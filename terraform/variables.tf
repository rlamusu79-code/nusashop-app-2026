variable "aws_region" {
  description = "Region AWS untuk deploy semua resource"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment (production / staging)"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block untuk VPC utama"
  type        = string
  default     = "10.10.0.0/16"
}

variable "public_subnet_a_cidr" {
  description = "CIDR public subnet AZ-a"
  type        = string
  default     = "10.10.0.0/26"
}

variable "public_subnet_b_cidr" {
  description = "CIDR public subnet AZ-b"
  type        = string
  default     = "10.10.0.64/26"
}

variable "private_subnet_a_cidr" {
  description = "CIDR private subnet AZ-a"
  type        = string
  default     = "10.10.1.0/26"
}

variable "private_subnet_b_cidr" {
  description = "CIDR private subnet AZ-b"
  type        = string
  default     = "10.10.1.64/26"
}

variable "participant_id" {
  description = "ID peserta (digunakan untuk penamaan resource unik)"
  type        = string
}
