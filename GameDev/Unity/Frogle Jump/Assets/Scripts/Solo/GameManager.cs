using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    public GameObject barier;
    public GameObject mainCamera;
    public GameObject highScoreLine;
    public Text score;
    public Text gameOverScore;
    public Text gg;
    public int platformCount = 8;
    public GameObject[] platformSprites;
    public Vector2 platformRangeHorizontal = new Vector2(-2f, 2f);
    public Vector2 platformRangeVertical = new Vector2(1.4f, 2f);
    [HideInInspector] public Vector3 spawnPosition;
    [HideInInspector] public bool playerDied = false;
    [HideInInspector] public bool smashing = false;
    [HideInInspector] public bool canSmash = false;

    public GameObject canvas;
    public GameObject gameScore;
    public GameObject pauseCanvas;

    [HideInInspector]public int randomSprite;
    [HideInInspector]public int previusRandom;

    private void Start()
    {
        Application.targetFrameRate = 30;
        randomSprite = (int)Random.Range(0, platformSprites.Length - 3);
        previusRandom = 0;
        spawnPosition = new Vector3();
        for (int i = 0; i < platformCount; i++) {
            spawnPosition.y += Random.Range(platformRangeVertical.x, platformRangeVertical.y);
            spawnPosition.x = Random.Range(platformRangeHorizontal.x, platformRangeHorizontal.y);
            while (randomSprite == previusRandom) {
                randomSprite = (int)Random.Range(0, platformSprites.Length - 3);
            }
            Instantiate(platformSprites[randomSprite], spawnPosition, Quaternion.identity);
            previusRandom = randomSprite;
        }
        SetHighScoreUI();
    }

    public void OnRestart() {
        SceneManager.LoadScene( SceneManager.GetActiveScene().name );
        SetHighScoreUI();
    }

    public void Paused() {
        pauseCanvas.SetActive(true);
        Time.timeScale = 0f;
    }
    public void Resumed() {
        pauseCanvas.SetActive(false);
        Time.timeScale = 1f;
    }

    private void OnApplicationFocus(bool focusStatus) {
        if (!focusStatus) {
            Paused();
        }
    }

    private void Update() {
        //If Player is dead
        if (playerDied == true) {
            gameObject.SetActive(false);
            canvas.SetActive(true);
            gameScore.SetActive(false);
        }

        if (Input.GetKeyDown(KeyCode.Escape) || Input.GetKeyDown(KeyCode.P)) {
            if (pauseCanvas.activeSelf) {
                Resumed();
            } else {
                Paused();
            }
        }
        if (!pauseCanvas.activeSelf) {
            Time.timeScale = 1f;
        }
    }

    void SetHighScoreUI() {
        //high score line
        highScoreLine.transform.position = new Vector3(highScoreLine.transform.position.x, PlayerPrefs.GetInt("HighScore", 0), 0);
        if (PlayerPrefs.GetInt("HighScore", 0) == 0) {
            highScoreLine.SetActive(false);
        } else {
            highScoreLine.SetActive(true);
        }
    }
}
