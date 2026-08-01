###############################################
# Availability Zones
###############################################

data "aws_availability_zones" "available" {
  state = "available"
}

###############################################
# VPC
###############################################

resource "aws_vpc" "main" {

  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    local.common_tags,
    {
      Name = "${local.project_name}-vpc"
    }
  )
}

###############################################
# Internet Gateway
###############################################

resource "aws_internet_gateway" "main" {

  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    {
      Name = "${local.project_name}-igw"
    }
  )
}

###############################################
# Public Subnet 1
###############################################

resource "aws_subnet" "public_1" {

  vpc_id = aws_vpc.main.id

  cidr_block = var.public_subnet_1

  availability_zone = data.aws_availability_zones.available.names[0]

  map_public_ip_on_launch = true

  tags = merge(
    local.common_tags,
    {
      Name = "${local.project_name}-public-subnet-1"

      "kubernetes.io/role/elb" = "1"

      "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    }
  )
}

###############################################
# Public Subnet 2
###############################################

resource "aws_subnet" "public_2" {

  vpc_id = aws_vpc.main.id

  cidr_block = var.public_subnet_2

  availability_zone = data.aws_availability_zones.available.names[1]

  map_public_ip_on_launch = true

  tags = merge(
    local.common_tags,
    {
      Name = "${local.project_name}-public-subnet-2"

      "kubernetes.io/role/elb" = "1"

      "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    }
  )
}

###############################################
# Public Route Table
###############################################

resource "aws_route_table" "public" {

  vpc_id = aws_vpc.main.id

  route {

    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.main.id

  }

  tags = merge(
    local.common_tags,
    {
      Name = "${local.project_name}-public-route-table"
    }
  )
}

###############################################
# Route Table Association - Public 1
###############################################

resource "aws_route_table_association" "public_1" {

  subnet_id = aws_subnet.public_1.id

  route_table_id = aws_route_table.public.id

}

###############################################
# Route Table Association - Public 2
###############################################

resource "aws_route_table_association" "public_2" {

  subnet_id = aws_subnet.public_2.id

  route_table_id = aws_route_table.public.id

}