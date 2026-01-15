output "aws_lb_target_group_arn" {
  value = aws_lb.my_alb.arn
}

output "lb_dns_name" {
  value = aws_lb.my_alb.dns_name
}
