terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote State di S3
  # Ganti bucket_name sesuai peserta
  backend "s3" {
    bucket = "s3-nusashop-assets-2026-PARTICIPANT_ID"
    key    = "terraform/state.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "LKS-CC-2026"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# ── VPC ──────────────────────────────────────────────────────────
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name         = "vpc-lks-cc-2026-nusashop"
    "LKS-CC-2026" = "VPC"
  }
}

# ── Internet Gateway ─────────────────────────────────────────────
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name         = "igw-lks-cc-2026"
    "LKS-CC-2026" = "INTERNET-GW"
  }
}

# ── Subnets Public ───────────────────────────────────────────────
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_a_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name         = "public-subnet-a-2026"
    "LKS-CC-2026" = "PUBLIC-SUBNET-A"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_b_cidr
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true

  tags = {
    Name         = "public-subnet-b-2026"
    "LKS-CC-2026" = "PUBLIC-SUBNET-B"
  }
}

# ── Subnets Private ──────────────────────────────────────────────
resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_a_cidr
  availability_zone = "${var.aws_region}a"

  tags = {
    Name         = "private-subnet-a-2026"
    "LKS-CC-2026" = "PRIVATE-SUBNET-A"
  }
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_b_cidr
  availability_zone = "${var.aws_region}b"

  tags = {
    Name         = "private-subnet-b-2026"
    "LKS-CC-2026" = "PRIVATE-SUBNET-B"
  }
}

# ── Elastic IP untuk NAT Gateway ─────────────────────────────────
resource "aws_eip" "nat" {
  domain = "vpc"
  tags = { Name = "eip-nat-gw-2026" }
}

# ── NAT Gateway ──────────────────────────────────────────────────
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_a.id

  tags = {
    Name         = "nat-gw-lks-cc-2026"
    "LKS-CC-2026" = "NAT-GW"
  }

  depends_on = [aws_internet_gateway.main]
}

# ── Route Table Public ───────────────────────────────────────────
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name         = "public-route-table"
    "LKS-CC-2026" = "PUBLIC-ROUTE"
  }
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

# ── Route Table Private ──────────────────────────────────────────
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name         = "private-route-table"
    "LKS-CC-2026" = "PRIVATE-ROUTE"
  }
}

resource "aws_route_table_association" "private_a" {
  subnet_id      = aws_subnet.private_a.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_b" {
  subnet_id      = aws_subnet.private_b.id
  route_table_id = aws_route_table.private.id
}
