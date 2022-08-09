using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class playerController : MonoBehaviour
{
    public AudioClip explosion;
    public AudioClip blip;
    public AudioSource source;
    Rigidbody2D rb;
    float velocity;
    GravityControlll gc;
    LevelCreator lc;
    List<Blocks> blocks = new List<Blocks>();
    public LayerMask blockLayers;
    public LayerMask spikeLayers;
    public float moveSpeed = 50;
    public float jumpForce = 5;
    public BoxCollider2D boxCollider;
    public LayerMask ground;
    public Animator animator;
    cameraFollow cam;
    Vector2 raycastDir;
    int died = 0;
    bool facingRight = false;
    int succesCount = 0;
    private void Awake() {
        source = GetComponent<AudioSource>();
        rb = GetComponent<Rigidbody2D>();
        gc = GetComponent<GravityControlll>();
        lc = FindObjectOfType<LevelCreator>();
        cam = FindObjectOfType<cameraFollow>();
        animator = GetComponent<Animator>();
    }

    private void Update() {
        if (Input.GetKey(KeyCode.A) && !Input.GetKey(KeyCode.D)) {
            velocity = -1;
            animator.SetBool("Walking", true);
            gameObject.transform.eulerAngles = new Vector3(0, 0, 0);
            facingRight = false;
        } else if (Input.GetKey(KeyCode.D) && !Input.GetKey(KeyCode.A)) {
            velocity = 1;
            animator.SetBool("Walking", true);
            gameObject.transform.eulerAngles = new Vector3(0, 180, 0);
            facingRight = true;
        } 
        
        if ((!Input.GetKey(KeyCode.D) && !Input.GetKey(KeyCode.A)) || (Input.GetKey(KeyCode.A) && Input.GetKey(KeyCode.D))) {
            velocity = 0;
            animator.SetBool("Walking", false);
            gameObject.transform.eulerAngles = new Vector3(0, facingRight ? 180 : 0, 0);
        }

        if (!IsGrounded()) {
            animator.SetBool("Jumping", true);
            animator.SetBool("Walking", false);
        } else {
            animator.SetBool("Jumping", false);
        }

        if (Finished()) {
            succesCount++;
            source.clip = blip;
            source.Play(0);
            lc.level[lc.nextLevel - 2].succeded = true;
            lc.level[lc.nextLevel - 2].successColor = lc.lvlBgs[lc.nextLevel - 2].color;
            lc.lvlBgs[lc.nextLevel - 2].gameObject.SetActive(true);
            foreach (Blocks i in lc.bLocksToDestroy) {
                if (i.gameObject.tag != "BorderSpikes") {
                    Destroy(i.gameObject);
                }
            }
            MoveToTheSpawner();
            lc.changeLevel();
        }
        if (Death()) {
            died++;
            source.clip = explosion;
            source.Play(0);
            lc.level[lc.nextLevel - 2].failed = true;
            lc.Particle(transform.position, Quaternion.Euler(cam.angle));
            foreach (Blocks i in lc.bLocksToDestroy) {
                if (i.gameObject.tag != "BorderSpikes") {
                    Destroy(i.gameObject);
                }
            }
            MoveToTheSpawner();
            lc.changeLevel();
        }

        if (SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Game")) {
            lc.gameOverSuccesResult.text = "Succes: " + succesCount.ToString();
            lc.gameOverDeathResult.text = "Died: " + died.ToString();

            if (lc.nextLevel > 7) {
                Destroy(gameObject);
            }
        }
    }

    void FixedUpdate()
    {
        if (Input.GetKey(KeyCode.W) && IsGrounded()) {
            if (gc.gDirection == GravityControlll.GravityDirection.Down) {
                rb.velocity = Vector2.up * jumpForce;
            } else if (gc.gDirection == GravityControlll.GravityDirection.Up) {
                rb.velocity = Vector2.down * jumpForce;
            } else if (gc.gDirection == GravityControlll.GravityDirection.Left) {
                rb.velocity = Vector2.right * jumpForce;
            } else if (gc.gDirection == GravityControlll.GravityDirection.Right) {
                rb.velocity = Vector2.left * jumpForce;
            }
        } 

        if (gc.gDirection == GravityControlll.GravityDirection.Down) {
            raycastDir = Vector2.down;
            rb.velocity = new Vector2(velocity * moveSpeed * Time.deltaTime, rb.velocity.y); 
        } else if (gc.gDirection == GravityControlll.GravityDirection.Up) {
            raycastDir = Vector2.up;
            rb.velocity = new Vector2(-velocity * moveSpeed * Time.deltaTime, rb.velocity.y); 
        } else if (gc.gDirection == GravityControlll.GravityDirection.Left) {
            raycastDir = Vector2.left;
            rb.velocity = new Vector2(rb.velocity.x, -velocity * moveSpeed * Time.deltaTime); 
        } else if (gc.gDirection == GravityControlll.GravityDirection.Right) {
            raycastDir = Vector2.right;
            rb.velocity = new Vector2(rb.velocity.x, velocity * moveSpeed * Time.deltaTime); 
        }
        if (SceneManager.GetActiveScene() == SceneManager.GetSceneByName("Game")) {
            if (died > 0) {
                lc.skull.gameObject.SetActive(true);
                lc.deathCount.text = died.ToString();
            } else {
                lc.skull.gameObject.SetActive(false);
            }
        }
    }

    public bool IsGrounded() {
        float extraHight = 0.2f;
        RaycastHit2D raycastHit = Physics2D.Raycast(boxCollider.bounds.center, raycastDir, boxCollider.bounds.extents.y + extraHight, ground);

        //Debugging
        Color raycastColor;
        if (raycastHit.collider != null) {
            raycastColor = Color.green;
        } else {
            raycastColor = Color.red;
        }
        Debug.DrawRay(boxCollider.bounds.center, raycastDir * (boxCollider.bounds.extents.y + extraHight), raycastColor);
        return raycastHit.collider != null;
    }

    public bool Finished() {
        float extraHight = 0.2f;
        RaycastHit2D raycastHit = Physics2D.Raycast(boxCollider.bounds.center, raycastDir, boxCollider.bounds.extents.y + extraHight, LayerMask.GetMask("finish"));
        return raycastHit.collider != null;
    }
    public bool Death() {
        float extraHight = 0.2f;
        RaycastHit2D raycastHit = Physics2D.Raycast(boxCollider.bounds.center, raycastDir, boxCollider.bounds.extents.y + extraHight, spikeLayers);
        return raycastHit.collider != null;
    }
    

    void MoveToTheSpawner() {
        gameObject.transform.position = new Vector3(-2, 6, 0);
        gc.gDirection = GravityControlll.GravityDirection.Down;
    }

}
