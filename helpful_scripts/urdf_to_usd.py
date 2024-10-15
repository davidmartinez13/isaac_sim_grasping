#External Libraries
import numpy as np
from tqdm import tqdm
import os
import argparse
import sys
import time

def make_parser():
    """ Input Parser """
    # Get the current user's home directory
    user_home = os.path.expanduser("~")

    parser = argparse.ArgumentParser(description='Standalone script for grasp filtering.')

    # Set the defaults as per the provided command-line arguments
    parser.add_argument('--headless', type=bool, help='Running Program in headless mode',
                        default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--force_reset', type=bool, help='Force Reset of Isaac Sim',
                        default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--json_dir', type=str, help='Directory of Grasp Information',
                        default=os.path.join(user_home, 'Documents/Dataset/hithand_transfered'))
    parser.add_argument('--gripper_dir', type=str, help='Directory of Gripper urdf/usd',
                        default=os.path.join(user_home, 'isaac_sim_grasping/grippers'))
    parser.add_argument('--objects_dir', type=str, help='Directory of Object usd',
                        default=os.path.join(user_home, 'Documents/Dataset/objects_usd/google_objects_usd'))
    parser.add_argument('--output_dir', type=str, help='Output directory for filtered grasps',
                        default=os.path.join(user_home, 'Documents/Dataset/graspit_grasps/hithand'))
    parser.add_argument('--num_w', type=int, help='Number of Workstations used in the simulation', default=10)
    parser.add_argument('--device', type=int, help='Gpu to use', default=0)
    parser.add_argument('--test_time', type=int, help='Total time for each grasp test', default=3)
    parser.add_argument('--print_results', type=bool, help='Enable printing of grasp statistics after filtering a document',
                         default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument('--controller', type=str,
                        help='Gripper Controller to use while testing, should match the controller dictionary in the Manager Class',
                        default='position')
    parser.add_argument('--/log/level', type=str, help='Isaac Sim logging arguments', default='error', required=False)
    parser.add_argument('--/log/fileLogLevel', type=str, help='Isaac Sim logging arguments', default='error', required=False)
    parser.add_argument('--/log/outputStreamLevel', type=str, help='Isaac Sim logging arguments', default='error', required=False)
    
    return parser
#Parser
parser = make_parser()
args = parser.parse_args()
head = args.headless
force_reset = args.force_reset
print(args.controller)

from omni.isaac.kit import SimulationApp
config= {
    "headless": head,
    'max_bounces':0,
    'fast_shutdown': True,
    'max_specular_transmission_bounces':0,
    'physics_gpu': args.device,
    'active_gpu': args.device
    }
simulation_app = SimulationApp(config) # we can also run as headless.
import omni.kit.commands
from omni.importer.urdf import _urdf
from pxr import Usd, Sdf
 # Set the settings in the import config
import_config = _urdf.ImportConfig()
import_config.merge_fixed_joints = False
import_config.convex_decomp = False
import_config.fix_base = False
import_config.make_default_prim = True
import_config.self_collision = False
import_config.make_instanceable = True
import_config.create_physics_scene = True
import_config.import_inertia_tensor = False
import_config.default_drive_strength = 10000.0
import_config.default_position_drive_damping = 1000.0
import_config.default_drive_type = _urdf.UrdfJointTargetType.JOINT_DRIVE_POSITION
import_config.distance_scale = 1
import_config.density = 0.0
# dataset_name = "bigbird"
# dataset_name = "kit"
dataset_name = "ycb"

if dataset_name == "ycb":
    is_add_material = True # for kit,ycb
    material_png = "texture_map.png" #for ycb
    material_prim_name = "material_material_0" #for ycb

elif dataset_name == "kit":
    is_add_material = True # for kit,ycb
    material_png = "material0.png" #for kit
    material_prim_name = "material_material0" #for kit

elif dataset_name == "bigbird":
    is_add_material = False # for bigbird since it adds it directly

# Set the base directory where the objects are located
base_dir = "/home/dm/panda_ws/gazebo-objects/objects_gazebo/" + dataset_name

for object_name in os.listdir(base_dir):
    object_dir = os.path.join(base_dir, object_name)
    if os.path.isdir(object_dir):
        urdf_file = os.path.join(object_dir, "{}.urdf".format(object_name))
        usd_file = os.path.join(object_dir, "{}.usd".format(object_name, object_name))
        # usd_file = os.path.join(object_dir, "{}.usda".format(object_name, object_name))

        if os.path.isfile(urdf_file):
            print("Processing {}".format(object_name))
            
            # Convert URDF to USDA
            result, prim_path = omni.kit.commands.execute(
                'URDFParseAndImportFile',
                urdf_path=urdf_file,
                import_config=import_config,
                dest_path=usd_file
            )

            # Modify the USDA file to add texture material0.png
            if os.path.isfile(usd_file) and is_add_material:
                print("Modifying USDA {}".format(usd_file))

                # Load the USDA stage
                if import_config.make_instanceable == True:
                    usd_file = os.path.join(object_dir, "instanceable_meshes.usd")
                    stage = Usd.Stage.Open(usd_file)
                else:
                    stage = Usd.Stage.Open(usd_file)

                # Iterate over the prims in the stage
                for prim in stage.Traverse():
                    if prim.GetName() == material_prim_name or prim.GetName() == "material_DefaultMaterial":
                        shader_prim = stage.GetPrimAtPath(prim.GetPath().AppendPath("Shader"))
                        shader_attrs = shader_prim.GetAttributes()

                        # Check if the diffuse color is present, and if so, add the texture
                        if shader_prim.HasAttribute("inputs:diffuse_color_constant"):
                            # Create or modify the diffuse_texture attribute
                            diffuse_texture_attr = shader_prim.CreateAttribute("inputs:diffuse_texture", Sdf.ValueTypeNames.Asset)
                            material_path = os.path.join(object_dir, material_png)
                            if os.path.isfile(material_path):
                                diffuse_texture_attr.Set(material_path)
                            else:
                                material_path = os.path.join(object_dir, "textured.png")
                                diffuse_texture_attr.Set(material_path)
                            print("Added diffuse texture to {}".format(prim.GetPath()))

                # Save the modified USDA
                stage.GetRootLayer().Save()
                print("Texture added to USDA {}".format(usd_file))

            else:
                print("USDA file not found for {}".format(object_name))
            
# omni.kit.commands.execute('URDFParseAndImportFile',
# 	urdf_path='/home/dm/panda_ws/gazebo-objects/objects_gazebo/kit/BakingVanilla/BakingVanilla.urdf',
# 	import_config=import_config,
# 	# import_config=<omni.importer.urdf._urdf.ImportConfig object at 0x792faa788170>,
# 	dest_path='/home/dm/panda_ws/gazebo-objects/objects_gazebo/kit/BakingVanilla/BakingVanilla/BakingVanilla.usd')

# omni.kit.commands.execute('URDFParseFile',
# 	urdf_path='/home/dm/panda_ws/gazebo-objects/objects_gazebo/kit/BakingVanilla/BakingVanilla.urdf',
# 	import_config=import_config)
	# import_config=<omni.importer.urdf._urdf.ImportConfig object at 0x792faa788170>)

# omni.kit.commands.execute('SelectPrims',
# 	old_selected_paths=[],
# 	new_selected_paths=['/World/BakingVanilla'],
# 	expand_in_stage=True)
# omni.kit.commands.execute('DeletePrims',
# 	paths=[Sdf.Path('/World/BakingVanilla')],
# 	destructive=False)

# import omni.kit.commands
# from pxr import Usd, Sdf

# omni.kit.commands.execute('SetLightingMenuModeCommand',
# 	lighting_mode='Default',
# 	usd_context_name='')

# omni.kit.commands.execute('SelectPrims',
# 	old_selected_paths=[],
# 	new_selected_paths=['/BakingVanilla'],
# 	expand_in_stage=True)

# omni.kit.commands.execute('SelectPrims',
# 	old_selected_paths=['/BakingVanilla'],
# 	new_selected_paths=['/BakingVanilla/Looks'],
# 	expand_in_stage=True)

# omni.kit.commands.execute('SelectPrims',
# 	old_selected_paths=['/BakingVanilla/Looks'],
# 	new_selected_paths=['/BakingVanilla/Looks/material_material0/Shader'],
# 	expand_in_stage=True)

# omni.kit.commands.execute('Group')

# omni.kit.commands.execute('ChangeProperty',
# 	prop_path=Sdf.Path('/BakingVanilla/Looks/material_material0/Shader.inputs:diffuse_texture'),
# 	value=Sdf.AssetPath('../material0.png', '/home/dm/panda_ws/gazebo-objects/objects_gazebo/kit/BakingVanilla/material0.png'),
# 	prev=None,
# 	target_layer=Sdf.Find('/home/dm/panda_ws/gazebo-objects/objects_gazebo/kit/BakingVanilla/BakingVanilla/BakingVanilla.usd'),
# 	usd_context_name=Usd.Stage.Open(rootLayer=Sdf.Find('/home/dm/panda_ws/gazebo-objects/objects_gazebo/kit/BakingVanilla/BakingVanilla/BakingVanilla.usd'), sessionLayer=Sdf.Find('anon:0x792c9401ead0'), pathResolverContext=<invalid repr>))
