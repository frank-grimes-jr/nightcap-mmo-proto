using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEditor;
using UnityEditor.SceneManagement;
using Object = UnityEngine.Object;

public static class EbbCantorBuild
{
    internal const string Root = "Assets/NightcapDarkElfFemale/ebb-cantor";
    internal const string Model = Root + "/Model/DarkElfFemale.fbx";
    internal const string Prefab = Root + "/Prefab/DarkElfFemale.prefab";
    internal const string Scene = Root + "/Review/DarkElfFemale_RobeReview.unity";
    internal const string Human = "Assets/NightcapHumans/Female_FieldHuman.fbx";
    internal static string Evidence => Environment.GetEnvironmentVariable("NIGHTCAP_CANTOR_EVIDENCE") ?? Path.GetFullPath(Path.Combine(Application.dataPath, "../../output/dark-elf-female/ebb-cantor/UnityReview"));
    internal static readonly string[] States = {"Ebb Cantor"};
    internal static readonly string[] Maps = new string[] { "Auricle", "Copper-Iris", "Ebb-Pall", "Ebb-Procession", "Ebb-Stoneware", "Indigo-Skin", "Ivory-Locks" };
    // Slot order matches the native FBX submeshes, including turned cloth and vessel interiors.
    internal static readonly Dictionary<string,string[]> MeshSlots = new Dictionary<string,string[]>
    {
        { "Eyes | Copper pair", new string[] { "Copper iris" } },
        { "Face | Ash brows", new string[] { "Ash brows" } },
        { "Skin | Head neck and hands", new string[] { "Indigo skin" } },
        { "Face | Modelled pinna l", new string[] { "Auricle paint" } },
        { "Face | Modelled pinna r", new string[] { "Auricle paint" } },
        { "Hair | Swept ivory bob", new string[] { "Combed ivory" } },
        { "Hair | Swept forelock 1", new string[] { "Combed ivory" } },
        { "Hair | Swept forelock 2", new string[] { "Combed ivory" } },
        { "Hair | Swept forelock 3", new string[] { "Combed ivory" } },
        { "Hair | Swept forelock 4", new string[] { "Combed ivory" } },
        { "Hair | Braid strand 1", new string[] { "Combed ivory" } },
        { "Hair | Braid strand 2", new string[] { "Combed ivory" } },
        { "Hair | Braid strand 3", new string[] { "Combed ivory" } },
        { "Hair | Bound ferrule 1", new string[] { "Worn brass" } },
        { "Hair | Bound ferrule 2", new string[] { "Worn brass" } },
        { "Underlayer | River leather boots", new string[] { "Wool and resist print" } },
        { "Underlayer | Fitted linen shift", new string[] { "Wool and resist print" } },
        { "Habit | West breadth", new string[] { "Wool and resist print", "Pitch-soaked reed" } },
        { "Habit | Funeral road front", new string[] { "Wool and resist print", "Pitch-soaked reed" } },
        { "Habit | East breadth", new string[] { "Wool and resist print", "Pitch-soaked reed" } },
        { "Habit | Joined back", new string[] { "Wool and resist print", "Pitch-soaked reed" } },
        { "Habit | Cut sleeve l", new string[] { "Wool and resist print", "Pitch-soaked reed", "Flax cord", "Madder binding" } },
        { "Habit | Cut sleeve r", new string[] { "Wool and resist print", "Pitch-soaked reed", "Flax cord", "Madder binding" } },
        { "Habit | Madder sounding chart", new string[] { "Pall and dike chart", "Madder binding", "Flax cord", "Pitch-soaked reed" } },
        { "Pall | Seventeen gathered folds", new string[] { "Pall and dike chart", "Flax cord", "Madder binding", "Pitch-soaked reed" } },
        { "Pall | Pierced reed shuttle", new string[] { "Pitch-soaked reed", "Rubbed copper", "Madder binding" } },
        { "Binding | Reed band and ferry knot", new string[] { "Wool and resist print", "Pitch-soaked reed", "Flax cord", "Madder binding" } },
        { "Voices | Open throat", new string[] { "Smoke fired clay", "Cut slip and firing clouds", "Chalk slip", "Pitch-soaked reed" } },
        { "Voices | Wax-stopped throat", new string[] { "Smoke fired clay", "Cut slip and firing clouds", "Chalk slip", "Pitch-soaked reed", "Sealing wax" } },
        { "Voices | Small witness", new string[] { "Smoke fired clay", "Cut slip and firing clouds", "Chalk slip", "Pitch-soaked reed", "Sealing wax" } },
        { "Voices | Reed rack and cords", new string[] { "Pitch-soaked reed", "Flax cord" } },
        { "Voices | Breath above the open throat", new string[] { "Condensed breath" } },
        { "Pall | Fired name slips", new string[] { "Madder binding", "Chalk slip", "Smoke fired clay", "Pitch-soaked reed" } },
        { "Skin | Covered limbs and torso", new string[] { "Indigo skin" } },
    };
    internal static readonly (string slot,string map,string rgb,float metallic,float gloss)[] Recipe = {
        ("Silt | Indigo skin","Indigo-Skin","ffffff",0f,0f),
        ("Silt | Combed ivory","Ivory-Locks","ffffff",0f,0f),
        ("Silt | Copper iris","Copper-Iris","ffffff",0f,0f),
        ("Silt | Ash brows","","453a4b",0f,0f),
        ("Silt | Auricle paint","Auricle","ffffff",0f,0f),
        ("Silt | Worn brass","","ae8653",0.65f,0.61f),
        ("Cantor | Wool and resist print","Ebb-Procession","ffffff",0f,0f),
        ("Cantor | Pall and dike chart","Ebb-Pall","ffffff",0f,0f),
        ("Cantor | Madder binding","","82422e",0f,0f),
        ("Cantor | Flax cord","","b8a786",0f,0f),
        ("Cantor | Pitch-soaked reed","","303d3b",0f,0f),
        ("Cantor | Smoke fired clay","","ab6b48",0f,0.34f),
        ("Cantor | Chalk slip","","c7ae89",0f,0.38f),
        ("Cantor | Rubbed copper","","99715b",0.45f,0.52f),
        ("Cantor | Cut slip and firing clouds","Ebb-Stoneware","ffffff",0f,0.29f),
        ("Cantor | Condensed breath","","8fb9ad",0f,0.64f),
        ("Cantor | Sealing wax","","763b32",0f,0.57f),
    };
    internal static string SurfaceName(string slot) => slot.Split('|').Last().Trim();
    internal static bool MaterialsMatch(SkinnedMeshRenderer skin) =>
        MeshSlots.TryGetValue(skin.name,out var names) && skin.sharedMaterials.SequenceEqual(names.Select(Surface));
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
            ti.sRGBTexture=true;
            ti.mipmapEnabled=true;ti.streamingMipmaps=false;
            ti.filterMode=FilterMode.Trilinear;ti.wrapMode=TextureWrapMode.Clamp;
            ti.GetSourceTextureWidthAndHeight(out int width,out int height);
            ti.maxTextureSize=Math.Max(width,height);
            var desktop=ti.GetPlatformTextureSettings("Standalone");
            desktop.overridden=compressed;desktop.maxTextureSize=ti.maxTextureSize;
            desktop.format=TextureImporterFormat.BC7;desktop.compressionQuality=100;
            ti.SetPlatformTextureSettings(desktop);
            ti.textureCompression=compressed?TextureImporterCompression.CompressedHQ:TextureImporterCompression.Uncompressed;
            ti.alphaSource=TextureImporterAlphaSource.None;
            ti.anisoLevel=4;ti.SaveAndReimport();
        }
    }
    static Material[] ConfigureMaterials()
    {
        var result=new Material[Recipe.Length];
        for(int i=0;i<Recipe.Length;i++)
        {
            var row=Recipe[i];
            var m=CreateMaterial(Root+"/Materials/"+SurfaceName(row.slot)+".mat",
                Shader.Find(row.gloss>0?"Standard":"Nightcap/Painted Character"));
            ColorUtility.TryParseHtmlString("#"+row.rgb,out var tint);
            m.color=tint;m.mainTexture=row.map.Length>0?Texture(row.map):null;
            m.mainTextureOffset=Vector2.zero;m.mainTextureScale=Vector2.one;
            if(row.gloss>0)
            {
                m.SetFloat("_Metallic",row.metallic);m.SetFloat("_Glossiness",row.gloss);
                if(row.slot.EndsWith("Condensed breath"))
                {
                    m.EnableKeyword("_EMISSION");m.SetColor("_EmissionColor",tint.linear*.12f);
                }
            }
            else {m.SetFloat("_DiffuseWrap",.35f);m.SetFloat("_IndirectGain",1.5f);}
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
        foreach(var previous in importer.GetExternalObjectMap().Keys.Where(id=>id.type==typeof(Material)).ToArray()) importer.RemoveRemap(previous);
        for(int i=0;i<Recipe.Length;i++)
            importer.AddRemap(new AssetImporter.SourceAssetIdentifier(typeof(Material),Recipe[i].slot.Replace('|','_')),materials[i]);
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
        if(name=="Skin | Covered limbs and torso" || name=="Underlayer | Fitted linen shift") return state==1;
        if(name.StartsWith("Habit |") || name.StartsWith("Pall |") || name.StartsWith("Binding |") || name.StartsWith("Voices |")) return state==0;
        return true;
    }
    internal static void SetOutfit(GameObject actor,int state)
    {
        foreach(var skin in actor.GetComponentsInChildren<SkinnedMeshRenderer>(true)) skin.enabled=Visible(skin.name,state);
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
            Check(skins.Length==34,"Expected 34 skinned renderers, got "+skins.Length);
            foreach(var skin in skins)
            {
                Check(MaterialsMatch(skin),
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
        RenderSettings.ambientLight=preset==2?new Color(.43f,.47f,.58f):new Color(.49f,.49f,.52f);
        key.type=preset==2?LightType.Point:LightType.Directional;
        key.shadows=LightShadows.Soft;key.shadowStrength=.65f;
        key.color=preset==2?new Color(1,.70f,.49f):new Color(1,.96f,.92f);
        key.intensity=preset==2?1.9f:1.25f;key.range=3f;
        key.transform.position=new Vector3(.65f,1.42f,.72f);
        key.transform.rotation=Quaternion.LookRotation(new Vector3(preset==1?-.64f:.64f,-.82f,-.82f));
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
        CameraPose(cam,new Vector3(0,.86f,.03f),new Vector3(.58f,.14f,1.8f),.94f);
        var views=new GameObject("Fixed review cameras").transform;
        void FixedView(string name,Vector3 at,Vector3 from,float size)
        {
            var fixedCamera=new GameObject(name).AddComponent<Camera>();
            fixedCamera.CopyFrom(cam);fixedCamera.enabled=false;
            fixedCamera.transform.SetParent(views);CameraPose(fixedCamera,at,from,size);
        }
        var center=new Vector3(0,.86f,.03f);
        FixedView("Side",center,Vector3.right,.94f);FixedView("Rear",center,Vector3.back,.94f);
        FixedView("Face and collar",new Vector3(0,1.52f,.05f),new Vector3(.43f,.12f,1.65f),.23f);
        FixedView("Printed hem",new Vector3(0,.30f,.08f),new Vector3(.16f,.05f,1.45f),.30f);
        FixedView("128 pixels at 720p",new Vector3(0,.857f,.03f),Vector3.forward,1.714f*720/256);
        if(SceneView.lastActiveSceneView)
            SceneView.lastActiveSceneView.LookAt(new Vector3(0,.93f,0),cam.transform.rotation,1.23f,true);
        Check(EditorSceneManager.SaveScene(scene,Scene),"Unable to save review scene");
        AssetDatabase.SaveAssets();
    }
    [MenuItem("Nightcap/Ebb Cantor/Build static handoff")]
    public static void Run()
    {
        Directory.CreateDirectory(Evidence);
        AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
        ConfigureTextures(false);var materials=ConfigureMaterials();
        ConfigureModel(materials);BuildPrefab();BuildScene();
        Debug.Log("CANTOR_BUILD_COMPLETE");
    }
    static void PreviewOutfit(int state)
    {
        var actor=GameObject.Find("Ebb Cantor");
        Check(actor && actor.scene.path==Scene,"Open the Ebb Cantor review scene");
        var skins=actor.GetComponentsInChildren<SkinnedMeshRenderer>();
        Undo.RecordObjects(skins,"Preview outfit");
        SetOutfit(actor,state);
        foreach(var skin in skins)PrefabUtility.RecordPrefabInstancePropertyModifications(skin);
    }
    [MenuItem("Nightcap/Ebb Cantor/Preview/Robed")]
    static void PreviewRobed() => PreviewOutfit(0);
    [MenuItem("Nightcap/Ebb Cantor/Preview/Base")]
    static void PreviewBase() => PreviewOutfit(1);
    internal static void Compress() {ConfigureTextures(true);}
}



