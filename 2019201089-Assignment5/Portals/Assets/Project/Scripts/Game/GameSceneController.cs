using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameSceneController : MonoBehaviour {

	[Header("Game")]
	public Player player;

	[Header("UI")]
	public Text instructionText;
	public Text timeText;
	public Text endGameText;

	private bool endedLevel;
	private float gameTimer;
	private float endGameTimer = 5f;

	// Use this for initialization
	void Start () {
		endGameText.gameObject.SetActive (false);

		player.onCollectOrb = OnCollectOrb;
	}
	
	// Update is called once per frame
	void Update () {
		// Update the game timer.
		if (endedLevel == false) {
			gameTimer += Time.deltaTime;
			timeText.text = "Time: " + Mathf.FloorToInt (gameTimer) + "s";
		} else {
			endGameTimer -= Time.deltaTime;
			if (endGameTimer <= 0f) {
				LevelManager.Instance.LoadNextLevel ();
			}
		}
	}

	private void OnCollectOrb () {
		endedLevel = true;

		// Show the end game message.
		instructionText.gameObject.SetActive (false);
		timeText.gameObject.SetActive (false);
		endGameText.gameObject.SetActive (true);

		endGameText.text = "Well done!\nYour time: " + Mathf.FloorToInt (gameTimer) + "s";
	}
}
