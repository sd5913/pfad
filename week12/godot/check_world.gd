extends SceneTree

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var premature_rejected := true
    for count in range(3):
        var probe = load("res://world.tscn").instantiate()
        root.add_child(probe)
        probe.set_physics_process(false)
        probe.player = Vector2(float(probe.config.exit_x), 300)
        probe.collected = count
        probe.advance(0.0, false)
        premature_rejected = premature_rejected and not probe.won
        probe.free()
    var world = load("res://world.tscn").instantiate()
    root.add_child(world)
    world.set_physics_process(false)
    var exit_locked: bool = not world.won and world.collected == 0
    for frame in range(180):
        world.advance(1.0 / 60.0, true)
    var final_position: Vector2 = world.player
    var final_ticks: int = world.ticks
    if world.won:
        world.advance(1.0 / 60.0, true)
    var stopped: bool = world.won and world.player == final_position and world.ticks == final_ticks
    var result := {"exit_locked_initially":exit_locked, "collected":world.collected,
        "won_by_180_frames":world.won, "player_x":world.player.x, "ticks":world.ticks,
        "speed":world.config.speed, "engine":Engine.get_version_info().string}
    result["premature_exit_rejected"] = premature_rejected
    result["premature_exit_cases"] = [0, 1, 2]
    result["stopped_after_win"] = stopped
    var passed: bool = exit_locked and premature_rejected and world.collected == 3 and world.won and stopped
    result["passed"] = passed
    print("WORLD_CHECK " + JSON.stringify(result))
    quit(0 if passed else 1)
