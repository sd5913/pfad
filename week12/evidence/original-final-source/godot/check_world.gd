extends SceneTree

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var world = load("res://world.tscn").instantiate()
    root.add_child(world)
    world.set_physics_process(false)
    var exit_locked: bool = not world.won and world.collected == 0
    for frame in range(180):
        world.advance(1.0 / 60.0, true)
    var result := {"exit_locked_initially":exit_locked, "collected":world.collected,
        "won_by_180_frames":world.won, "player_x":world.player.x, "ticks":world.ticks,
        "speed":world.config.speed, "engine":Engine.get_version_info().string}
    var passed: bool = exit_locked and world.collected == 3 and world.won
    result["passed"] = passed
    print("WORLD_CHECK " + JSON.stringify(result))
    quit(0 if passed else 1)
