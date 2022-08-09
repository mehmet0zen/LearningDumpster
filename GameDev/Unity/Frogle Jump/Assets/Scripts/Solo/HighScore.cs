using UnityEngine;
using TMPro;

public class HighScore : MonoBehaviour
{
    public TextMeshProUGUI highScore;

    void Start() {
        if (PlayerPrefs.GetInt("HighScore", 0) <= 0) {
            highScore.text = " ";
        } else {
            highScore.text = "HS: " + PlayerPrefs.GetInt("HighScore", 0).ToString();
        }
    }

    void Update()
    {
        if (PlayerPrefs.GetInt("HighScore", 0) <= 0) {
            highScore.text = " ";
        } else {
            highScore.text = "HS: " + PlayerPrefs.GetInt("HighScore", 0).ToString();
        }
    }

    public void OnReset() {
        PlayerPrefs.DeleteKey("HighScore");
        PlayerPrefs.DeleteKey("userName");
    }
}
