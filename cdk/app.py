#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags

from cdk.cdk_stack import CdkStack


app = cdk.App()

# Get service name from context
app_config = app.node.try_get_context("app_config")
service_name = app_config["dev"]["ecs_service_name"]

# Pass service name to the stack, so that we will use this name to the service.
stack = CdkStack(app, "CdkStack", service_name=service_name)

# Add project_name as a tag to all stack resources
Tags.of(stack).add("project_name", "github-gist")

# synthesis the cdk app, it will generates the CloudFormation template.
app.synth()
