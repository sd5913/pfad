# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame==2.6.1", "watchfiles==1.3.0"]
# ///
"""Run synchronized ASCII and Pygame views of one simulation."""

if __package__:
    from .ball_pygame import main as run_pygame
else:
    from ball_pygame import main as run_pygame


def main():
    run_pygame(show_ascii=True)


if __name__ == "__main__":
    main()
