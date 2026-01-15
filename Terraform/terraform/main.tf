terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.57.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Create a VPC
module "minha_vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.9.0"
  
  name = "minha-vpc-terraform"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = false # Change this to true if you want to provision NAT Gateways for each of your private subnets https://aws.amazon.com/pt/vpc/pricing/
  enable_vpn_gateway = false

  default_security_group_name = "minha-vpc-terraform-sg"

  tags = {
    Terraform = "true"
    Environment = "dev"
  }
}


# Create an EC2 Instance
module "ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"

  name = "terraform-single-instance"
  instance_type          = "t2.micro" 

  subnet_id              = module.minha_vpc.private_subnets[0]
  key_name               = null # Change this to your key pair name
  monitoring             = false # Change this to true if you want to enable detailed monitoring
  vpc_security_group_ids = null
 

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }

}
