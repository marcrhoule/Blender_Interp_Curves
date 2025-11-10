bl_info = {
    "name": "Custom Keyframe Interpolation - 140 Functions",
    "author": "Marc Houle",
    "version": (2, 0, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar (N) > Marc's Interps",
    "description": "Apply 140 custom interpolation curves with visual previews",
    "category": "Animation",
}

import bpy
import math
import os
import bpy.utils.previews

# Import functions from external file
from . import interpolation_functions
INTERPOLATION_FUNCTIONS = interpolation_functions.INTERPOLATION_FUNCTIONS
CATEGORIES = interpolation_functions.CATEGORIES

# Preview collection for icons
preview_collections = {}

# Get addon directory for preview images
def get_addon_dir():
    return os.path.dirname(os.path.realpath(__file__))

def load_preview_icons():
    """Load preview icons using Blender's preview system"""
    pcoll = bpy.utils.previews.new()
    
    addon_dir = get_addon_dir()
    preview_dir = os.path.join(addon_dir, "interp_previews")
    
    if os.path.exists(preview_dir):
        for name in INTERPOLATION_FUNCTIONS.keys():
            # Remove the return marker for filename
            safe_name = name.replace(" ↺", "").replace(" ", "_").replace("+", "plus").replace("/", "_")
            img_path = os.path.join(preview_dir, f"{safe_name}.png")
            
            if os.path.exists(img_path):
                pcoll.load(safe_name, img_path, 'IMAGE')
    
    preview_collections["main"] = pcoll

def unload_preview_icons():
    """Unload preview icons"""
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

class ANIM_OT_apply_interpolation(bpy.types.Operator):
    """Apply custom interpolation between selected keyframes"""
    bl_idname = "anim.apply_interpolation"
    bl_label = "Apply Interpolation"
    bl_options = {'REGISTER', 'UNDO'}
    
    interp_name: bpy.props.StringProperty()
    
    samples: bpy.props.IntProperty(
        name="Samples",
        description="Number of keyframes to create between start and end",
        default=20,
        min=2,
        max=200
    )
    
    influence: bpy.props.FloatProperty(
        name="Influence",
        description="Blend between linear (0%) and full effect (100%)",
        default=100.0,
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE'
    )
    
    reverse: bpy.props.BoolProperty(
        name="Reverse",
        description="Flip the interpolation backwards",
        default=False
    )
    
    overshoot: bpy.props.FloatProperty(
        name="Overshoot",
        description="Amplify overshoot/bounce effects (1.0 = normal)",
        default=1.0,
        min=0.0,
        max=3.0
    )
    
    time_scale: bpy.props.FloatProperty(
        name="Time Scale",
        description="Speed up (>1) or slow down (<1) the effect",
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    output_mode: bpy.props.EnumProperty(
        name="Output Mode",
        description="Where to apply the interpolation",
        items=[
            ('KEYFRAMES', "Keyframes", "Apply to selected keyframes in timeline", 'KEYFRAME', 0),
            ('GEO_NODES', "Geometry Nodes", "Create a node group for Geometry Nodes", 'NODETREE', 1),
        ],
        default='KEYFRAMES'
    )
    
    @classmethod
    def poll(cls, context):
        # Always allow if we have an active object (no animation data needed for Geometry Nodes mode)
        return context.active_object is not None
    
    def create_geometry_node_group(self, context):
        """Create a Geometry Nodes node group with the interpolation curve"""
        interp_func = INTERPOLATION_FUNCTIONS[self.interp_name]
        
        # Create node group
        node_group = bpy.data.node_groups.new(f"Interp: {self.interp_name}", 'GeometryNodeTree')
        
        # Create group inputs and outputs
        group_inputs = node_group.nodes.new('NodeGroupInput')
        group_outputs = node_group.nodes.new('NodeGroupOutput')
        
        group_inputs.location = (-400, 0)
        group_outputs.location = (400, 0)
        
        # Add input socket (Blender 4.0+ API)
        input_socket = node_group.interface.new_socket(name="Value", in_out='INPUT', socket_type='NodeSocketFloat')
        input_socket.default_value = 0.0
        input_socket.min_value = 0.0
        input_socket.max_value = 1.0
        
        # Add output socket
        node_group.interface.new_socket(name="Result", in_out='OUTPUT', socket_type='NodeSocketFloat')
        
        # Create Float Curve node
        curve_node = node_group.nodes.new('ShaderNodeFloatCurve')
        curve_node.location = (0, 0)
        
        # Sample the interpolation function and create curve points
        curve = curve_node.mapping.curves[0]
        
        num_points = min(self.samples, 64)
        
        # Blender curves start with 2 default points
        # We'll reuse them and add more if needed
        current_points = len(curve.points)
        
        # Add additional points if we need more than the default 2
        for _ in range(num_points - current_points):
            curve.points.new(0, 0)
        
        # Now set coordinates for each point (only use the first num_points)
        for i in range(min(num_points, len(curve.points))):
            t = i / (num_points - 1)
            
            # Apply time scale
            t_scaled = min(1.0, t * self.time_scale)
            
            # Apply reverse
            if self.reverse:
                t_scaled = 1.0 - t_scaled
            
            try:
                # Get interpolated value
                interp_t = interp_func(t_scaled)
                
                # Apply overshoot multiplier
                if interp_t < 0:
                    interp_t = interp_t * self.overshoot
                elif interp_t > 1:
                    interp_t = 1 + (interp_t - 1) * self.overshoot
                
                # Apply influence
                linear_value = t
                influence_factor = self.influence / 100.0
                value = linear_value * (1 - influence_factor) + interp_t * influence_factor
                
                # Set point location
                curve.points[i].location = (t, value)
                
            except Exception as e:
                # Fallback to linear
                curve.points[i].location = (t, t)
                print(f"Error evaluating interpolation at t={t}: {e}")
        
        # Update the curve mapping
        curve_node.mapping.update()
        
        # Connect nodes
        # Float Curve has two inputs: 0=Factor (for the curve itself), 1=Value
        # We want to connect to Value (index 1) not Factor (index 0)
        node_group.links.new(group_inputs.outputs[0], curve_node.inputs[1])
        node_group.links.new(curve_node.outputs[0], group_outputs.inputs[0])
        
        # Try to add to active geometry nodes modifier
        obj = context.active_object
        geo_mod = None
        
        # Find existing geometry nodes modifier
        for mod in obj.modifiers:
            if mod.type == 'NODES':
                geo_mod = mod
                break
        
        # Create modifier if none exists
        if not geo_mod:
            geo_mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        
        # Create node tree if modifier doesn't have one
        if geo_mod.node_group is None:
            geo_mod.node_group = bpy.data.node_groups.new(name="Geometry Nodes", type='GeometryNodeTree')
            # Add basic input/output nodes
            input_node = geo_mod.node_group.nodes.new('NodeGroupInput')
            output_node = geo_mod.node_group.nodes.new('NodeGroupOutput')
            input_node.location = (-200, 0)
            output_node.location = (200, 0)
            
            # Add geometry socket to the tree
            geo_mod.node_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
            geo_mod.node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
            
            # Connect input to output
            geo_mod.node_group.links.new(input_node.outputs[0], output_node.inputs[0])
        
        # Add the interpolation node group to the modifier's node tree
        if geo_mod.node_group:
            interp_node = geo_mod.node_group.nodes.new('GeometryNodeGroup')
            interp_node.node_tree = node_group
            interp_node.label = f"{self.interp_name}"
            interp_node.location = (0, -200)
        
        return node_group
    
    def apply_to_keyframes(self, context):
        """Apply interpolation to selected keyframes"""
        obj = context.active_object
        
        # Only check for animation data in keyframes mode
        if not obj or not obj.animation_data or not obj.animation_data.action:
            self.report({'WARNING'}, "No animation data found. Select object with keyframes or use Geometry Nodes mode.")
            return {'CANCELLED'}
        
        action = obj.animation_data.action
        interp_func = INTERPOLATION_FUNCTIONS[self.interp_name]
        
        # Check if this is a return-to-start function (marked with ↺)
        is_return_to_start = " ↺" in self.interp_name
        
        modified_count = 0
        
        # Process each fcurve
        for fcurve in action.fcurves:
            # Get selected keyframes
            selected_points = [kp for kp in fcurve.keyframe_points if kp.select_control_point]
            
            if len(selected_points) < 2:
                continue
            
            # Sort by frame
            selected_points.sort(key=lambda kp: kp.co[0])
            
            # First, set all selected keyframes to LINEAR with Vector handles to prevent any interpolation issues
            for kp in selected_points:
                kp.interpolation = 'LINEAR'
                kp.handle_left_type = 'VECTOR'
                kp.handle_right_type = 'VECTOR'
            
            # Process pairs of consecutive selected keyframes
            for i in range(len(selected_points) - 1):
                start_kf = selected_points[i]
                end_kf = selected_points[i + 1]
                
                start_frame = start_kf.co[0]
                end_frame = end_kf.co[0]
                start_value = start_kf.co[1]
                end_value = end_kf.co[1]
                
                # Skip if frames are the same
                if start_frame >= end_frame:
                    continue
                
                # For return-to-start functions, use start_value as the target end value
                target_end_value = start_value if is_return_to_start else end_value
                
                # Remove existing keyframes between start and end (except endpoints)
                points_to_remove = [kp for kp in fcurve.keyframe_points 
                                   if start_frame < kp.co[0] < end_frame]
                for kp in points_to_remove:
                    fcurve.keyframe_points.remove(kp)
                
                # Insert new keyframes with custom interpolation
                # Note: range goes from 1 to samples-1, so we don't duplicate the endpoints
                for j in range(1, self.samples):
                    t = j / self.samples
                    frame = start_frame + t * (end_frame - start_frame)
                    
                    # Apply time scale
                    t_scaled = min(1.0, t * self.time_scale)
                    
                    # Apply reverse
                    if self.reverse:
                        t_scaled = 1.0 - t_scaled
                    
                    try:
                        # Get interpolated value
                        interp_t = interp_func(t_scaled)
                        
                        # Apply overshoot multiplier
                        if interp_t < 0:
                            interp_t = interp_t * self.overshoot
                        elif interp_t > 1:
                            interp_t = 1 + (interp_t - 1) * self.overshoot
                        
                        # Calculate final value using target_end_value
                        interp_value = start_value + interp_t * (target_end_value - start_value)
                        
                        # Apply influence
                        linear_value = start_value + t * (target_end_value - start_value)
                        influence_factor = self.influence / 100.0
                        value = linear_value * (1 - influence_factor) + interp_value * influence_factor
                        
                        fcurve.keyframe_points.insert(frame, value)
                    except Exception as e:
                        # Fallback to linear interpolation
                        value = start_value + t * (target_end_value - start_value)
                        fcurve.keyframe_points.insert(frame, value)
                        print(f"Error applying interpolation at frame {frame}: {e}")
                
                # If this is a return-to-start function, move the end keyframe to start value
                if is_return_to_start:
                    end_kf.co = (end_frame, start_value)
                
                modified_count += 1
            
            # Now set ALL keyframes in the fcurve to linear with vector handles
            # This must happen AFTER all insertions to ensure clean linear interpolation
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'LINEAR'
                kp.handle_left_type = 'VECTOR'
                kp.handle_right_type = 'VECTOR'
        
        # Update the view
        for area in context.screen.areas:
            if area.type in ('GRAPH_EDITOR', 'DOPESHEET_EDITOR'):
                area.tag_redraw()
        
        if modified_count > 0:
            if is_return_to_start:
                self.report({'INFO'}, f"Applied {self.interp_name} to {modified_count} curve segment(s) - Returns to start")
            else:
                self.report({'INFO'}, f"Applied {self.interp_name} to {modified_count} curve segment(s)")
        else:
            self.report({'WARNING'}, "No valid keyframe pairs selected")
        
        return {'FINISHED'}
    
    def execute(self, context):
        if self.output_mode == 'GEO_NODES':
            try:
                node_group = self.create_geometry_node_group(context)
                self.report({'INFO'}, f"Created Geometry Nodes group: {node_group.name}")
                return {'FINISHED'}
            except Exception as e:
                self.report({'ERROR'}, f"Failed to create Geometry Nodes group: {str(e)}")
                return {'CANCELLED'}
        else:
            return self.apply_to_keyframes(context)
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        
        # Show large preview image (remove ↺ for filename lookup)
        safe_name = self.interp_name.replace(" ↺", "").replace(" ", "_").replace("+", "plus").replace("/", "_")
        pcoll = preview_collections.get("main")
        if pcoll and safe_name in pcoll:
            icon = pcoll[safe_name]
            layout.template_icon(icon_value=icon.icon_id, scale=10.0)
        
        layout.label(text=self.interp_name, icon='FCURVE')
        layout.separator()
        
        # Output mode selection
        box = layout.box()
        box.label(text="Output Mode:", icon='EXPORT')
        box.prop(self, "output_mode", expand=True)
        
        layout.separator()
        
        # Main parameters
        col = layout.column(align=True)
        col.prop(self, "samples")
        col.prop(self, "influence")
        
        layout.separator()
        
        # Advanced parameters
        box = layout.box()
        box.label(text="Advanced", icon='PREFERENCES')
        col = box.column(align=True)
        col.prop(self, "reverse")
        col.prop(self, "overshoot")
        col.prop(self, "time_scale")

class VIEW3D_PT_custom_interpolation(bpy.types.Panel):
    """Main panel in 3D Viewport sidebar"""
    bl_label = "Custom Interpolation"
    bl_idname = "VIEW3D_PT_custom_interpolation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Marc's Interps"
    
    def draw(self, context):
        layout = self.layout
        
        # Check if we have valid selection
        obj = context.active_object
        if not obj:
            layout.label(text="No active object", icon='INFO')
            return
        
        # Show animation status (but don't require it)
        box = layout.box()
        if not obj.animation_data or not obj.animation_data.action:
            box.label(text="No animation data", icon='INFO')
            box.label(text="Functions work in Geo Nodes mode")
        else:
            # Count selected keyframes
            selected_count = 0
            for fcurve in obj.animation_data.action.fcurves:
                selected_count += len([kp for kp in fcurve.keyframe_points if kp.select_control_point])
            
            if selected_count < 2:
                box.label(text="Select 2+ keyframes", icon='INFO')
                box.label(text="(in Graph Editor or Timeline)")
                box.label(text="Or use Geo Nodes mode")
            else:
                box.label(text=f"{selected_count} keyframes selected", icon='KEYFRAME_HLT')
        
        layout.separator()
        
        # Get preview collection
        pcoll = preview_collections.get("main")
        
        # Category colors for visual distinction
        category_colors = {
            "SMOOTH & CLASSIC": 'COLORSET_01_VEC',
            "ELASTIC & SPRINGY": 'COLORSET_03_VEC',
            "BOUNCY & OVERSHOOT": 'COLORSET_02_VEC',
            "EXPONENTIAL & POWER": 'COLORSET_06_VEC',
            "RHYTHMIC & WAVES": 'COLORSET_04_VEC',
            "ORGANIC & NATURAL": 'COLORSET_14_VEC',
            "GLITCHY & DIGITAL": 'COLORSET_09_VEC',
            "EXTREME & WILD": 'COLORSET_01_VEC',
            "MECHANICAL & ROBOTIC": 'COLORSET_15_VEC',
            "COMPLEX STORIES": 'COLORSET_08_VEC',
        }
        
        # Display all interpolations organized by category with color coding
        for category_name, function_list in CATEGORIES.items():
            # Category header with colored icon
            box = layout.box()
            row = box.row()
            
            # Use a colored icon for the category
            color_icon = category_colors.get(category_name, 'DOT')
            row.label(text=category_name, icon=color_icon)
            
            # Display functions in this category
            for name in function_list:
                if name in INTERPOLATION_FUNCTIONS:
                    # Remove ↺ for filename lookup but keep in display
                    safe_name = name.replace(" ↺", "").replace(" ", "_").replace("+", "plus").replace("/", "_")
                    
                    # Get the icon if available
                    if pcoll and safe_name in pcoll:
                        icon = pcoll[safe_name].icon_id
                    else:
                        icon = 0
                    
                    # Create operator button with icon (name includes ↺ symbol)
                    op = box.operator(ANIM_OT_apply_interpolation.bl_idname, text=name, icon_value=icon)
                    op.interp_name = name
            
            layout.separator()

def register():
    bpy.utils.register_class(ANIM_OT_apply_interpolation)
    bpy.utils.register_class(VIEW3D_PT_custom_interpolation)
    
    # Load preview icons
    load_preview_icons()

def unregister():
    # Unload preview icons
    unload_preview_icons()
    
    bpy.utils.unregister_class(VIEW3D_PT_custom_interpolation)
    bpy.utils.unregister_class(ANIM_OT_apply_interpolation)

if __name__ == "__main__":
    register()
