#!/usr/bin/env python3

"""
PoC - diagram as code
brew install graphviz
(venv) pip install diagrams
"""

from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3

with Diagram("Diagram PoC", show=False):
    source = EKS('k8s source')

    with Cluster("Event Flows"):
        with Cluster("Event Workers"):
            workers = [ECS("w1"), ECS("w2")]

    store = S3("Events Store")
    db = Dynamodb("Analytics")

print('Goodbye')