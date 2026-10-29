extends Node2D
## Shared behavior for play, deterministic replay and the engine check.
var config: Dictionary
var player := Vector2(80, 300)
var pickups := [Vector2(240, 300), Vector2(420, 300), Vector2(600, 300)]
var collected := 0
var won := false
var ticks := 0
var replay := false

func _ready() -> void:
    config = JSON.parse_string(FileAccess.get_file_as_string("res://world.json"))
    replay = "--replay" in OS.get_cmdline_user_args()

func advance(delta: float, automatic: bool) -> void:
    if won:
        return
    ticks += 1
    var target := Vector2(float(config.exit_x), 300)
    if collected < pickups.size():
        target = pickups[collected]
    if automatic:
        player = player.move_toward(target, float(config.speed) * delta)
    else:
        player += Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down") * float(config.speed) * delta
        player = player.clamp(Vector2(24, 100), Vector2(936, 480))
    if collected < pickups.size() and player.distance_to(pickups[collected]) <= float(config.pickup_radius):
        collected += 1
    won = collected == 3 and player.distance_to(Vector2(float(config.exit_x), 300)) <= 20

func _physics_process(delta: float) -> void:
    advance(delta, replay)
    queue_redraw()

func _draw() -> void:
    draw_rect(Rect2(45, 270, 870, 60), Color("29424c"))
    draw_rect(Rect2(float(config.get("exit_x", 860)) - 20, 240, 40, 120), Color("79d5bb") if collected == 3 else Color("627881"))
    for index in range(collected, pickups.size()):
        draw_circle(pickups[index], float(config.get("pickup_radius", 24)), Color("ffd074"))
    draw_circle(player, 19, Color("f6f1e8"))
    var font := ThemeDB.fallback_font
    draw_string(font, Vector2(48, 75), "THREE LIGHTS  /  %d OF 3" % collected, HORIZONTAL_ALIGNMENT_LEFT, -1, 32, Color("f6f1e8"))
    draw_string(font, Vector2(48, 130), "EXIT OPEN" if collected == 3 else "Collect each light to open the exit", HORIZONTAL_ALIGNMENT_LEFT, -1, 23, Color("ffd074"))
    draw_string(font, Vector2(48, 470), "COMPLETE" if won else "Arrow keys to move  /  route: left to right", HORIZONTAL_ALIGNMENT_LEFT, -1, 24, Color("f6f1e8"))
