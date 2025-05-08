from .resource_manager import ResourceManager
from .steps import ReconnaissanceStep, PrivilegeEscalationStep, LateralMovementStep, ImpactStep

class AttackChain:
    def __init__(self, resource_manager: ResourceManager, logger, fake_data_generator):
        self.resource_manager = resource_manager
        self.logger = logger
        self.fake_data_generator = fake_data_generator
        self.s3_bucket_name = None

    def reconnaissance(self):
        step = ReconnaissanceStep(self.logger, self.fake_data_generator)
        step.run()

    def privilege_escalation(self):
        step = PrivilegeEscalationStep(self.logger)
        step.run()

    def lateral_movement(self):
        step = LateralMovementStep(self.logger, self.fake_data_generator)
        step.run()

    def impact(self):
        step = ImpactStep(self.logger, self.fake_data_generator, self.s3_bucket_name)
        step.run()

    def run(self):
        # Create resources first
        sg = self.resource_manager.create_security_group()
        ecr = self.resource_manager.create_ecr_repository()
        s3 = self.resource_manager.create_s3_bucket()
        iam_role = self.resource_manager.create_iam_role()
        self.s3_bucket_name = s3.id if hasattr(s3, 'id') else None
        # Simulate attack chain
        self.reconnaissance()
        self.privilege_escalation()
        self.lateral_movement()
        self.impact() 