using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cameraFollow : MonoBehaviour
{
    public Vector3 angle;
    // public GameObject borderSpikes;
    private void Update() {
        // borderSpikes.transform.rotation = gameObject.transform.rotation;
        Quaternion rotateTo = Quaternion.Euler(angle);
        gameObject.transform.rotation = Quaternion.Lerp(gameObject.transform.rotation, rotateTo, 2f * Time.deltaTime);

        // Rotate camera
    }

}
