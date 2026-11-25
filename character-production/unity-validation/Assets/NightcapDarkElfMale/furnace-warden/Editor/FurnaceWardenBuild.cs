using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEditor;
using UnityEditor.SceneManagement;
using Object = UnityEngine.Object;

public static class FurnaceWardenBuild
{
    internal const string Root = "Assets/NightcapDarkElfMale/furnace-warden";
    internal const string Model = Root + "/Model/DarkElfMale.fbx";
    internal const string Prefab = Root + "/Prefab/DarkElfMale.prefab";
    internal const string Scene = Root + "/Review/DarkElfMale_Review.unity";
    internal const string Human = "Assets/NightcapHumans/Male_FieldHuman.fbx";
    internal static string Evidence => Path.GetFullPath(Path.Combine(Application.dataPath, "../../output/dark-elf-male/furnace-warden/UnityReview"));
    internal static readonly string[] States = {"Armored - helm on", "Armored - helm off", "Base - underlayers"};
    internal static readonly string[] Maps = {"DarkElf-Skin","DarkElf-Amber","DarkElf-Ivory","Warden-Plate","Warden-Heat"};
    internal static readonly string[] Slots = {"Dark Elf • indigo skin","Dark Elf • copper amber","Dark Elf • brushed ivory","Dark Elf • ash brows","Furnace Warden • banked iron"};
    internal static readonly string[] Surfaces = {"Indigo Skin","Amber Eyes","Swept Ivory","Ash Brows","Banked Iron"};
    internal static void Check(bool ok, string message) { if (!ok) throw new InvalidOperationException(message); }
    internal static T Asset<T>(string path) where T : Object
    {
        var asset = AssetDatabase.LoadAssetAtPath<T>(path);
        Check(asset, "Missing " + path);
        return asset;
    }
    internal static Texture2D Texture(string name) => Asset<Texture2D>(Root+"/Textures/"+name+".png");
    internal static Material Surface(string name) => Asset<Material>(Root+"/Materials/"+name+".mat");
    static Material CreateMaterial(string path, Shader shader)
    {
        Check(shader && shader.isSupported && !ShaderUtil.ShaderHasError(shader), "Unavailable shader for "+path);
        var mat = AssetDatabase.LoadAssetAtPath<Material>(path);
        if (!mat) { mat=new Material(shader); AssetDatabase.CreateAsset(mat,path); }
        mat.shader=shader;
        EditorUtility.SetDirty(mat);
        return mat;
    }
    internal static void ConfigureTextures(bool compressed)
    {
        foreach (string map in Maps)
        {
            var ti=(TextureImporter)AssetImporter.GetAtPath(Root+"/Textures/"+map+".png");
            ti.textureType=TextureImporterType.Default;
            ti.sRGBTexture=map!="Warden-Heat";
            ti.mipmapEnabled=true;ti.streamingMipmaps=false;
            ti.filterMode=FilterMode.Trilinear;ti.wrapMode=TextureWrapMode.Clamp;
            ti.maxTextureSize=map=="DarkElf-Ivory"||map=="DarkElf-Amber"?512:2048;
            ti.textureCompression=compressed?TextureImporterCompression.CompressedHQ:TextureImporterCompression.Uncompressed;
            ti.alphaSource=TextureImporterAlphaSource.None;
            ti.anisoLevel=4;ti.SaveAndReimport();
        }
    }
    static Material[] ConfigureMaterials()
    {
        var result=new Material[Surfaces.Length];
        for(int i=0;i<Surfaces.Length;i++)
        {
            bool plate=i==4;
            var m=CreateMaterial(Root+"/Materials/"+Surfaces[i]+".mat",
                Shader.Find(plate?"Nightcap/Furnace Warden/Painted Heat":"Nightcap/Painted Character"));
            if(i!=3)m.mainTexture=Texture(plate?"Warden-Plate":Maps[i]);
            m.color=i==3?new Color(.349f,.308f,.332f,1):Color.white;
            m.mainTextureOffset=Vector2.zero;m.mainTextureScale=Vector2.one;
            m.SetFloat("_DiffuseWrap",.35f);m.SetFloat("_IndirectGain",1.5f);
            if(plate){m.SetTexture("_HeatMask",Texture("Warden-Heat"));m.SetFloat("_HeatIntensity",.85f);}
            result[i]=m;
        }
        return result;
    }
    static void ConfigureModel(Material[] materials)
    {
        var importer=(ModelImporter)AssetImporter.GetAtPath(Model);
        var example=(ModelImporter)AssetImporter.GetAtPath(Human);
        importer.animationType=ModelImporterAnimationType.Generic;
        importer.avatarSetup=ModelImporterAvatarSetup.NoAvatar;
        importer.importAnimation=false;importer.importBlendShapes=false;
        importer.importLights=false;importer.importCameras=false;importer.addCollider=false;
        importer.isReadable=true;importer.useFileUnits=true;importer.useFileScale=true;importer.globalScale=1;
        importer.importNormals=ModelImporterNormals.Import;importer.importTangents=ModelImporterTangents.None;
        importer.meshCompression=ModelImporterMeshCompression.Off;
        importer.skinWeights=ModelImporterSkinWeights.Custom;importer.maxBonesPerVertex=4;importer.minBoneWeight=0;
        importer.optimizeGameObjects=false;importer.optimizeBones=false;
        importer.materialImportMode=ModelImporterMaterialImportMode.ImportStandard;
        for(int i=0;i<Slots.Length;i++)
            importer.AddRemap(new AssetImporter.SourceAssetIdentifier(typeof(Material),Slots[i]),materials[i]);
        importer.SaveAndReimport();
        var model=Asset<GameObject>(Model);
        var pose=Object.Instantiate(model);pose.name=model.name;
        try
        {
            var bones=pose.GetComponentsInChildren<Transform>(true).ToDictionary(t=>t.name);
            foreach (string side in new[]{"_l","_r"})
            {
                var arm=bones["upperarm"+side];var forearm=bones["lowerarm"+side];var hand=bones["hand"+side];
                var dir=arm.position.x>pose.transform.position.x?Vector3.right:Vector3.left;
                arm.rotation=Quaternion.FromToRotation(forearm.position-arm.position,dir)*arm.rotation;
                forearm.rotation=Quaternion.FromToRotation(hand.position-forearm.position,dir)*forearm.rotation;
                hand.rotation=Quaternion.FromToRotation(bones["middle_01"+side].position-hand.position,dir)*hand.rotation;
            }
            var definition=example.humanDescription;
            definition.skeleton=bones.Values.Select(t=>new SkeletonBone{name=t.name,position=t.localPosition,rotation=t.localRotation,scale=t.localScale}).ToArray();
            importer.animationType=ModelImporterAnimationType.Human;
            importer.avatarSetup=ModelImporterAvatarSetup.CreateFromThisModel;
            importer.humanDescription=definition;
            importer.SaveAndReimport();
        }
        finally {Object.DestroyImmediate(pose);}
    }
    internal static bool Visible(string name, int state)
    {
        switch(name)
        {
            case "DarkElf_HeadAndNeck":case "DarkElf_AmberEyes":case "DarkElf_Brows":case "Warden_QuiltedJackAndHose":return true;
            case "DarkElf_SweptIvory":return state!=0;
            case "DarkElf_CoveredBody":return state==2;
            case "Warden_ForgeHood":case "Warden_Visor_Grille":case "Warden_TempleAndNape":case "Warden_NeckGuard":return state==0;
            default:return state!=2;
        }
    }
    internal static Vector3[] Vertices(SkinnedMeshRenderer skin)
    {
        var baked = new Mesh();
        try {skin.BakeMesh(baked);return baked.vertices.Select(skin.transform.TransformPoint).ToArray();}
        finally {Object.DestroyImmediate(baked);}
    }
    internal static Bounds BoundsOf(IEnumerable<Vector3> points)
    {
        using(var iter=points.GetEnumerator())
        {
            Check(iter.MoveNext(),"Empty mesh");var bounds=new Bounds(iter.Current,Vector3.zero);
            while(iter.MoveNext())bounds.Encapsulate(iter.Current);
            return bounds;
        }
    }
    static void BuildPrefab()
    {
        var actor=(GameObject)PrefabUtility.InstantiatePrefab(Asset<GameObject>(Model));
        try
        {
            var animator=actor.GetComponent<Animator>();
            Check(animator && animator.avatar && animator.avatar.isHuman && animator.avatar.isValid,"Invalid Humanoid Avatar");
            animator.runtimeAnimatorController=null;animator.applyRootMotion=false;animator.enabled=false;
            var skins=actor.GetComponentsInChildren<SkinnedMeshRenderer>(true);
            Check(skins.Length==38,"Expected 38 skinned renderers, got "+skins.Length);
            foreach(var skin in skins)
            {
                Check(skin.sharedMaterials.Length==1 && skin.sharedMaterial && Surfaces.Contains(skin.sharedMaterial.name),
                    "Unresolved FBX slot "+skin.name+" / "+string.Join(", ",skin.sharedMaterials.Select(m=>m?m.name:"(null)")));
                // A skinned local bound is in the renderer's current bounds coordinate space.
                // Derive it from the current world-to-local transform of the renderer root.
                var space=skin.rootBone?skin.rootBone:skin.transform;
                var bounds=BoundsOf(Vertices(skin).Select(space.InverseTransformPoint));bounds.Expand(.012f/Mathf.Max(.0001f,space.lossyScale.x));
                skin.localBounds=bounds;skin.quality=SkinQuality.Bone4;skin.updateWhenOffscreen=false;
                skin.enabled=Visible(skin.name,0);
                PrefabUtility.RecordPrefabInstancePropertyModifications(skin);
            }
            PrefabUtility.RecordPrefabInstancePropertyModifications(animator);
            PrefabUtility.SaveAsPrefabAsset(actor,Prefab,out bool ok);Check(ok,"Unable to save prefab");
        }
        finally {Object.DestroyImmediate(actor);}
    }
    internal static void SetLight(Light key, int preset)
    {
        RenderSettings.ambientMode=AmbientMode.Flat;RenderSettings.fog=false;
        RenderSettings.ambientLight=preset==2?new Color(.28f,.33f,.43f):new Color(.49f,.49f,.52f);
        key.type=LightType.Directional;key.shadows=LightShadows.Soft;key.shadowStrength=.65f;
        key.color=preset==2?new Color(1,.61f,.35f):new Color(1,.96f,.92f);
        key.intensity=preset==2?.85f:1.25f;
        var direction=preset==2?new Vector3(.94f,-.42f,-.36f):new Vector3(preset==1?-.64f:.64f,-.82f,-.82f);
        key.transform.rotation=Quaternion.LookRotation(direction);
    }
    internal static void CameraPose(Camera cam,Vector3 target,Vector3 from,float ortho)
    {
        cam.orthographic=true;cam.orthographicSize=ortho;cam.nearClipPlane=.02f;cam.farClipPlane=50;
        cam.transform.position=target+from.normalized*5;cam.transform.LookAt(target);
    }
    static void BuildScene()
    {
        var scene=EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
        var asset=Asset<GameObject>(Prefab);
        for(int i=0;i<States.Length;i++)
        {
            var actor=(GameObject)PrefabUtility.InstantiatePrefab(asset);
            actor.name=States[i];
            foreach(var skin in actor.GetComponentsInChildren<SkinnedMeshRenderer>(true))
            {
                skin.enabled=Visible(skin.name,i);PrefabUtility.RecordPrefabInstancePropertyModifications(skin);
            }
            actor.SetActive(i==0);PrefabUtility.RecordPrefabInstancePropertyModifications(actor);
        }
        var floor=GameObject.CreatePrimitive(PrimitiveType.Plane);floor.name="Matte floor";
        Object.DestroyImmediate(floor.GetComponent<Collider>());
        floor.transform.localScale=new Vector3(8,1,8);
        var floorMat=CreateMaterial(Root+"/Review/Matte Gray.mat",Shader.Find("Standard"));
        floorMat.color=new Color(.265f,.254f,.28f);floorMat.SetFloat("_Glossiness",0);floorMat.SetFloat("_Metallic",0);
        floor.GetComponent<Renderer>().sharedMaterial=floorMat;
        var light=new GameObject("Key - neutral").AddComponent<Light>();SetLight(light,0);RenderSettings.sun=light;
        var cam=new GameObject("Review Camera").AddComponent<Camera>();cam.tag="MainCamera";
        cam.clearFlags=CameraClearFlags.SolidColor;cam.backgroundColor=new Color(.235f,.225f,.25f);
        cam.allowHDR=false;cam.renderingPath=RenderingPath.Forward;
        CameraPose(cam,new Vector3(0,.925f,.025f),new Vector3(1.55f,.33f,4.5f),1.045f);
        if(SceneView.lastActiveSceneView)
            SceneView.lastActiveSceneView.LookAt(new Vector3(0,.93f,0),cam.transform.rotation,1.23f,true);
        Check(EditorSceneManager.SaveScene(scene,Scene),"Unable to save review scene");
        AssetDatabase.SaveAssets();
    }
    [MenuItem("Nightcap/Furnace Warden/Build static handoff")]
    public static void Run()
    {
        Directory.CreateDirectory(Evidence);
        AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
        ConfigureTextures(false);var materials=ConfigureMaterials();
        ConfigureModel(materials);BuildPrefab();BuildScene();
        Debug.Log("WARDEN_BUILD_COMPLETE");
    }
    internal static void Compress() {ConfigureTextures(true);}
}

