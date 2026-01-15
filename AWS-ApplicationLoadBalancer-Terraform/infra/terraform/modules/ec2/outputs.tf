output "public_ip" {
  value = aws_instance.instance.public_ip
}

output "id" {
  value = aws_instance.instance.id
}

output "public_dns" {
  value = aws_instance.instance.public_dns
}
