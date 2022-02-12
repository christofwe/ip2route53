# ip2route53

Simple container that uses https://www.ipify.org/ and updates a DNS record in AWS Route53.

## Requirements:
- Docker execution runtime
- AWS account

## Steps
1. Create user in AWS IAM
2. Attach this minimal IAM policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Action": [
                "route53:ChangeResourceRecordSets"
            ],
            "Resource": [
                "arn:aws:route53:::hostedzone/[YOUR_HOSTED_ZONE_ID]"
            ]
        }
    ]
}
```
3. Generate IAM credentials
4. Copy `.env.sample` to `.env` and update w/ actual values
5. Run `docker-compose up -d`