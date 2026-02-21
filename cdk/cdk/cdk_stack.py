from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, service_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "GistsVpc", max_azs=2)
        
        # Create ECS Cluster
        cluster = ecs.Cluster(self, "GistsCluster", vpc=vpc)
        
        # Create Fargate Service with ALB
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, service_name,
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../"),
                container_port=8080,
            ),
            public_load_balancer=True,
        )
        
        # Health check
        fargate_service.target_group.configure_health_check(
            path="/health",
        )
        
        # Output the load balancer URL
        CfnOutput(self, "LoadBalancerURL",
            value=f"http://{fargate_service.load_balancer.load_balancer_dns_name}",
            description="Load Balancer URL"
        )
