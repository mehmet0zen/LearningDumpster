using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LevelSucceded : MonoBehaviour
{
    public Image SuccessIcon;
    public Image FailedIcon;
    public Color successColor;
    public bool succeded {get; set;} = false;
    public bool failed {get; set;} = false;
    public int successCount = 0;

    private void Update() {
        if (succeded) {
            SuccessIcon.gameObject.SetActive(true);
            SuccessIcon.color = successColor;
            successCount++;
        } 
        if (failed) {
            FailedIcon.gameObject.SetActive(true);
        }
    }
}
