using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneLoad : MonoBehaviour
{
    public void LoadSceneName(string sceneName) {
        SceneManager.LoadScene(sceneName);
        Time.timeScale = 1f;
    }
    public void Quit() {
        Application.Quit();
    }
}
