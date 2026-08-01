#########################################################
# EKS Cluster IAM Role
#########################################################

resource "aws_iam_role" "eks_cluster_role" {

  name = "${local.project_name}-cluster-role"

  assume_role_policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {

        Effect = "Allow"

        Principal = {

          Service = "eks.amazonaws.com"

        }

        Action = "sts:AssumeRole"

      }

    ]

  })

  tags = local.common_tags
}

#########################################################
# Attach Required Policies
#########################################################

resource "aws_iam_role_policy_attachment" "cluster_policy" {

  role = aws_iam_role.eks_cluster_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"

}

resource "aws_iam_role_policy_attachment" "vpc_resource_controller" {

  role = aws_iam_role.eks_cluster_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"

}

#########################################################
# Node Group IAM Role
#########################################################

resource "aws_iam_role" "node_group_role" {

  name = "${local.project_name}-nodegroup-role"

  assume_role_policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {

        Effect = "Allow"

        Principal = {

          Service = "ec2.amazonaws.com"

        }

        Action = "sts:AssumeRole"

      }

    ]

  })

  tags = local.common_tags
}

#########################################################
# Worker Node Policies
#########################################################

resource "aws_iam_role_policy_attachment" "worker_node" {

  role = aws_iam_role.node_group_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"

}

resource "aws_iam_role_policy_attachment" "cni" {

  role = aws_iam_role.node_group_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"

}

resource "aws_iam_role_policy_attachment" "ecr" {

  role = aws_iam_role.node_group_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"

}