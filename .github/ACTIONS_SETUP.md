# GitHub Actions Setup

This workflow automatically deploys your CDK stack to AWS when you push to the main branch.

## Setup Steps

### 1. Add AWS Credentials to GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key

### 2. Update AWS Region (if needed)

Edit `.github/workflows/deploy-cdk.yml` and change:
```yaml
aws-region: us-east-1  # Change to your region
```

### 3. Trigger Deployment

**Automatic:**
- Push to `main` branch triggers deployment

**Manual:**
- Go to Actions tab → Deploy CDK to AWS → Run workflow

## What the Workflow Does

1. Checks out your code
2. Sets up Node.js and Python
3. Installs AWS CDK
4. Configures AWS credentials
5. Installs Python dependencies
6. Runs `cdk bootstrap` (first time only)
7. Runs `cdk deploy` with dev environment

## Monitoring

- View deployment progress in Actions tab
- Check CloudFormation in AWS Console
- Get load balancer URL from workflow output
