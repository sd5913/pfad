# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame==2.6.1", "watchfiles==1.3.0"]
# ///
"""A graphical view of the shared Ball physics model."""

if __package__:
    from .ball_live import Simulation
else:
    from ball_live import Simulation

SIZE = (960, 680)
COLORS = ((255, 116, 83), (109, 208, 221))


def main(show_ascii=False):
    import pygame

    pygame.init()
    screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Ball physics | SD5913 Week 7")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 26)
    heading = pygame.font.Font(None, 38)
    simulation = Simulation()
    ascii_view = None
    if show_ascii:
        if __package__:
            from .ball_play import AsciiView
        else:
            from ball_play import AsciiView
        ascii_view = AsciiView()
    last_status = None
    paused = False
    running = True

    try:
        while running:
            seconds = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        simulation.reload()
                    elif event.key == pygame.K_SPACE:
                        paused = not paused

            simulation.advance(0 if paused else seconds)
            width, height = screen.get_size()
            scale = max(0.1, min((width - 56) / simulation.model.WIDTH,
                                 (height - 150) / simulation.model.HEIGHT))
            arena = pygame.Rect(0, 0, round(simulation.model.WIDTH * scale),
                                round(simulation.model.HEIGHT * scale))
            arena.center = (width // 2, (height - 80) // 2 + 35)

            screen.fill((21, 35, 38))
            pygame.draw.rect(screen, (28, 46, 50), arena)
            pygame.draw.rect(screen, (112, 133, 128), arena, 2)
            title = "One model. Two views." if show_ascii else "Ball physics"
            screen.blit(heading.render(title, True, (242, 238, 221)), (28, 20))
            for index, ball in enumerate(simulation.balls):
                center = (round(arena.left + ball.x * scale), round(arena.top + ball.y * scale))
                radius = max(2, round(ball.radius * scale))
                pygame.draw.circle(screen, COLORS[index % len(COLORS)], center, radius)
                pygame.draw.circle(screen, (242, 238, 221),
                                   (center[0] - radius // 3, center[1] - radius // 3), max(1, radius // 5))

            controls = "Space: pause / resume   R: reset   Save ball.py: reload"
            screen.blit(font.render(controls, True, (242, 238, 221)), (28, height - 69))
            state = "PAUSED" if paused else "MOVING"
            status = f"{state} / frame {simulation.ticks} / revision {simulation.revision}"
            screen.blit(font.render(status, True, (255, 217, 117)), (28, height - 42))
            if "Error:" in simulation.status:
                pygame.display.set_caption("Ball physics | edit error: see terminal")
                if ascii_view is None and simulation.status != last_status:
                    print(simulation.status)
            else:
                pygame.display.set_caption("Ball physics | SD5913 Week 7")
            last_status = simulation.status
            if ascii_view is not None:
                ascii_view.draw(simulation)
            pygame.display.flip()
    except KeyboardInterrupt:
        pass
    finally:
        simulation.close()
        if ascii_view is not None:
            ascii_view.close()
        pygame.quit()


if __name__ == "__main__":
    main()
