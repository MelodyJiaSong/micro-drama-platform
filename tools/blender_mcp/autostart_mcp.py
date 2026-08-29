import bpy


def _start() -> None:
    if not bpy.context.preferences.addons.get("blender_mcp"):
        bpy.ops.preferences.addon_enable(module="blender_mcp")
    if not bpy.context.scene.blendermcp_server_running:
        bpy.ops.blendermcp.start_server()
    print(f"[BlenderMCP] server running on port {bpy.context.scene.blendermcp_port}")


bpy.app.timers.register(_start, first_interval=1.0)
