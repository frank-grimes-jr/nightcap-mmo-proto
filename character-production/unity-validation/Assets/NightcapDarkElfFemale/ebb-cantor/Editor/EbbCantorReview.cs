using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using SceneManager = UnityEngine.SceneManagement.SceneManager;
using UnityEditor;
using UnityEditor.SceneManagement;
using Object = UnityEngine.Object;
using static EbbCantorBuild;

public static class EbbCantorReview
{
    [Serializable] public class MeshRow
    {
        public string name, material; public int triangles, influences, bindings, uvCount, vertices;
        public float weightError, boundsEscape; public Vector3 min,max;
    }
    [Serializable] public class Mapping { public string human, bone; }
    [Serializable] public class MapInfo { public string name,format;public int size,height,mips;public bool sRGB; }
    [Serializable] public class Report
    {
        public string unity,device,avatar; public bool passed,forwardZ,rootIdentity,edgeCameraPassed;
        public int renderers,rigTransforms,clips,allTriangles,dressedTriangles,distancePixels;
        public int stationaryFrames; public float jointDriftMetres; public float barefoot,equipped,leftSole,rightSole,edgePixelRetention;
        public List<MeshRow> meshes=new List<MeshRow>();public List<Mapping> mapping=new List<Mapping>();
        public List<MapInfo> textures=new List<MapInfo>(); public List<string> errors=new List<string>();
    }
    static GameObject[] StatesInScene()
    {
        var roots=SceneManager.GetActiveScene().GetRootGameObjects();
        return States.Select(n=>roots.Single(o=>o.name==n)).ToArray();
    }
    static void Show(GameObject[] actors,int state)
    {
        for(int i=0;i<actors.Length;i++)actors[i].SetActive(i==state);
    }
    static float Escape(Bounds b,Vector3 v)
    {
        return (v-b.ClosestPoint(v)).magnitude;
    }
    static Report Inspect(GameObject[] actors)
    {
        var r=new Report{unity=Application.unityVersion,device=SystemInfo.graphicsDeviceName};
        var baseAsset=Asset<GameObject>(Prefab);
        Check(baseAsset.GetComponentsInChildren<Camera>(true).Length==0 &&
              baseAsset.GetComponentsInChildren<Light>(true).Length==0 &&
              baseAsset.GetComponentsInChildren<Collider>(true).Length==0 &&
              baseAsset.GetComponentsInChildren<MonoBehaviour>(true).Length==0,"Unexpected prefab dependency");
        var actor=actors[0];
        r.rootIdentity=actor.transform.position.sqrMagnitude<1e-10f &&
            Quaternion.Angle(actor.transform.rotation,Quaternion.identity)<.001f &&
            (actor.transform.localScale-Vector3.one).sqrMagnitude<1e-10f;
        Check(r.rootIdentity,"Prefab root is not identity");
        var animator=actor.GetComponent<Animator>();
        Check(animator && animator.avatar.isValid && animator.avatar.isHuman && !animator.runtimeAnimatorController && !animator.applyRootMotion,"Invalid static Animator");
        r.avatar=animator.avatar.name;
        var hierarchy=actor.GetComponentsInChildren<Transform>(true);
        var armature=hierarchy.Single(t=>t.name=="Female_GameRig");
        var root=hierarchy.Single(t=>t.name=="Root");
        r.rigTransforms=root.GetComponentsInChildren<Transform>(true).Length;
        Check(r.rigTransforms==53 && root.IsChildOf(armature),"Unexpected deform hierarchy "+r.rigTransforms);
        var modelImport=(ModelImporter)AssetImporter.GetAtPath(Model);
        var humanImport=(ModelImporter)AssetImporter.GetAtPath(Human);
        var expected=humanImport.humanDescription.human.ToDictionary(h=>h.humanName,h=>h.boneName);
        for(int i=0;i<(int)HumanBodyBones.LastBone;i++)
        {
            if(!expected.TryGetValue(HumanTrait.BoneName[i],out string bone))continue;
            var mapped=animator.GetBoneTransform((HumanBodyBones)i);
            Check(mapped && mapped.name==bone && mapped.IsChildOf(root),"Avatar mapping "+HumanTrait.BoneName[i]+" / "+bone);
            r.mapping.Add(new Mapping{human=HumanTrait.BoneName[i],bone=bone});
        }
        Check(r.mapping.Count==expected.Count && r.mapping.Count==52,"Incomplete Humanoid mapping "+r.mapping.Count);
        r.clips=AssetDatabase.LoadAllAssetsAtPath(Model).OfType<AnimationClip>().Count();
        Check(r.clips==0 && !modelImport.importAnimation && !modelImport.optimizeGameObjects,"Unexpected animation import");
        var skins=actor.GetComponentsInChildren<SkinnedMeshRenderer>(true);
        var positions=new Dictionary<string,Vector3[]>();
        foreach(var skin in skins)
        {
            var mesh=skin.sharedMesh;
            var p=Vertices(skin);
            var box=BoundsOf(p);
            var mr=new MeshRow{name=skin.name,material=string.Join(" / ",skin.sharedMaterials.Select(m=>m.name)),vertices=mesh.vertexCount,
                triangles=mesh.triangles.Length/3,bindings=mesh.bindposes.Length,uvCount=mesh.uv.Length,min=box.min,max=box.max};
            Check(mesh && mesh.normals.Length==mesh.vertexCount && mr.uvCount==mesh.vertexCount,"Missing normals/UV0 on "+skin.name);
            Check(skin.bones.Length==mr.bindings && skin.bones.All(b=>b&&(b==root||b.IsChildOf(root))),"Foreign or missing skin bone "+skin.name);
            Check(mr.bindings>0 && skin.rootBone && mesh.bindposes.All(m=>Mathf.Abs(m.determinant)>1e-12f),"Invalid bindpose "+skin.name);
            foreach(var weight in mesh.boneWeights)
            {
                mr.weightError=Mathf.Max(mr.weightError,Mathf.Abs(weight.weight0+weight.weight1+weight.weight2+weight.weight3-1));
                mr.influences=Math.Max(mr.influences,new[]{weight.weight0,weight.weight1,weight.weight2,weight.weight3}.Count(w=>w>0));
            }
            Check(mr.influences>0 && mr.influences<=4 && mr.weightError<.0002f,"Invalid weights "+skin.name);
            mr.boundsEscape=p.Max(v=>Escape(skin.bounds,v));
            Check(mr.boundsEscape<.003f,skin.name+" bounds exclude skin by "+mr.boundsEscape+" m");
            Check(MaterialsMatch(skin) && skin.sharedMaterials.All(m=>m.shader.isSupported && !ShaderUtil.ShaderHasError(m.shader)), "Invalid material slots on "+skin.name);
            positions.Add(skin.name,p);r.meshes.Add(mr);r.allTriangles+=mr.triangles;
            if(skin.enabled)r.dressedTriangles+=mr.triangles;
        }
        for(int i=0;i<actors.Length;i++)
        {
            var state=actors[i];
            var sets=state.GetComponentsInChildren<SkinnedMeshRenderer>(true);
            Check(sets.Length==34 && sets.All(s=>s.enabled==Visible(s.name,i)),"State toggles mismatch "+state.name);
            Check(state.GetComponentsInChildren<Animator>(true).Length==1,"Wrong rig count "+state.name);
            Check(sets.All(s=>s.bones.All(b=>b.IsChildOf(state.transform)) && s.sharedMesh==skins.Single(other=>other.name==s.name).sharedMesh),"Broken instance mesh or bone "+state.name);
        }
        r.renderers=skins.Length;Check(r.renderers==34 && r.allTriangles==131488 && r.dressedTriangles==109276,"Renderer/triangle count mismatch");
        var body=BoundsOf(positions["Skin | Head neck and hands"].Concat(positions["Skin | Covered limbs and torso"]));
        r.barefoot=body.size.y;r.equipped=BoundsOf(skins.Where(s=>s.enabled).SelectMany(s=>positions[s.name])).size.y;
        r.leftSole=positions["Underlayer | River leather boots"].Where(v=>v.x<0).Min(v=>v.y);r.rightSole=positions["Underlayer | River leather boots"].Where(v=>v.x>0).Min(v=>v.y);
        var foot=animator.GetBoneTransform(HumanBodyBones.LeftFoot);var toe=animator.GetBoneTransform(HumanBodyBones.LeftToes);
        r.forwardZ=(toe.position-foot.position).normalized.z>.55f;
        Check(r.forwardZ && Mathf.Abs(r.barefoot-1.700f)<.017f && Mathf.Abs(r.equipped-1.714f)<.01714f,
            "Orientation or scale mismatch "+r.forwardZ+" barefoot "+r.barefoot+" dressed "+r.equipped);
        Check(Mathf.Abs(r.leftSole)<.001f && Mathf.Abs(r.rightSole)<.001f,"Boots miss floor");
        foreach(string map in Maps)
        {
            var t=Texture(map);var ti=(TextureImporter)AssetImporter.GetAtPath(AssetDatabase.GetAssetPath(t));
            Check(ti.sRGBTexture==true && t.mipmapCount>1 && t.width==ti.maxTextureSize,"Texture setting "+map);
            r.textures.Add(new MapInfo{name=map,format=t.format.ToString(),size=t.width,height=t.height,mips=t.mipmapCount,sRGB=ti.sRGBTexture});
        }
        foreach(var row in Recipe)
        {
            var mat=Surface(SurfaceName(row.slot));
            Check(mat.mainTexture==(row.map.Length>0?Texture(row.map):null),"Incorrect paint "+row.slot);
        }
        SetOutfit(actor,1);
        Check(skins.Count(x=>x.enabled)==18 && skins.All(x=>x.enabled==Visible(x.name,1)),"Base restoration failed");
        SetOutfit(actor,0);
        Check(skins.Count(x=>x.enabled)==32 && skins.All(x=>MaterialsMatch(x)),"Robed restoration failed");
        return r;
    }
    static Color32[] Capture(Camera cam,string file,int w=800,int h=920)
    {
        var target=new RenderTexture(w,h,24,RenderTextureFormat.ARGB32){antiAliasing=4};
        var prev=RenderTexture.active;var prevTarget=cam.targetTexture;var im=new Texture2D(w,h,TextureFormat.RGBA32,false);
        try
        {
            cam.targetTexture=target;cam.Render();RenderTexture.active=target;
            im.ReadPixels(new Rect(0,0,w,h),0,0);im.Apply();
            if(file!=null)File.WriteAllBytes(Path.Combine(Evidence,file+".png"),im.EncodeToPNG());
            return im.GetPixels32();
        }
        finally{cam.targetTexture=prevTarget;RenderTexture.active=prev;target.Release();Object.DestroyImmediate(target);Object.DestroyImmediate(im);}
    }
    internal static void Hero(Camera cam)
    {
        CameraPose(cam,new Vector3(0,.86f,.03f),new Vector3(.58f,.14f,1.8f),.94f);
    }
    static void Portrait(Camera c)
    {
        CameraPose(c,new Vector3(0,1.52f,.05f),new Vector3(.43f,.12f,1.65f),.23f);
    }
    static void EdgeAndDistance(Camera c,Report r)
    {
        const int w=960,h=720;
        var at=new Vector3(0,.857f,.03f);
        CameraPose(c,at,Vector3.forward,1.714f*h/(2*128f));
        Capture(c,"Distance-128",w,h);
        CameraPose(c,at,Vector3.back,c.orthographicSize);Capture(c,"Distance-rear",w,h);
        CameraPose(c,at,Vector3.forward,c.orthographicSize);
        var floor=GameObject.Find("Matte floor");floor.SetActive(false);
        var color=c.backgroundColor;
        try
        {
            c.backgroundColor=Color.clear;
            var pix=Capture(c,null,w,h);int low=h,high=-1;
            for(int i=0;i<pix.Length;i++)if(pix[i].a>128){low=Math.Min(low,i/w);high=Math.Max(high,i/w);}
            r.distancePixels=high-low+1;Check(Math.Abs(r.distancePixels-128)<=2,"Distance frame silhouette "+r.distancePixels);
            CameraPose(c,at,Vector3.forward,1.04f);var centered=Capture(c,null,w,h);
            int min=w,max=-1;
            for(int i=0;i<centered.Length;i++)if(centered[i].a>128){min=Math.Min(min,i%w);max=Math.Max(max,i%w);}
            int shift=w-3-max;
            c.transform.position-=c.transform.right*(shift*(2*c.orthographicSize/h));
            var edge=Capture(c,"Camera-edge",w,h);
            r.edgePixelRetention=(float)edge.Count(p=>p.a>128)/centered.Count(p=>p.a>128);
            r.edgeCameraPassed=r.edgePixelRetention>.985f && r.edgePixelRetention<1.015f;
            Check(r.edgeCameraPassed,"Near-edge silhouette was culled "+r.edgePixelRetention);
        }
        finally{floor.SetActive(true);c.backgroundColor=color;}
    }
    static void Shots(GameObject[] actors,Report r)
    {
        var c=Camera.main;var key=RenderSettings.sun;Show(actors,0);
        var center=new Vector3(0,.86f,.03f);
        Hero(c);Capture(c,"Neutral-three-quarter");
        SetLight(key,1);Capture(c,"Reversed-key");
        SetLight(key,2);
        var cool=RenderSettings.ambientLight;
        RenderSettings.ambientLight=new Color(.28f,.33f,.43f);Capture(c,"Dusk-before-fill");
        RenderSettings.ambientLight=cool;Capture(c,"Dusk");SetLight(key,0);
        CameraPose(c,center,Vector3.forward,.94f);Capture(c,"Front");
        CameraPose(c,center,Vector3.back,.94f);Capture(c,"Rear");
        CameraPose(c,center,Vector3.right,.94f);Capture(c,"Side");
        Portrait(c);Capture(c,"Face-collar",940,860);
        Hem(c);Capture(c,"Procession-seam",960,720);
        // Project the actual shared selvedge to pixels for the registered print detail.
        var pieces=actors[0].GetComponentsInChildren<SkinnedMeshRenderer>();
        var front=Vertices(pieces.Single(x=>x.name=="Habit | Funeral road front"));
        var east=Vertices(pieces.Single(x=>x.name=="Habit | East breadth"));
        Vector3Int Grid(Vector3 v)=>Vector3Int.RoundToInt(v*10000);
        var neighbor=new HashSet<Vector3Int>(east.Select(Grid));
        c.aspect=960f/720;
        var selvedge=front.Where(v=>v.y<.55f && neighbor.Contains(Grid(v)))
            .GroupBy(v=>Mathf.RoundToInt(v.y*100)).Select(g=>g.OrderByDescending(v=>v.z).First())
            .OrderBy(v=>v.y).Select(v=>c.WorldToViewportPoint(v)).ToArray();
        c.ResetAspect();
        Check(selvedge.Length>=8,"Insufficient shared seam positions");
        File.WriteAllLines(Path.Combine(Evidence,"hem-seam.tsv"),selvedge.Select(v=>
            FormattableString.Invariant($"{v.x*960:F2}\t{(1-v.y)*720:F2}")));
        CameraPose(c,new Vector3(.15f,.99f,.087f),new Vector3(.95f,.46f,1.5f),.23f);Capture(c,"Vessels");
        CameraPose(c,new Vector3(0,.29f,-.09f),new Vector3(-.49f,-.22f,-1.4f),.31f);Capture(c,"Rear-opening");
        EdgeAndDistance(c,r);
        SetOutfit(actors[0],1);Hero(c);Capture(c,"Base");
        CameraPose(c,center,Vector3.back,.94f);Capture(c,"Base-rear");
        CameraPose(c,new Vector3(0,1.56f,.05f),new Vector3(1,.025f,.02f),.20f);Capture(c,"Base-profile");
        SetOutfit(actors[0],0);Hero(c);
    }
    static void Hem(Camera c) => CameraPose(c,new Vector3(0,.30f,.08f),new Vector3(.16f,.05f,1.45f),.30f);
    internal static void Diagnostic(GameObject actor,Camera c,bool clay)
    {
        var old=actor.GetComponentsInChildren<SkinnedMeshRenderer>(true).ToDictionary(s=>s,s=>s.sharedMaterials);
        var temporary=new Dictionary<Material,Material>();
        try
        {
            foreach(var source in old.Values.SelectMany(a=>a).Distinct())
            {
                var mat=new Material(Shader.Find(clay?"Nightcap/Painted Character":source.mainTexture?"Unlit/Texture":"Unlit/Color"));
                if(clay)mat.color=new Color(.61f,.59f,.55f);
                else if(source.mainTexture)mat.mainTexture=source.mainTexture;
                else mat.color=source.color;
                temporary.Add(source,mat);
            }
            foreach(var pair in old)pair.Key.sharedMaterials=pair.Value.Select(m=>temporary[m]).ToArray();
            Hero(c);Capture(c,clay?"Flat-tint":"Unlit-albedo");
            Hem(c);Capture(c,clay?"Flat-hem":"Unlit-hem",960,720);
        }
        finally
        {
            foreach(var p in old)p.Key.sharedMaterials=p.Value;
            foreach(var m in temporary.Values)Object.DestroyImmediate(m);
        }
    }
    [MenuItem("Nightcap/Ebb Cantor/Verify and capture review")]
    public static void Run()
    {
        Directory.CreateDirectory(Evidence);
        ConfigureTextures(false);
        EditorSceneManager.OpenScene(Scene);var actors=StatesInScene();
        Portrait(Camera.main);Capture(Camera.main,"Face-before-compression",940,860);
        Hem(Camera.main);Capture(Camera.main,"Hem-before-compression",960,720);
        Compress();AssetDatabase.ImportAsset(Model,ImportAssetOptions.ForceUpdate|ImportAssetOptions.ForceSynchronousImport);
        EditorSceneManager.OpenScene(Scene);actors=StatesInScene();
        var r=Inspect(actors);Shots(actors,r);Diagnostic(actors[0],Camera.main,true);Diagnostic(actors[0],Camera.main,false);
        EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
        var fresh=(GameObject)PrefabUtility.InstantiatePrefab(Asset<GameObject>(Prefab));
        Inspect(new[]{fresh});
        EditorSceneManager.OpenScene(Scene);
        var deps=AssetDatabase.GetDependencies(Scene,true);
        Check(deps.All(path=>path.StartsWith(Root+"/") || path=="Assets/NightcapHumans/PaintedCharacter.shader" || !path.StartsWith("Assets/")),"Unexpected external dependency: "+string.Join(", ",deps));
        File.WriteAllLines(Path.Combine(Evidence,"scene-dependencies.txt"),deps);
        AssetDatabase.ExportPackage(new[]{Root,"Assets/NightcapHumans/PaintedCharacter.shader"},Path.Combine(Evidence,"Ebb-Cantor.unitypackage"),ExportPackageOptions.Recurse);
        r.passed=true;File.WriteAllText(Path.Combine(Evidence,"import-audit.json"),JsonUtility.ToJson(r,true));
        Debug.Log("CANTOR_REVIEW_COMPLETE");
    }
    static readonly string PlayKey="Nightcap.Cantor.StaticPlayCheck";
    public static void TestPlay()
    {
        EditorSceneManager.OpenScene(Scene);
        Hero(Camera.main);Capture(Camera.main,"Edit-mode",720,800);
        SessionState.SetBool(PlayKey,true);EditorApplication.EnterPlaymode();
    }
    [InitializeOnLoadMethod]
    static void ObservePlay()
    {
        EditorApplication.update+=PollPlay;
    }
    static Vector3[] initialJoints;
    static int firstFrame;
    static Vector3[] Joints(GameObject actor) => actor.GetComponentsInChildren<Transform>()
        .Single(t=>t.name=="Root").GetComponentsInChildren<Transform>().Select(t=>t.position).ToArray();
    static void PollPlay()
    {
        if(!SessionState.GetBool(PlayKey,false) || !EditorApplication.isPlaying ||
           EditorApplication.isCompiling || !SceneManager.GetActiveScene().isLoaded || !Camera.main)return;
        if(initialJoints==null)
        {
            initialJoints=Joints(StatesInScene()[0]);firstFrame=Time.frameCount;
            if(initialJoints.Length!=53){SessionState.EraseBool(PlayKey);EditorApplication.Exit(1);}
            return;
        }
        if(Time.frameCount-firstFrame<12)return;
        SessionState.EraseBool(PlayKey);
        CheckPlay();
    }
    static void CheckPlay()
    {
        int code=1;
        try
        {
            var actors=StatesInScene();Check(actors[0].activeSelf,"Play state mismatch");
            var r=Inspect(actors);
            r.stationaryFrames=Time.frameCount-firstFrame;
            r.jointDriftMetres=Joints(actors[0]).Zip(initialJoints,Vector3.Distance).Max();
            Check(r.jointDriftMetres<.000001f,"Static skeleton drift");
            Hero(Camera.main);Capture(Camera.main,"Play-mode",720,800);
            r.passed=true;File.WriteAllText(Path.Combine(Evidence,"play-audit.json"),JsonUtility.ToJson(r,true));
            Debug.Log("CANTOR_PLAY_COMPLETE");code=0;
        }
        catch(Exception e){Debug.LogException(e);}
        finally{EditorApplication.ExitPlaymode();EditorApplication.Exit(code);}
    }
}

