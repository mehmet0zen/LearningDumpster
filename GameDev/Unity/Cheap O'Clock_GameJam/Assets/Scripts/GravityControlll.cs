using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GravityControlll : MonoBehaviour
{
    public float gravity = 10;
    public enum GravityDirection { Down, Left, Up, Right };
    public GravityDirection gDirection;
    playerController pc;
    cameraFollow cam;
    int controlTime = 1;

    void Start()
    {
        gDirection = GravityDirection.Down;
        cam = FindObjectOfType<cameraFollow>();
        pc = GetComponent<playerController>();
    }
    void Update()
    {
        Quaternion rotateTo = Quaternion.Euler(cam.angle);
        gameObject.transform.rotation = Quaternion.Lerp(gameObject.transform.rotation, rotateTo, 1.8f * Time.deltaTime);
        if (pc.IsGrounded()) {
            controlTime = 1;
        }
        switch (gDirection)
        {
            case GravityDirection.Down:
                Physics2D.gravity = new Vector2(0, -gravity);
                cam.angle = new Vector3(0, 0, 0);
                if (Input.GetKeyDown(KeyCode.LeftArrow) && controlTime > 0)
                {
                    Debug.Log("Down - Right");
                    gDirection = GravityDirection.Right;
                    controlTime--;
                    
                } else if (Input.GetKeyDown(KeyCode.RightArrow) && controlTime > 0) {
                    Debug.Log("Down - Left");
                    gDirection = GravityDirection.Left;
                    controlTime--;
                }
                break;

            case GravityDirection.Left:
                Physics2D.gravity = new Vector2(-gravity, 0);
                cam.angle = new Vector3(0, 0, -90);
                if (Input.GetKeyDown(KeyCode.LeftArrow) && controlTime > 0)
                {
                    Debug.Log("Left - Down");
                    gDirection = GravityDirection.Down;
                    controlTime--;
                } else if (Input.GetKeyDown(KeyCode.RightArrow) && controlTime > 0) {
                    Debug.Log("Left - Up");
                    gDirection = GravityDirection.Up;
                    controlTime--;
                }
                break;

            case GravityDirection.Up:
                Physics2D.gravity = new Vector2(0, gravity);
                cam.angle = new Vector3(0, 0, 180);
                if (Input.GetKeyDown(KeyCode.LeftArrow) && controlTime > 0)
                {
                    Debug.Log("Up - Left");
                    gDirection = GravityDirection.Left;
                    controlTime--;
                } else if (Input.GetKeyDown(KeyCode.RightArrow) && controlTime > 0) {
                    Debug.Log("Up - Right");
                    gDirection = GravityDirection.Right;
                    controlTime--;
                }
                break;

            case GravityDirection.Right:
                Physics2D.gravity = new Vector2(gravity, 0);
                cam.angle = new Vector3(0, 0, 90);
                if (Input.GetKeyDown(KeyCode.LeftArrow) && controlTime > 0)
                {
                    Debug.Log("Right - Up");
                    gDirection = GravityDirection.Up;
                    controlTime--;
                } else if (Input.GetKeyDown(KeyCode.RightArrow) && controlTime > 0) {
                    Debug.Log("Right - Down");
                    gDirection = GravityDirection.Down;
                    controlTime--;
                }
                break;
        }
    }
}
