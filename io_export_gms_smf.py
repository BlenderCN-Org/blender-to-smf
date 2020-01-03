import bpy
from struct import pack

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSMF(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_scene.smf"
    bl_label = "Export SMF"

    # ExportHelper mixin class uses this
    filename_ext = ".smf"

    filter_glob = StringProperty(
            default="*.smf",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = BoolProperty(
            name="Example Boolean",
            description="Example Tooltip",
            default=True,
            )

    type = EnumProperty(
            name="Example Enum",
            description="Choose between two items",
            items=(('OPT_A', "First Option", "Description one"),
                   ('OPT_B', "Second Option", "Description two")),
            default='OPT_A',
            )

    def execute(self, context):
        obj = context.object
        
        with open(self.filepath, "wb") as file:
            # Write header text
            file.write("SnidrsModelFormat".encode('utf-8'))
            file.write(bytes(1))    # Null byte
            
            # Write version
            version = 7
            file.write(pack('f', version))
            
            # Write rest of header
            offsets = (0, 0, 0, 0, 0, 0, 0, 0)
            file.write(pack('IIIIIIII', *offsets))
            
            no_models = len(context.selected_objects)
            file.write(pack('B', no_models))
            
            placeholder_bytes = (0, 0)
            file.write(pack('II', *placeholder_bytes))
            
            center, size = obj.location[:], 1
            file.write(pack('ffff', *(*center, size)))
            
            # Write actual data
        
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSMF.bl_idname, text="Export SMF")


def register():
    bpy.utils.register_class(ExportSMF)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportSMF)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_scene.smf('INVOKE_DEFAULT')
