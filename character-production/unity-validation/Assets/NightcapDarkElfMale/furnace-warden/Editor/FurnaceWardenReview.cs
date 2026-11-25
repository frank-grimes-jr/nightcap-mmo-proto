using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using SceneManager = UnityEngine.SceneManagement.SceneManager;
using UnityEditor;
using UnityEditor.SceneManagement;
using Object = UnityEngine.Object;
using static FurnaceWardenBuild;

public static class FurnaceWardenReview
{
    [Serializable] public class MeshRow
    {
        public string name, material; public int triangles, influences, bindings, uvCount, vertices;
        public float weightError, boundsEscape; public Vector3 min,max;
    }
    [Serializable] public class Mapping { public string human, bone; }
    [Serializable] public class MapInfo { public string name,format;public int size,mips;public bool sRGB; }
    [Serializable] public class Report
    {
        public string unity,device,avatar; public bool passed,forwardZ,rootIdentity,edgeCameraPassed;
        public int renderers,rigTransforms,clips,allTriangles,dressedTriangles,distancePixels;
        public float barefoot,equipped,leftSole,rightSole,edgePixelRetention;
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
        var armature=hierarchy.Single(t=>t.name=="Male_GameRig");
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
            var mr=new MeshRow{name=skin.name,material=skin.sharedMaterial.name,vertices=mesh.vertexCount,
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
            Check(skin.sharedMaterial && skin.sharedMaterial.shader.isSupported && !ShaderUtil.ShaderHasError(skin.sharedMaterial.shader),"Shader problem on "+skin.name);
            Check(skin.name=="DarkElf_Brows" || skin.sharedMaterial.mainTexture,"Missing paint on "+skin.name);
            positions.Add(skin.name,p);r.meshes.Add(mr);r.allTriangles+=mr.triangles;
            if(skin.enabled)r.dressedTriangles+=mr.triangles;
        }
        for(int i=0;i<actors.Length;i++)
        {
            var state=actors[i];
            var sets=state.GetComponentsInChildren<SkinnedMeshRenderer>(true);
            Check(sets.Length==38 && sets.All(s=>s.enabled==Visible(s.name,i)),"State toggles mismatch "+state.name);
            Check(state.GetComponentsInChildren<Animator>(true).Length==1,"Wrong rig count "+state.name);
            Check(sets.All(s=>s.bones.All(b=>b.IsChildOf(state.transform)) && s.sharedMesh==skins.Single(other=>other.name==s.name).sharedMesh),"Broken instance mesh or bone "+state.name);
        }
        r.renderers=skins.Length;Check(r.renderers==38 && r.allTriangles==52884 && r.dressedTriangles==31324,"Renderer/triangle count mismatch");
        var body=BoundsOf(positions["DarkElf_HeadAndNeck"].Concat(positions["DarkElf_CoveredBody"]));
        r.barefoot=body.size.y;r.equipped=BoundsOf(skins.Where(s=>s.enabled).SelectMany(s=>positions[s.name])).size.y;
        r.leftSole=positions["Warden_Sabatons_l"].Min(v=>v.y);r.rightSole=positions["Warden_Sabatons_r"].Min(v=>v.y);
        var foot=animator.GetBoneTransform(HumanBodyBones.LeftFoot);var toe=animator.GetBoneTransform(HumanBodyBones.LeftToes);
        r.forwardZ=(toe.position-foot.position).normalized.z>.55f;
        Check(r.forwardZ && Mathf.Abs(r.barefoot-1.820f)<.0182f && Mathf.Abs(r.equipped-1.857f)<.01857f,
            "Orientation or scale mismatch "+r.forwardZ+" barefoot "+r.barefoot+" dressed "+r.equipped);
        Check(Mathf.Abs(r.leftSole)<.001f && Mathf.Abs(r.rightSole)<.001f,"Boots miss floor");
        foreach(string map in Maps)
        {
            var t=Texture(map);var ti=(TextureImporter)AssetImporter.GetAtPath(AssetDatabase.GetAssetPath(t));
            Check(ti.sRGBTexture==(map!="Warden-Heat") && t.mipmapCount>1 && t.width==ti.maxTextureSize,"Texture setting "+map);
            r.textures.Add(new MapInfo{name=map,format=t.format.ToString(),size=t.width,mips=t.mipmapCount,sRGB=ti.sRGBTexture});
        }
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
        CameraPose(cam,new Vector3(0,.925f,.025f),new Vector3(1.55f,.33f,4.5f),1.045f);
    }
    static void Portrait(Camera c)
    {
        CameraPose(c,new Vector3(0,1.62f,.065f),new Vector3(.45f,.16f,1.75f),.292f);
    }
    static void EdgeAndDistance(Camera c,Report r)
    {
        const int w=960,h=720;
        var at=new Vector3(0,.9285f,.025f);
        CameraPose(c,at,Vector3.forward,1.857f*h/(2*128f));
        Capture(c,"Distance-128",w,h);
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
        var center=new Vector3(0,.925f,.025f);
        Hero(c);Capture(c,"Neutral-three-quarter");
        CameraPose(c,center,Vector3.forward,1.045f);Capture(c,"Front");
        CameraPose(c,center,Vector3.back,1.045f);Capture(c,"Rear");
        CameraPose(c,center,Vector3.right,1.045f);Capture(c,"Side");
        Portrait(c);Capture(c,"Helm-detail",940,860);
        var iron=Surface("Banked Iron");float heat=iron.GetFloat("_HeatIntensity");
        try{iron.SetFloat("_HeatIntensity",0);Capture(c,"Helm-albedo-heat",940,860);}
        finally{iron.SetFloat("_HeatIntensity",heat);}
        Hero(c);SetLight(key,1);Capture(c,"Reversed-key");
        SetLight(key,2);Capture(c,"Forge");SetLight(key,0);
        EdgeAndDistance(c,r);
        Show(actors,1);Hero(c);Capture(c,"Armored-helm-off");
        CameraPose(c,new Vector3(0,1.685f,.055f),new Vector3(.5f,.1f,1.8f),.193f);
        Capture(c,"Uncovered-head",800,820);
        CameraPose(c,new Vector3(0,1.69f,.055f),new Vector3(1,.025f,.18f),.20f);
        Capture(c,"Head-profile",760,800);
        Show(actors,2);Hero(c);Capture(c,"Base");CameraPose(c,center,Vector3.back,1.045f);Capture(c,"Base-rear");
        Show(actors,0);Hero(c);
    }
    static void Unlit(GameObject actor,Camera c)
    {
        var shader=Shader.Find("Unlit/Texture");var temp=new Dictionary<Material,Material>();
        var old=actor.GetComponentsInChildren<SkinnedMeshRenderer>(true).ToDictionary(s=>s,s=>s.sharedMaterial);
        try
        {
            foreach(var pair in old)
            {
                if(!temp.TryGetValue(pair.Value,out var m)){m=new Material(shader);m.mainTexture=pair.Value.mainTexture;temp.Add(pair.Value,m);}
                pair.Key.sharedMaterial=m;
            }
            Portrait(c);Capture(c,"Unlit-portrait",760,760);Hero(c);Capture(c,"Unlit-suit");
            var floor=GameObject.Find("Matte floor");var backdrop=c.backgroundColor;
            try
            {
                floor.SetActive(false);c.backgroundColor=Color.clear;
                CameraPose(c,new Vector3(0,.93f,.035f),new Vector3(-.34f,.15f,1.65f),1.04f);
                Capture(c,"Unlit-Blender-match",670,850);
            }
            finally{floor.SetActive(true);c.backgroundColor=backdrop;}
        }
        finally{foreach(var p in old)p.Key.sharedMaterial=p.Value;foreach(var m in temp.Values)Object.DestroyImmediate(m);}
    }
    [MenuItem("Nightcap/Furnace Warden/Verify and capture review")]
    public static void Run()
    {
        Directory.CreateDirectory(Evidence);
        ConfigureTextures(false);
        EditorSceneManager.OpenScene(Scene);var actors=StatesInScene();
        Portrait(Camera.main);Capture(Camera.main,"Full-resolution-before-compression",940,860);
        Compress();AssetDatabase.ImportAsset(Model,ImportAssetOptions.ForceUpdate|ImportAssetOptions.ForceSynchronousImport);
        EditorSceneManager.OpenScene(Scene);actors=StatesInScene();
        var r=Inspect(actors);Shots(actors,r);Unlit(actors[0],Camera.main);
        EditorSceneManager.OpenScene(Scene);
        r.passed=true;File.WriteAllText(Path.Combine(Evidence,"import-audit.json"),JsonUtility.ToJson(r,true));
        Debug.Log("WARDEN_REVIEW_COMPLETE");
    }
    static readonly string PlayKey="Nightcap.Warden.StaticPlayCheck";
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
    static void PollPlay()
    {
        if(!SessionState.GetBool(PlayKey,false) || !EditorApplication.isPlaying ||
           EditorApplication.isCompiling || !SceneManager.GetActiveScene().isLoaded || !Camera.main)return;
        SessionState.EraseBool(PlayKey);
        CheckPlay();
    }
    static void CheckPlay()
    {
        int code=1;
        try
        {
            var actors=StatesInScene();Check(actors[0].activeSelf && !actors[1].activeSelf && !actors[2].activeSelf,"Play state mismatch");
            var r=Inspect(actors);Hero(Camera.main);Capture(Camera.main,"Play-mode",720,800);
            r.passed=true;File.WriteAllText(Path.Combine(Evidence,"play-audit.json"),JsonUtility.ToJson(r,true));
            Debug.Log("WARDEN_PLAY_COMPLETE");code=0;
        }
        catch(Exception e){Debug.LogException(e);}
        finally{EditorApplication.ExitPlaymode();EditorApplication.Exit(code);}
    }
}

