extends Node3D


func _ready():
	var asset = load("res://sculpture.glb").instantiate()
	asset.name = "Asset"
	add_child(asset)
	var floor_mesh = MeshInstance3D.new()
	floor_mesh.name = "Floor"
	var plane = PlaneMesh.new()
	plane.size = Vector2(200, 200)
	floor_mesh.mesh = plane
	var floor_material = StandardMaterial3D.new()
	floor_material.albedo_color = Color(0.16, 0.22, 0.28)
	floor_mesh.material_override = floor_material
	add_child(floor_mesh)
	var camera = Camera3D.new()
	camera.position = Vector3(5, 4, 6)
	camera.fov = 45
	add_child(camera)
	camera.look_at(Vector3(0, 1.25, 0))
	camera.current = true
	var light = DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-50, -25, 0)
	light.light_energy = 1.5
	light.shadow_enabled = true
	add_child(light)
	var environment = WorldEnvironment.new()
	environment.environment = Environment.new()
	environment.environment.background_mode = Environment.BG_COLOR
	environment.environment.background_color = Color(0.075, 0.11, 0.16)
	environment.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.environment.ambient_light_color = Color(0.8, 0.85, 1)
	environment.environment.ambient_light_energy = 0.5
	add_child(environment)
