resource "aws_key_pair" "my_kp" {
  key_name   = "ssh_key_pair_public"
  public_key = file("~/.ssh/id_rsa.pub")

}

resource "aws_instance" "instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  user_data     = var.data_user

  key_name        = aws_key_pair.my_kp.key_name
  subnet_id       = var.public_subnet_id
  security_groups = [var.security_group_id]

  associate_public_ip_address = true

  tags = {
    Name = var.instance_name
  }

}
