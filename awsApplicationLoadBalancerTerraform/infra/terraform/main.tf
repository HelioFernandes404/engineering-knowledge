module "vpc" {
  source   = "./modules/vpc"
  vpc_name = "vpc_public_webapi"
}

module "security_group" {
  source = "./modules/security_group"
  vpc_id = module.vpc.vpc_id
}

resource "aws_key_pair" "ssh_key_pair_public" {
  key_name   = "ssh_key_pair_public"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_instance" "instance_a" {
  ami           = "ami-0b72821e2f351e396"
  instance_type = "t2.micro"

  associate_public_ip_address = true
  subnet_id                   = module.vpc.subnets[0] // subnet_id = module.vpc.subnets[0]
  security_groups             = [module.security_group.id]

  key_name = aws_key_pair.ssh_key_pair_public.key_name

  user_data = file("user_data_a.sh")

  tags = {
    Name = "Instance A"
  }
}

resource "aws_instance" "instance_b" {
  ami           = var.ami
  instance_type = "t2.micro"

  associate_public_ip_address = true
  subnet_id                   = module.vpc.subnets[1] // subnet_id = module.vpc.subnets[1]
  security_groups             = [module.security_group.id]

  key_name = aws_key_pair.ssh_key_pair_public.key_name

  user_data = file("user_data_b.sh")

  tags = {
    Name = "Instance B"
  }
}

// ALB
module "load_balancer" {
  source = "./modules/load_balancer"

  vpc_sg  = module.security_group.id
  subnets = module.vpc.subnets
  vpc_id  = module.vpc.vpc_id

  instance_a = aws_instance.instance_a.id
  instance_b = aws_instance.instance_b.id
}

output "lb_dns_name" {
  value = module.load_balancer.lb_dns_name
}



