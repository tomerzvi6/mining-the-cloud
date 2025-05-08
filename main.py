from attack_chain import ResourceManager, AttackChain, FakeDataGenerator, Logger
import pulumi

def main():
    resource_manager = ResourceManager()
    fake_data_generator = FakeDataGenerator()
    logger = Logger()
    attack_chain = AttackChain(resource_manager, logger, fake_data_generator)
    attack_chain.run()

    # Export Pulumi outputs
    if resource_manager.spot_instance:
        pulumi.export("spot_public_ip", resource_manager.spot_instance.public_ip)
        pulumi.export("spot_public_dns", resource_manager.spot_instance.public_dns)
    if resource_manager.ecr_repo:
        pulumi.export("ecr_repository_url", resource_manager.ecr_repo.repository_url)
    if resource_manager.s3_bucket:
        pulumi.export("s3_bucket_name", resource_manager.s3_bucket.id)

if __name__ == "__main__":
    main() 