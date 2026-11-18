extends SceneTree


func _initialize():
	call_deferred("check_asset")


func check_asset():
	var preview = load("res://preview.tscn").instantiate()
	root.add_child(preview)
	var asset = preview.get_node("Asset")
	var meshes = asset.find_children("*", "MeshInstance3D", true, false)
	if asset is MeshInstance3D:
		meshes.push_front(asset)
	var minimum = Vector3(INF, INF, INF)
	var maximum = Vector3(-INF, -INF, -INF)
	var terracotta = false
	var albedo = []
	for instance in meshes:
		var bounds = instance.mesh.get_aabb()
		for corner in range(8):
			var point = instance.global_transform * bounds.get_endpoint(corner)
			minimum = minimum.min(point)
			maximum = maximum.max(point)
		var material = instance.get_active_material(0)
		if material is StandardMaterial3D:
			var color = material.albedo_color
			albedo = [color.r, color.g, color.b]
			var linear = color.srgb_to_linear()
			terracotta = abs(linear.r - 0.8) < 0.001 and abs(linear.g - 0.22) < 0.001 and abs(linear.b - 0.08) < 0.001
	var size = maximum - minimum
	var passed = meshes.size() == 1 and abs(minimum.y) < 0.001 and size.x > 0 and size.y > 0 and size.z > 0 and terracotta
	var report = {"passed": passed, "godot": Engine.get_version_info().string,
		"mesh_count": meshes.size(), "size": [size.x, size.y, size.z],
		"bottom_y": minimum.y, "terracotta": terracotta, "albedo": albedo,
		"asset_position": [asset.position.x, asset.position.y, asset.position.z],
		"collision": "not supplied; rendering a mesh does not create collision"}
	print("ASSET_CHECK " + JSON.stringify(report))
	preview.queue_free()
	quit(0 if passed else 1)
