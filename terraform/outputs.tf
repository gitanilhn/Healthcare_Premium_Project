#########################################################
# VPC
#########################################################

output "vpc_id" {
  value = aws_vpc.main.id
}

#########################################################
# Public Subnets
#########################################################

output "public_subnet_1" {
  value = aws_subnet.public_1.id
}

output "public_subnet_2" {
  value = aws_subnet.public_2.id
}

#########################################################
# EKS
#########################################################

output "cluster_name" {
  value = aws_eks_cluster.main.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.main.endpoint
}

output "cluster_version" {
  value = aws_eks_cluster.main.version
}

#########################################################
# IAM
#########################################################

output "cluster_role_arn" {
  value = aws_iam_role.eks_cluster_role.arn
}

output "node_role_arn" {
  value = aws_iam_role.node_group_role.arn
}