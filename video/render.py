"""Original 3D motion study. Run: blender -b -t 4 --python video/render.py"""
import bpy, math, os
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=960; s.render.resolution_y=540; s.render.resolution_percentage=100
s.render.fps=24; s.frame_start=1; s.frame_end=144
s.render.image_settings.file_format='PNG'; s.render.filepath=ROOT+'/output/frame_'
s.world.color=(0.008,0.012,0.025)
sh=s.display.shading
sh.light='STUDIO'; sh.studiolight_rotate_z=0.4; sh.color_type='MATERIAL'; sh.show_shadows=True
sh.show_cavity=True; sh.cavity_type='BOTH'; sh.background_type='WORLD'; sh.show_specular_highlight=True
s.view_settings.view_transform='Standard'
def mat(name,color):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); return m
blue=mat('Electric azure',(0.06,0.32,0.95)); mint=mat('Signal mint',(0.18,0.95,0.7)); white=mat('Porcelain',(0.9,0.94,1)); dark=mat('Ink',(0.025,0.04,0.085))
def anim(o,prop,values):
 for f,v in values:
  setattr(o,prop,v); o.keyframe_insert(data_path=prop,frame=f)
 if o.animation_data:
  for curve in o.animation_data.action.fcurves:
   for p in curve.keyframe_points: p.interpolation='BEZIER'
def text(body,loc,size,material):
 c=bpy.data.curves.new(body,'FONT'); c.body=body; c.align_x='CENTER'; c.size=size; c.extrude=.007; c.bevel_depth=.003
 o=bpy.data.objects.new(body,c); s.collection.objects.link(o); o.location=loc; o.rotation_euler=(math.pi/2,0,0); c.materials.append(material); return o
bpy.ops.object.camera_add(location=(0,-19,8))
cam=bpy.context.object; cam.rotation_euler=(Vector((0,0,0.4))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=15; s.camera=cam
# Central sculptural hub and orbiting components, all actual 3D geometry.
bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=1.05,location=(0,0,.55))
hub=bpy.context.object; hub.data.materials.append(blue); bpy.ops.object.shade_smooth()
anim(hub,'scale',[(1,(.01,)*3),(30,(1.05,)*3),(45,(1,)*3),(110,(1,)*3),(144,(.85,)*3)])
for i in range(3):
 bpy.ops.mesh.primitive_torus_add(major_segments=96,minor_segments=12,location=(0,0,.55),major_radius=1.6+i*.34,minor_radius=.025)
 o=bpy.context.object; o.data.materials.append([mint,blue,white][i]); o.rotation_euler=(.6+i*.6,.3+i*.4,0)
 anim(o,'rotation_euler',[(1,(.6+i*.6,.3+i*.4,0)),(144,(.6+i*.6,.3+i*.4,math.pi*1.4))])
for i in range(12):
 a=i*math.tau/12
 bpy.ops.object.empty_add(); pivot=bpy.context.object
 anim(pivot,'rotation_euler',[(1,(0,0,a)),(144,(0,0,a+math.pi*.65))])
 bpy.ops.mesh.primitive_cube_add(size=.38,location=(3.1+(i%3)*.15,0,.55+math.sin(a)*.5))
 o=bpy.context.object; o.parent=pivot; o.data.materials.append(mint if i%3==0 else blue)
 be=o.modifiers.new('Soft precision edges','BEVEL'); be.width=.09; be.segments=4; o.modifiers.new('Normals','WEIGHTED_NORMAL')
 anim(o,'scale',[(1,(.001,)*3),(24+i*2,(1,)*3),(110,(1,)*3),(144,(.5,)*3)])
logo=text('JERP',(0,-.5,3.35),1.05,white)
anim(logo,'location',[(1,(0,-.5,4.5)),(32,(0,-.5,3.35)),(144,(0,-.5,3.35))])
text('M C P',(0,-.9,-1.9),.28,mint)
cta=text('getjerp.com',(0,-1.2,-2.75),.35,white)
anim(cta,'scale',[(1,(.001,)*3),(83,(.001,)*3),(112,(1,)*3),(144,(1,)*3)])
# A camera push produces a continuous spatial transition.
anim(cam.data,'ortho_scale',[(1,18),(55,15),(100,14),(144,13)])
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/output/jerp-motion.blend')
bpy.ops.render.render(animation=True)
