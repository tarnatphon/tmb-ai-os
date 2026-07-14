from apply_milestone_4_2 import main as apply_wrappers
from patch_canonical_config import main as patch_config


def main() -> None:
    patch_config()
    apply_wrappers()


if __name__ == "__main__":
    main()
