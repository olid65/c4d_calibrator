import c4d
import os,glob
 
ABSOLU = 1101
ALPHA = 1102
PLAN = 1103
OK = 1201
CANCEL = 1202
lst_ext = ['.jpg','.tif','.tga','.png','.psd','.b3d','.gif']

def listdirectory(path): 
    """retourne une liste de tous les dossiers en enfants de path"""
    res=[] 
    
    for root, dirs, files in os.walk(path): 
        for i in dirs: 
            res.append(os.path.join(root, i))
    return res

def is_in_doc_path(fn,doc):
    """retourne vrai si le fichier est au meme endroit que doc 
       ou dans tex ou dans un sous dossier de tex"""
    path_img,name_img = os.path.split(fn)
    path_doc = doc.GetDocumentPath()    
    if not path_doc : 
        return False
    if path_doc==path_img:
        return True
    path_tex = os.path.join(path_doc,'tex')
    if path_tex == path_img:
        return True
    lst_dir =listdirectory(path_tex)
    if path_img in lst_dir:
        return True
    return False

def creer_mat(fn,nom,alpha=False):
    doc = c4d.documents.GetActiveDocument()
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat.SetName(nom)
    shd = c4d.BaseList2D(c4d.Xbitmap)

    #si l'image est dans le chemin des textures
    #on le met en relatif
    if is_in_doc_path(fn,doc):
        fn = os.path.basename(fn) 
        
    shd[c4d.BITMAPSHADER_FILENAME] = fn
    mat[c4d.MATERIAL_COLOR_SHADER] = shd
    mat.InsertShader(shd)
    mat[c4d.MATERIAL_USE_SPECULAR]=False
    mat[c4d.MATERIAL_PREVIEWSIZE]= c4d. MATERIAL_PREVIEWSIZE_NO_SCALE #taille de pr\visualisation
    #c4d.MATERIAL_PREVIEWSIZE_1024
    if alpha :
        mat[c4d.MATERIAL_USE_ALPHA]=True
        shda = c4d.BaseList2D(c4d.Xbitmap)
        shda[c4d.BITMAPSHADER_FILENAME] = fn 
        mat[c4d.MATERIAL_ALPHA_SHADER]=shda
        mat.InsertShader(shda)
        
    mat.Message(c4d.MSG_UPDATE)
    mat.Update(True, True)
    return mat 

def creer_plan_image(fn,nom,mat,tag_display = True):
    doc = c4d.documents.GetActiveDocument()
    bmp = c4d.bitmaps.BaseBitmap()
    if bmp.InitWith(fn)[0]== c4d.IMAGERESULT_OK:
        larg,haut = bmp.GetSize()
        bmp.FlushAll()
        plan = c4d.BaseObject(c4d.Oplane)
        plan.SetName(nom)
        plan[c4d.PRIM_PLANE_WIDTH]=larg
        plan[c4d.PRIM_PLANE_HEIGHT]=haut
        plan[c4d.PRIM_PLANE_SUBW]=1
        plan[c4d.PRIM_PLANE_SUBH]=1
        plan[c4d.PRIM_AXIS]=5
        tag = c4d.TextureTag()
        tag.SetMaterial(mat)
        tag[c4d.TEXTURETAG_PROJECTION]=6
        plan.InsertTag(tag)

        if tag_display:
            tag = c4d.BaseTag(c4d.Tdisplay)
            tag[c4d.DISPLAYTAG_AFFECT_DISPLAYMODE] = True
            tag[c4d.DISPLAYTAG_SDISPLAYMODE] = c4d.DISPLAYTAG_SDISPLAY_FLAT
            plan.InsertTag(tag)

        return plan
    else : return None

def creer_poly_image(fn,nom,mat,tag_display = True):
    bmp = c4d.bitmaps.BaseBitmap()
    if bmp.InitWith(fn)[0]== c4d.IMAGERESULT_OK:
        larg,haut = bmp.GetSize()
        mi_l=larg/2.
        mi_h = haut/2.
        bmp.FlushAll()
        plan = c4d.PolygonObject(4,1)
        plan.SetName(nom)
        plan.SetPoint(0,c4d.Vector(-mi_l,0,-mi_h))
        plan.SetPoint(1,c4d.Vector(-mi_l,0,mi_h))
        plan.SetPoint(2,c4d.Vector(mi_l,0,mi_h))
        plan.SetPoint(3,c4d.Vector(mi_l,0,-mi_h))
        plan.SetPolygon(0,c4d.CPolygon(0,1,2,3))
        
        tag = c4d.TextureTag()
        tag.SetMaterial(mat)
        tag[c4d.TEXTURETAG_PROJECTION]=6
        plan.InsertTag(tag)

        if tag_display:
            tag = c4d.BaseTag(c4d.Tdisplay)
            tag[c4d.DISPLAYTAG_AFFECT_DISPLAYMODE] = True
            tag[c4d.DISPLAYTAG_SDISPLAYMODE] = c4d.DISPLAYTAG_SDISPLAY_FLAT
            plan.InsertTag(tag)
        
        tuvw = c4d.UVWTag(1)
        tuvw.SetSlow(0,c4d.Vector(0,1,0),
                       c4d.Vector(0,0,0),
                       c4d.Vector(1,0,0),
                       c4d.Vector(1,1,0))
        plan.InsertTag(tuvw)
        plan.Message(c4d.MSG_UPDATE)        
        return plan #doc.InsertObject(plan)
    else : return None
 
if __name__=='__main__':
    
    pass