variable "vpc_id" {
  description = "The VPC ID"
  type        = string
}

variable "subnets" {
  description = "The subnets"
  type        = list(string)

}

variable "vpc_sg" {
  description = "The security group"
  type        = string
}

variable "instance_a" {
  description = "value of ec2_a_id"
  type        = string
}

variable "instance_b" {
  description = "value of ec2_b_id"
  type        = string
}
