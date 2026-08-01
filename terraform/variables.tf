#########################################################
# AWS
#########################################################

variable "aws_region" {
  type = string
}

#########################################################
# EKS
#########################################################

variable "cluster_name" {
  type = string
}

variable "kubernetes_version" {
  type    = string
  default = "1.33"
}

#########################################################
# Networking
#########################################################

variable "vpc_cidr" {
  type = string
}

variable "public_subnet_1" {
  type = string
}

variable "public_subnet_2" {
  type = string
}

#########################################################
# Node Group
#########################################################

variable "node_instance_type" {
  type    = string
  default = "t3.medium"
}

variable "desired_size" {
  type    = number
  default = 2
}

variable "min_size" {
  type    = number
  default = 2
}

variable "max_size" {
  type    = number
  default = 3
}