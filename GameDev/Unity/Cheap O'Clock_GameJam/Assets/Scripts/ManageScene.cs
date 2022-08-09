using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ManageScene : MonoBehaviour
{
    public Canvas pause;
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space) && SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Menu"))
        {
            SceneManager.LoadScene("Game");
        } else if (Input.GetKeyDown(KeyCode.P) && SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Game"))
        {
            if (Time.timeScale == 0) {
                Time.timeScale = 1;
                pause.gameObject.SetActive(false);
            } else if (Time.timeScale == 1) {
                Time.timeScale = 0;
                pause.gameObject.SetActive(true);
            }
        }
    }

    public void Resume() {
        Time.timeScale = 1;
        pause.gameObject.SetActive(false);
    }
    public void MainMenu(string sceneName) {
        SceneManager.LoadScene(sceneName);
        Time.timeScale = 1;
    }

    private void OnApplicationFocus(bool focusStatus) {
        if (focusStatus == false && SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Game")) {
            Time.timeScale = 0;
            pause.gameObject.SetActive(true);
        } 
    }
}
