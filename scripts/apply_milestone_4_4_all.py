from apply_milestone_4_4 import main as apply_wrappers
from patch_milestone_4_4_config import main as patch_config
from patch_milestone_4_4_lifespan import main as patch_lifespan


def main() -> None:
    patch_config()
    patch_lifespan()
    apply_wrappers()


if __name__ == "__main__":
    main()
