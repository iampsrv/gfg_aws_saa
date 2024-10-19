# data "aws_ami" "ubuntu" {
#   most_recent = true

#   filter {
#     name   = "name"
#     values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
#   }

#   filter {
#     name   = "virtualization-type"
#     values = ["hvm"]
#   }

#   owners = ["099720109477"] # Canonical
# }

resource "aws_instance" "web" {
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t3.micro"
  subnet_id = aws_subnet.main.id
  associate_public_ip_address = true

  tags = {
    Name = "HelloWorld"
  }
}