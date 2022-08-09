using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BGScroll : MonoBehaviour
{
    [Range(1,5)]
    public float scrollSpeed = 4;
    public Rigidbody2D playerRB;
    float offset;
    Material mat;
    void Awake()
    {
        mat = GetComponent<Renderer>().material;
    }

    void Update()
    {
        if (playerRB != null) {
            if (playerRB.velocity.y < -0.1f) {
                offset += (Time.deltaTime * scrollSpeed) / 20;
            } else {
                offset += (Time.deltaTime * scrollSpeed) / 15;
            }
        } else {
            offset += (Time.deltaTime * scrollSpeed) / 15;
        }
        mat.SetTextureOffset("_MainTex", new Vector2(0, offset));
    }
}
