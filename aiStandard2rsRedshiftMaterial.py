'''

aiStandardSurface2rsRedshiftMaterial
by Jorge Sanchez Salcedo, 2020.
www.jorgesanchez-da.com
jorgesanchez.da@gmail.com

Convert from aiStandardSurface to
rsRedshiftMaterial previously selected.

'''

import maya.cmds as cmds

def convert():
    shaders = cmds.ls(sl=True, typ='aiStandardSurface')
    for i in shaders:
        currentName = i.split('SH_')
        newShName = 'rs' + (currentName[-1]).capitalize()
        newSgName = newShName + 'SG'
        newSh = cmds.shadingNode('RedshiftMaterial', n=newShName, asShader=True)
        newSg = cmds.sets(n=newSgName, nss=True, r=True)
        cmds.connectAttr(newSh + '.outColor', newSg + '.surfaceShader', f=True)

        cmds.hyperShade(o=i)
        cmds.hyperShade(a=newSh)

        attribs = { 'base': 'diffuse_weight',
                    'baseColor': 'diffuse_color',
                    'diffuseRoughness': 'diffuse_roughness',
                    'specular': 'refl_weight',
                    'specularColor': 'refl_color',
                    'specularRoughness': 'refl_roughness',
                    'specularAnisotropy': 'refl_aniso',
                    'specularRotation': 'refl_aniso_rotation',
                    'specularIOR': 'refl_ior',
                    'transmission': 'refr_weight',
                    'transmissionColor': 'refr_color',
                    'thinWalled': 'refr_thin_walled',
                    'coat': 'coat_weight',
                    'coatColor': 'coat_color',
                    'coatRoughness': 'coat_roughness',
                    'coatIOR': 'coat_ior',
                    'normalCamera': 'bump_input'
                   }

        for k, v in attribs.iteritems():
            checkConn = cmds.connectionInfo(i + '.' + k, id=True)
            fileConn = cmds.connectionInfo(i + '.' + k, sfd=True)
            if checkConn is True:
                cmds.connectAttr(fileConn, newShName + '.' + v, f=True)
            else:
                try:
                    val = cmds.getAttr(i + '.' + k)
                    cmds.setAttr(newShName + '.' + v, val)
                except RuntimeError:
                    try:
                        colorRGB = ['R','G','B']
                        for color in colorRGB:
                            val = cmds.getAttr(i + '.' + k + color)
                            cmds.setAttr(newShName + '.' + v + color, val)
                    except ValueError:
                        pass

        print(' >>> You have already converted ' + i + ' to ' + newShName + ' succesfully!')
