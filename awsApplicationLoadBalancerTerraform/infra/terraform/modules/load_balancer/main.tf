// Target group
resource "aws_lb_target_group" "my_tg_a" { // Target group A
  name     = "target-group-a"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

resource "aws_lb_target_group" "my_tg_b" { // Target group B
  name     = "target-group-b"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

// Target group attachment
resource "aws_lb_target_group_attachment" "tg_attachment_a" {
  target_group_arn = aws_lb_target_group.my_tg_a.arn
  target_id        = var.instance_a
  port             = 80
}

resource "aws_lb_target_group_attachment" "tg_attachment_b" {
  target_group_arn = aws_lb_target_group.my_tg_b.arn
  target_id        = var.instance_b
  port             = 80
}

// ALB
resource "aws_lb" "my_alb" {
  name               = "my-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.vpc_sg]
  subnets            = var.subnets

  tags = {
    Environment = "dev"
  }
}

// Listener
resource "aws_lb_listener" "my_listener" {
  load_balancer_arn = aws_lb.my_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_tg_a.arn
  }
}

resource "aws_lb_listener_rule" "rule_a" {
  listener_arn = aws_lb_listener.my_listener.arn
  priority     = 60

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_tg_a.arn
  }

  condition {
    path_pattern {
      values = ["/"]
    }
  }
}

resource "aws_lb_listener_rule" "rule_b" {
  listener_arn = aws_lb_listener.my_listener.arn
  priority     = 40

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_tg_b.arn
  }

  condition {
    path_pattern {
      values = ["/v1/*"]
    }
  }
}
