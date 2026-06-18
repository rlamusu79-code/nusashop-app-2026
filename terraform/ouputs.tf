output "vpc_id" {
  description = "ID dari VPC yang dibuat"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "ID subnet public (untuk ALB)"
  value       = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

output "private_subnet_ids" {
  description = "ID subnet private (untuk EC2 / ECS)"
  value       = [aws_subnet.private_a.id, aws_subnet.private_b.id]
}

output "internet_gateway_id" {
  description = "ID Internet Gateway"
  value       = aws_internet_gateway.main.id
}

output "nat_gateway_id" {
  description = "ID NAT Gateway"
  value       = aws_nat_gateway.main.id
}

output "nat_gateway_public_ip" {
  description = "IP publik NAT Gateway"
  value       = aws_eip.nat.public_ip
}
