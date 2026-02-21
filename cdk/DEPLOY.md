# Deploy to AWS ECS Fargate

Deploy the Gists API to AWS using CDK.

## Prerequisites

- AWS Account
- AWS CLI configured (`aws configure`)
- Docker running
- CDK installed (`npm install -g aws-cdk`)

## Setup

1. Go to CDK directory:
```bash
cd cdk
```

2. Create virtual environment:
```bash
python3 -m venv .venv
```

3. Activate it:
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Deploy

1. Bootstrap CDK (first time only):
```bash
cdk bootstrap
```

2. Synthesize CloudFormation template:
```bash
cdk synth -c env=dev
```

3. Deploy:
```bash
cdk deploy -c env=dev
```

CDK will build your Docker image and create:
- VPC with 2 availability zones
- ECS Fargate cluster
- Container with load balancer
- Health checks on `/health`

4. After deployment, you'll get the load balancer URL:
```
Outputs:
CdkStack.LoadBalancerURL = http://CdkSt-Gists-XXXXX.us-east-1.elb.amazonaws.com
```

## Test

```bash
curl http://YOUR-ALB-URL/octocat
curl http://YOUR-ALB-URL/health
curl http://YOUR-ALB-URL/version
```

## Clean Up

```bash
cdk destroy
```

## What Gets Created

- VPC (2 AZs, public/private subnets)
- ECS Fargate Cluster
- Application Load Balancer
- Fargate Service (1 task, 256 CPU, 512 MB RAM)
- Security Groups
- IAM Roles

## Cost

Roughly $20-30/month:
- Fargate task running 24/7
- Application Load Balancer
- Data transfer

Stop the service when not using it to save money.
