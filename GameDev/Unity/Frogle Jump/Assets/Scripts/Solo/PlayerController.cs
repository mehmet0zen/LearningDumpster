using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Audio;
using System.Collections;

public class PlayerController : MonoBehaviour
{
    public float moveSpeed = 45f;
    public float smashSpeed = 30f;
    public float smashDelay = 2;
    public GameManager gameManager;
    public Rigidbody2D rb;
    public Animator anim;
    Vector2 xValue;
    int scoreNum;
    float countDown = 0; //for smash delay

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        SetScore();
        //Animation
        Animations();

        if (!gameManager.canSmash) {
            countDown += Time.deltaTime;
            if (countDown >= smashDelay) {
                gameManager.canSmash = true;
                countDown = 0;
            }
        }
    }

    private void FixedUpdate()
    {
        xValue.x = Input.GetAxis("Horizontal");
        // Tilt();
        if (!gameManager.smashing) {
            Run();
        } else {
            //Smash
            rb.velocity = new Vector2(0, -1 * Mathf.Pow(smashSpeed, 2) * Time.deltaTime);
        }
    }

    //Run
    void Run() {
        rb.velocity = new Vector2(xValue.x * Mathf.Pow(moveSpeed, 2) * Time.deltaTime, rb.velocity.y);
    }

    //Tilt for mobile
    void Tilt() {
        float movement = Input.acceleration.x;
            xValue.x = movement;
    }

    //Smash
    void OnSmashDown() {
        if (gameManager.canSmash) { 
            gameManager.smashing = true;
            gameManager.canSmash = false;
        }
    }
    
    //Score
    void SetScore() {
        scoreNum = (int) gameManager.mainCamera.gameObject.transform.position.y;
        gameManager.score.text = scoreNum.ToString();
        gameManager.gameOverScore.text = scoreNum.ToString();

        if (scoreNum > PlayerPrefs.GetInt("HighScore", 0)) { 
            gameManager.score.color = Color.green;
            gameManager.gameOverScore.color = Color.green;
            gameManager.gg.color = Color.green;
            gameManager.gg.text = "New\nRecord!!";
            if (gameManager.playerDied) {
                PlayerPrefs.SetInt("HighScore", scoreNum);
            }
        }
    }

    //Animations
    void Animations() {
        if (rb.velocity.y < -0.1) {
            anim.SetBool("jumping", false);
        } 
        else if (rb.velocity.y > -0.1 && !gameManager.smashing){
            anim.SetBool("jumping", true);
        }
        anim.SetBool("smashing", gameManager.smashing);
    }

    //Dying and teleporting
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.tag == "Barier") 
        {
            gameManager.playerDied = true;
            gameObject.SetActive(false);
        }
        if (collision.tag == "BarierR" && xValue.x > 0)
        {
            transform.position = new Vector2(transform.position.x * -1, transform.position.y);
        }
        else if (collision.tag == "BarierL" && xValue.x < 0) 
        {
            transform.position = new Vector2(transform.position.x * -1, transform.position.y);
        }
    }
}
