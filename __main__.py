import pulumi
from attack_chain.resource_manager import ResourceManager

# Instantiate the resource manager
resource_manager = ResourceManager()

# Create resources
sg = resource_manager.create_security_group()
ecr = resource_manager.create_ecr_repository()
s3 = resource_manager.create_s3_bucket()
iam_role = resource_manager.create_iam_role()

# Export outputs if available
if resource_manager.spot_instance:
    pulumi.export("spot_public_ip", resource_manager.spot_instance.public_ip)
    pulumi.export("spot_public_dns", resource_manager.spot_instance.public_dns)
if resource_manager.ecr_repo:
    pulumi.export("ecr_repository_url", resource_manager.ecr_repo.repository_url)
if resource_manager.s3_bucket:
    pulumi.export("s3_bucket_name", resource_manager.s3_bucket.id) 