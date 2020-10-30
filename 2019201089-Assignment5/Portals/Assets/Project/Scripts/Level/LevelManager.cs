using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class LevelManager {

	private static LevelManager instance;
	public static LevelManager Instance {
		get {
			if (instance == null) {
				instance = new LevelManager ();
			}
			return instance;
		}
	}

	private int level;

	private const int MAXIMUM_LEVEL = 2;

	public void LoadFirstLevel () {
		level = 1;
		SceneManager.LoadScene ("Level" + level);
	}

	public void LoadNextLevel () {
		level++;

		if (level <= MAXIMUM_LEVEL) {
			SceneManager.LoadScene ("Level" + level);
		} else {
			SceneManager.LoadScene ("Menu");
		}
	}
}
