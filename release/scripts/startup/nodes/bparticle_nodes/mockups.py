import bpy
from bpy.props import *
from .. base import SimulationNode
from .. node_builder import NodeBuilder


class ParticleMeshDistanceNode(bpy.types.Node, SimulationNode):
    bl_idname = "fn_ParticleSurfaceDistanceNode"
    bl_label = "Mockup - Particle Surface Distance"

    def declaration(self, builder: NodeBuilder):
        builder.fixed_input("object", "Object", "Object")
        builder.fixed_output("distance", "Distance", "Float")
        builder.fixed_output("is_inside", "Is Inside", "Boolean")


class DerivedAttributeNode(bpy.types.Node, SimulationNode):
    bl_idname = "fn_DerivedAttributeNode"
    bl_label = "Mockup - Derived Attribute"

    predefined_attributes = {
        "Position" : "Vector",
        "Velocity" : "Vector",
        "Color" : "Color",
        "Size" : "Float",
    }

    attribute: EnumProperty(
        name="Attribute",
        items=[(name, name, "") for name in predefined_attributes.keys()] + [("Custom", "Custom", "")],
        update=SimulationNode.sync_tree,
    )

    attribute_type: EnumProperty(
        name="Attribute Type",
        items=[
            ("Vector", "Vector", ""),
            ("Float", "Float", ""),
            ("Color", "Color", ""),
        ],
        update=SimulationNode.sync_tree,
    )

    def declaration(self, builder: NodeBuilder):
        builder.fixed_input("is_active", "Is Active", "Boolean")
        if self.attribute == "Custom":
            builder.fixed_input("name", "Attribute Name", "Text")
            builder.fixed_input("value", "Value", self.attribute_type)
        else:
            builder.fixed_input("value", "Value", self.predefined_attributes[self.attribute])
        builder.influences_output("influence", "Influence")

    def draw(self, layout):
        layout.prop(self, "attribute", text="")
        if self.attribute == "Custom":
            layout.prop(self, "attribute_type", text="")


class SetAgeLimitNode(bpy.types.Node, SimulationNode):
    bl_idname = "fn_SetAgeLimitNode"
    bl_label = "Mockup - Set Age Limit"

    def declaration(self, builder: NodeBuilder):
        builder.fixed_input("lifetime", "Lifetime (seconds)", "Float", default=3)
        builder.fixed_input("variation", "Variation", "Float", default=0)
        builder.execute_output("execute", "Execute")


class AgeLimitReachedNode(bpy.types.Node, SimulationNode):
    bl_idname = "fn_AgeLimitReachedNode"
    bl_label = "Mockup - Age Limit Reached"

    kill: BoolProperty(
        name="Kill",
        default=True,
        description="Kill the particle when its age limit is reached",
    )

    execute__prop: NodeBuilder.ExecuteInputProperty()

    def declaration(self, builder: NodeBuilder):
        builder.execute_input("execute", "Execute", "execute__prop")
        builder.influences_output("event", "Event")

    def draw(self, layout):
        layout.prop(self, "kill")