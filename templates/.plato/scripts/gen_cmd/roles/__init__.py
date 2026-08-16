from .designer import DesignerStrategy
from .planner import PlannerStrategy
from .coder import CoderStrategy
from .fixer import FixerStrategy

ROLE_STRATEGIES: dict = {
    "designer": DesignerStrategy(),
    "planner": PlannerStrategy(),
    "coder": CoderStrategy(),
    "fixer": FixerStrategy(),
}
