using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.UI;
public class LevelCreator : MonoBehaviour
{
    

    [Header("Blocks:")]
    public GameObject[] blocks;
    public Blocks[] bLocksToDestroy;
    public GameObject spawnBlock;
    public GameObject endBlock;
    public GameObject player;
    public LevelSucceded[] level = new LevelSucceded[6];
    public ParticleSystem explosion;

    [Header("UI:")]
    public Canvas GameOverUI;
    public TextMeshProUGUI timerUI;
    public TextMeshProUGUI deathCount;
    public TextMeshProUGUI gameOverDeathResult;
    public TextMeshProUGUI gameOverSuccesResult;
    public TextMeshProUGUI gameOverTimeResult;
    public SpriteRenderer[] lvlBgs;
    public Image skull;

    [Header("Coordinates:")]
    public List<Vector2> cordinates = new List<Vector2>();
    public List<Vector2> cordinates6 = new List<Vector2>();
    public List<Vector2> cordinates5 = new List<Vector2>();
    public List<Vector2> cordinates4 = new List<Vector2>();
    public List<Vector2> cordinates3 = new List<Vector2>();
    public List<Vector2> cordinates2 = new List<Vector2>();
    public List<Vector2> cordinates1 = new List<Vector2>();
    public Vector2[] bgCordinates;

    float timer = 61f;
    int previousRandom = 1;
    public int nextLevel = 2;
    int spikeCount = 0;

    private void Awake() {
        List<Vector2> avoidPoints = new List<Vector2>();
        foreach (SpriteRenderer i in lvlBgs) {
            int random = Random.Range(0, bgCordinates.Length);
            if (!avoidPoints.Contains(bgCordinates[random])){
                i.transform.position = bgCordinates[random];
                i.transform.rotation = Quaternion.Euler(0, 0, Random.Range(0, 360));
                avoidPoints.Add(bgCordinates[random]);
            }
        }
    }

    void Start() {

        List<Vector2> avoidPoints = new List<Vector2>();
        foreach (Vector2 i in cordinates) {
            //spawn other blocks
            int random = Random.Range(0, blocks.Length);
            while(blocks[random].tag == "spike" && blocks[previousRandom].tag == "spike") {
                random = Random.Range(0, blocks.Length);
                if (blocks[random].tag != "spike") {
                    previousRandom = random;
                }
            }
            if (i == new Vector2(2, 4)) {
                GameObject spawn = Instantiate(spawnBlock, new Vector2(2, 4),  Quaternion.identity);
                Instantiate(player, new Vector2(2, 6), Quaternion.identity);
                GameObject end = Instantiate(endBlock, new Vector2(2, -4),  Quaternion.identity);
                avoidPoints.Add(new Vector2(2, 4));
                avoidPoints.Add(new Vector2(2, -4));
            }
            if (!avoidPoints.Contains(i)) {
                GameObject block = Instantiate(blocks[random], i,  Quaternion.identity);
            }
        }
    }

    void Update() {
        timer -= Time.deltaTime;

        timerUI.text = ((int)timer).ToString();
        gameOverTimeResult.text = "Time: " + ((int)(60 - timer)).ToString();
        bLocksToDestroy = FindObjectsOfType<Blocks>();
        if (timer <= 0) {
            GameOverUI.gameObject.SetActive(true);
            timerUI.gameObject.SetActive(false);
            deathCount.gameObject.SetActive(false);
            skull.gameObject.SetActive(false);
            foreach (Blocks i in bLocksToDestroy) {
                Destroy(i.gameObject);
            }
            Time.timeScale = 0;
        }
    }

    public void changeLevel() {
        spikeCount = 0;
        switch (nextLevel) {
            case 1:
                cordinates.Clear();
                cordinates = cordinates1;
                nextLevel++;
                break;
            case 2:
                cordinates.Clear();
                cordinates = cordinates2;
                nextLevel++;
                break;
            case 3:
                cordinates.Clear();
                cordinates = cordinates3;
                nextLevel++;
                break;
            case 4:
                cordinates.Clear();
                cordinates = cordinates4;
                nextLevel++;
                break;
            case 5:
                cordinates.Clear();
                cordinates = cordinates5;
                nextLevel++;
                break;
            case 6:
                cordinates.Clear();
                cordinates = cordinates6;
                nextLevel++;
                break;
            default:
                nextLevel++;
                break;
        }

        Vector2 startingPoint1 = new Vector2(-2, 4);
        Vector2 startingPoint2 = new Vector2(2, 4);
        Vector2 finishingPoint1 = new Vector2(-2, -4);
        Vector2 finishingPoint2 = new Vector2(2, -4);
        List<Vector2> avoidPoints = new List<Vector2>();
        if (nextLevel <= 7) {
            foreach (Vector2 i in cordinates) {
                int random = Random.Range(0, blocks.Length);
                if (blocks[random].tag == "spike") {
                    if (spikeCount > nextLevel) {
                        random = Random.Range(0, blocks.Length);
                    } else {
                        spikeCount++;
                    }
                } 
                if (cordinates.Contains(startingPoint1) && i == startingPoint1) {
                    GameObject spawn = Instantiate(spawnBlock, startingPoint1,  Quaternion.identity);
                    GameObject end = Instantiate(endBlock, finishingPoint2,  Quaternion.identity);
                    avoidPoints.Add(startingPoint1);
                    avoidPoints.Add(finishingPoint2);
                } else if (!cordinates.Contains(startingPoint1) && i == startingPoint2) {
                    GameObject spawn = Instantiate(spawnBlock, startingPoint2,  Quaternion.identity);
                    avoidPoints.Add(startingPoint2);
                    if (cordinates.Contains(finishingPoint1)) {
                        GameObject end = Instantiate(endBlock, finishingPoint1,  Quaternion.identity);
                        avoidPoints.Add(finishingPoint1);
                    } else {
                        GameObject end = Instantiate(endBlock, finishingPoint2,  Quaternion.identity);
                        avoidPoints.Add(finishingPoint2);
                    }
                } else if (!avoidPoints.Contains(i)) {
                    GameObject bLock = Instantiate(blocks[random], i,  Quaternion.identity);
                }
            }
        } else {
            GameOverUI.gameObject.SetActive(true);
            timerUI.gameObject.SetActive(false);
            deathCount.gameObject.SetActive(false);
            skull.gameObject.SetActive(false);
            foreach (Blocks i in bLocksToDestroy) {
                Destroy(i.gameObject);
            }
            Time.timeScale = 0;
        }
    }
    public void Particle(Vector2 position, Quaternion rotation) {
        Instantiate(explosion, position, rotation);
    }
 }
