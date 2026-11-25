Shader "Nightcap/Furnace Warden/Painted Heat"
{
    Properties
    {
        _MainTex ("Painted Albedo", 2D) = "white" {}
        _HeatMask ("Recessed heat (linear)", 2D) = "black" {}
        _HeatIntensity ("Heat intensity", Range(0,2)) = 0.85
        _Color ("Tint", Color) = (1,1,1,1)
        _DiffuseWrap ("Diffuse Wrap", Range(0,0.5)) = 0.2
        _IndirectGain ("Indirect Light Gain", Range(1,2)) = 1.25
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 200
        CGPROGRAM
        #pragma surface surf Painted fullforwardshadows addshadow exclude_path:deferred
        #pragma target 3.0
        #include "Lighting.cginc"
        sampler2D _MainTex;
        fixed4 _Color;
        sampler2D _HeatMask;
        half _HeatIntensity;
        half _DiffuseWrap;
        half _IndirectGain;
        struct Input { float2 uv_MainTex; };

        // Match Unity's Lambert GI contract, including light attenuation and probes.
        // Normalizing the wrap preserves the directly facing diffuse maximum.
        half4 LightingPainted(SurfaceOutput s, UnityGI gi)
        {
            half diffuse = saturate((dot(s.Normal, gi.light.dir) + _DiffuseWrap) / (1 + _DiffuseWrap));
            half3 color = s.Albedo * gi.light.color * diffuse;
            #ifdef UNITY_LIGHT_FUNCTION_APPLY_INDIRECT
                color += s.Albedo * gi.indirect.diffuse * _IndirectGain;
            #endif
            return half4(color, s.Alpha);
        }
        void LightingPainted_GI(SurfaceOutput s, UnityGIInput data, inout UnityGI gi)
        {
            gi = UnityGlobalIllumination(data, 1.0, s.Normal);
        }
        void surf(Input IN, inout SurfaceOutput o)
        {
            fixed4 paint = tex2D(_MainTex, IN.uv_MainTex) * _Color;
            o.Albedo = paint.rgb;
            o.Alpha = paint.a;
            o.Emission = paint.rgb * tex2D(_HeatMask, IN.uv_MainTex).r * _HeatIntensity;
        }
        ENDCG
    }
    Fallback "Diffuse"
}
