using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Platform : MonoBehaviour
{
    public float jumpForce = 10f;
    public float boostedJumpForce = 20f;
    public GameManager gameManager;
    float force;
    BoxCollider2D box;

    private void Awake()
    {
        gameManager = FindObjectOfType<GameManager>();
        box = GetComponent<BoxCollider2D>();
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.relativeVelocity.y <= 0f)
        {
            Rigidbody2D rb = collision.gameObject.GetComponent<Rigidbody2D>();
            if (rb != null) 
            {
                if (gameObject.tag != "Tornado") {
                    gameManager.smashing = false;
                    gameManager.canSmash = false;
                    Vector2 velocity = rb.velocity;
                    velocity.y = force;
                    rb.velocity = velocity;
                    if (gameObject.tag == "PlatformCracked") 
                    {
                        gameObject.SetActive(false);
                    } 
                    else if (gameObject.tag == "PlatformDanger") 
                    {
                        collision.gameObject.SetActive(false);
                        gameManager.playerDied = true;
                    }
                }
            }
        }
    }

    private void Update() {
        if (gameManager.smashing) {
            if (gameObject.tag == "PlatformCracked") 
            {
                box.isTrigger = true;
            } 
            force = boostedJumpForce;
        }
        else {
            if (gameObject.tag == "PlatformCracked") 
            {
                box.isTrigger = false;
            }
            force = jumpForce;
        }
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.tag == "Barier") 
        {
            gameManager.spawnPosition.y += Random.Range(gameManager.platformRangeVertical.x, gameManager.platformRangeVertical.y);
            gameManager.spawnPosition.x = Random.Range(gameManager.platformRangeHorizontal.x, gameManager.platformRangeHorizontal.y);
            while (gameManager.randomSprite == gameManager.previusRandom) {
                gameManager.randomSprite = (int) Random.Range(0, gameManager.platformSprites.Length);
            }
            if (gameManager.platformSprites[gameManager.previusRandom].tag == "PlatformCracked" || gameManager.platformSprites[gameManager.previusRandom].tag == "Tornado") {
                while (gameManager.platformSprites[gameManager.randomSprite].tag == "PlatformDanger" || gameManager.platformSprites[gameManager.randomSprite].tag == "Tornado") {
                    gameManager.randomSprite = (int) Random.Range(0, gameManager.platformSprites.Length);
                }
            }
            Instantiate(gameManager.platformSprites[gameManager.randomSprite], gameManager.spawnPosition, Quaternion.identity);
            gameManager.previusRandom = gameManager.randomSprite;
            Destroy(gameObject);
        }
        if (gameObject.tag == "PlatformCracked") 
        {
            gameObject.SetActive(false);
        } 
    }
}
