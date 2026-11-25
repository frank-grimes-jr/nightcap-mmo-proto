using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using Object=UnityEngine.Object;

// Unity exposes the Avatar configuration stage through its Inspector's Configure button.
// This editor-only check uses that same entry point in the pinned 6000.5.7f1 editor.
public static class EbbCantorAvatar
{
    [Serializable] class Result
    {
        public string stage,editor; public bool returnedToReview;
        public List<EbbCantorReview.Mapping> assigned=new List<EbbCantorReview.Mapping>();
    }
    public static void Inspect()
    {
        EditorSceneManager.OpenScene(EbbCantorBuild.Scene);
        var avatar=AssetDatabase.LoadAllAssetsAtPath(EbbCantorBuild.Model).OfType<Avatar>().Single();
        var inspector=Editor.CreateEditor(avatar);
        const BindingFlags flags=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Instance;
        var result=new Result{editor=inspector.GetType().FullName};
        try
        {
            var enter=inspector.GetType().GetMethod("SwitchToEditMode",flags);
            EbbCantorBuild.Check(enter!=null,"Avatar Configure entry unavailable");
            enter.Invoke(inspector,null);
            var stage=StageUtility.GetCurrentStage();result.stage=stage.GetType().Name;
            EbbCantorBuild.Check(result.stage=="AvatarConfigurationStage","Wrong configuration stage");
            var actor=(GameObject)inspector.GetType().GetField("m_GameObject",flags).GetValue(inspector);
            var animator=actor.GetComponent<Animator>();
            var importer=(ModelImporter)AssetImporter.GetAtPath(EbbCantorBuild.Model);
            var mapping=importer.humanDescription.human.ToDictionary(h=>h.humanName,h=>h.boneName);
            for(int i=0;i<(int)HumanBodyBones.LastBone;i++)
            {
                if(!mapping.TryGetValue(HumanTrait.BoneName[i],out var name))continue;
                var joint=animator.GetBoneTransform((HumanBodyBones)i);
                EbbCantorBuild.Check(joint && joint.name==name,"Configuration stage missing "+name);
                result.assigned.Add(new EbbCantorReview.Mapping{human=HumanTrait.BoneName[i],bone=joint.name});
            }
            EbbCantorBuild.Check(result.assigned.Count==52,"Incomplete configuration stage mapping");
        }
        finally
        {
            StageUtility.GoToMainStage();
            Object.DestroyImmediate(inspector);
            EditorSceneManager.OpenScene(EbbCantorBuild.Scene);
        }
        result.returnedToReview=StageUtility.GetCurrentStageHandle()==StageUtility.GetMainStageHandle();
        File.WriteAllText(Path.Combine(EbbCantorBuild.Evidence,"avatar-configuration.json"),JsonUtility.ToJson(result,true));
        Debug.Log("CANTOR_AVATAR_COMPLETE");
    }
}

