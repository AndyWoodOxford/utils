#!/usr/bin/env python3

"""
Enhanced VPC Diagram with Security Layers
brew install graphviz
(venv) pip install diagrams
Thank you, ChatGPT :-)
"""

from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import ALB, InternetGateway, NATGateway
from diagrams.aws.database import RDS
from diagrams.aws.security import WAF, Shield, KMS
from diagrams.onprem.client import User

with Diagram("Secure VPC Architecture", show=True, filename="secure_vpc_diagram"):

    # External Client
    client = User("Client")

    with Cluster("VPC"):

        # Edge Security
        waf = WAF("AWS WAF")
        igw = InternetGateway("Internet Gateway")

        # Represent security Groups
        alb_sg = Shield("ALB SG")
        web_sg = Shield("Web SG")
        middleware_sg = Shield("Middleware SG")
        rds_sg = Shield("DB SG")

        # Application Load Balancer
        alb = ALB("Application Load Balancer")

        # Public Subnets
        with Cluster("Public Subnet 1"):
            web1 = EC2("Web Server 1")
        with Cluster("Public Subnet 2"):
            web2 = EC2("Web Server 2")
        with Cluster("Public Subnet 3"):
            web3 = EC2("Web Server 3")

        # Private Subnets
        with Cluster("Private Subnet 1"):
            middleware1 = EC2("Middleware 1")
        with Cluster("Private Subnet 2"):
            middleware2 = EC2("Middleware 2")
        with Cluster("Private Subnet 3"):
            middleware3 = EC2("Middleware 3")

        # NAT Gateway for private outbound internet
        nat = NATGateway("NAT Gateway")

        # Database
        rds = RDS("Application Database")
        kms = KMS("KMS Encryption")

        # Connections (flow + security layers)
        client >> waf >> igw >> alb_sg >> alb

        alb >> web_sg >> [web1, web2, web3]

        [web1, web2, web3] >> middleware_sg >> [middleware1, middleware2, middleware3]

        [middleware1, middleware2, middleware3] >> rds_sg >> rds

        # Private instances can access the internet via NAT
        [middleware1, middleware2, middleware3] >> nat

        # Database encryption
        rds >> kms
