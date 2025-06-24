# Mining the Cloud: Attack Chain Simulation

## Slide 5: System Architecture

```mermaid
classDiagram
    class AttackChain {
        +execute()
        +addStep()
        -steps: List
    }
    
    class ResourceManager {
        +createResources()
        +cleanupResources()
        -infrastructure: Map
    }
    
    class AttackStep {
        <<abstract>>
        +execute()
    }
    
    class ReconnaissanceStep {
        +execute()
        -targets: List
    }
    
    class PrivilegeEscalationStep {
        +execute()
        -techniques: List
    }
    
    class LateralMovementStep {
        +execute()
        -movements: List
    }
    
    class ImpactStep {
        +execute()
        -impact: String
    }
    
    class FakeDataGenerator {
        +generateData()
        -templates: Map
    }
    
    class Logger {
        +log()
        +getLogs()
        -logs: List
    }
    
    AttackChain --> ResourceManager
    AttackChain --> AttackStep
    AttackStep <|-- ReconnaissanceStep
    AttackStep <|-- PrivilegeEscalationStep
    AttackStep <|-- LateralMovementStep
    AttackStep <|-- ImpactStep
    AttackStep --> Logger
    AttackStep --> FakeDataGenerator
```

### Key Components:
- **AttackChain**: Orchestrates the entire attack simulation
- **ResourceManager**: Manages cloud infrastructure resources
- **Attack Steps**: Modular components for different attack phases
- **Support Services**: Data generation and logging utilities 