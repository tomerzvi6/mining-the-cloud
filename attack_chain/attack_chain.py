from .resource_manager import ResourceManager
from .steps import ReconnaissanceStep, PrivilegeEscalationStep, LateralMovementStep, ImpactStep

class AttackChain:
    def __init__(self, resource_manager: ResourceManager, fake_data_generator):
        self.resource_manager = resource_manager
        self.fake_data_generator = fake_data_generator

    def reconnaissance(self):
        step = ReconnaissanceStep(self.fake_data_generator)
        step.run()

    def privilege_escalation(self):
        step = PrivilegeEscalationStep()
        step.run()

    def lateral_movement(self):
        step = LateralMovementStep(self.fake_data_generator)
        step.run()

    def impact(self):
        step = ImpactStep(self.fake_data_generator)
        step.run()

    def run(self):
        # --- STORY CONTEXT ---
        # The attacker obtained AWS credentials by accessing the in-org LLM (Large Language Model) web interface.
        # The DevOps user had once pasted their AWS access and secret key into the LLM, which was saved in its memory.
        # The attacker gained access to the LLM via a stolen session cookie and used prompt injection to extract the keys.
        # These long-term credentials (no MFA) are now used to attack the me-south-1 region.
        # ----------------------
        # Create resources first
        sg = self.resource_manager.create_security_group()
        ecr = self.resource_manager.create_ecr_repository()
        s3 = self.resource_manager.create_s3_bucket()
        iam_role = self.resource_manager.create_iam_role()
        # Simulate attack chain
        self.reconnaissance()
        self.privilege_escalation()
        self.lateral_movement()
        self.impact() 