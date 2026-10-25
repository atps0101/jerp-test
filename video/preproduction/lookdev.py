"""Optional Blender/Cycles material study; not the marketing film render."""
import bpy,math,os
from mathutils import Vector
R=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=False;s.cycles.max_bounces=8
s.render.resolution_x=1100;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.filepath=R+'/boards/orb-lookdev.png'
s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.18,.18,.2,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
s.view_settings.view_transform='AgX'
def material(name,color,metal=0,rough=.2,trans=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough;n.inputs['Transmission Weight'].default_value=trans;n.inputs['IOR'].default_value=1.45;return m
chrome=material('JERP studio silver',(.72,.74,.77),1,.18)
glass=material('JERP clear glass',(.8,.85,.95),0,.08,1)
blue=material('Primary token enamel',(.003,.23,1),.5,.2)
bpy.ops.mesh.primitive_uv_sphere_add(segments=96,ring_count=64,radius=1.35,location=(0,0,.3));o=bpy.context.object;o.data.materials.append(chrome);bpy.ops.object.shade_smooth()
# The thin curved evidence path is an original motion motif, not a site asset.
cu=bpy.data.curves.new('Evidence path','CURVE');cu.dimensions='3D';cu.resolution_u=32;cu.bevel_depth=.012;cu.bevel_resolution=4
sp=cu.splines.new('POLY');pts=[]
for i in range(150):
 t=i/149*math.pi*1.65;pts.append((1.8*math.cos(t),.35+1.0*math.sin(t),.3+.65*math.sin(t)))
sp.points.add(len(pts)-1)
for p,v in zip(sp.points,pts):p.co=(*v,1)
o=bpy.data.objects.new('A traceable source',cu);s.collection.objects.link(o);cu.materials.append(blue)
for i,(x,z) in enumerate([(-1.7,-.55),(1.55,.95)]):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(x,.2,z));o=bpy.context.object;o.scale=(.6,.05,.38);o.rotation_euler=(.08,.1,-.12 if i else .12);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(glass);b=o.modifiers.new('Rounded glass','BEVEL');b.width=.09;b.segments=6;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
def light(name,pos,power,size,scale=(1,1,1)):
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='RECTANGLE';o.data.size=size;o.data.size_y=size*.35;o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
light('Large white softbox',(-3,-4,5),800,5);light('Silver rim',(3,1,3),1000,4);light('Lower strip',(-1,-3,-3),500,3)
bpy.ops.object.camera_add(location=(0,-8,3));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.3))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7;s.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=R+'/boards/lookdev.blend');bpy.ops.render.render(write_still=True)
