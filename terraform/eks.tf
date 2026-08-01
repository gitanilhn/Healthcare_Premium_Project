#########################################################
# EKS Cluster
#########################################################

resource "aws_eks_cluster" "main" {

  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn

  version = var.kubernetes_version

  vpc_config {

    subnet_ids = [

      aws_subnet.public_1.id,
      aws_subnet.public_2.id

    ]

    endpoint_private_access = false
    endpoint_public_access  = true

  }

  depends_on = [

    aws_iam_role_policy_attachment.cluster_policy,
    aws_iam_role_policy_attachment.vpc_resource_controller

  ]

  tags = merge(

    local.common_tags,

    {

      Name = var.cluster_name

    }

  )

}

#########################################################
# Managed Node Group
#########################################################

resource "aws_eks_node_group" "main" {

  cluster_name = aws_eks_cluster.main.name

  node_group_name = "${local.project_name}-node-group"

  node_role_arn = aws_iam_role.node_group_role.arn

  subnet_ids = [

    aws_subnet.public_1.id,
    aws_subnet.public_2.id

  ]

  instance_types = [

    var.node_instance_type

  ]

  capacity_type = "ON_DEMAND"

  scaling_config {

    desired_size = var.desired_size

    min_size = var.min_size

    max_size = var.max_size

  }

  update_config {

    max_unavailable = 1

  }

  depends_on = [

    aws_iam_role_policy_attachment.worker_node,

    aws_iam_role_policy_attachment.cni,

    aws_iam_role_policy_attachment.ecr

  ]

  tags = merge(

    local.common_tags,

    {

      Name = "${local.project_name}-node-group"

    }

  )

}