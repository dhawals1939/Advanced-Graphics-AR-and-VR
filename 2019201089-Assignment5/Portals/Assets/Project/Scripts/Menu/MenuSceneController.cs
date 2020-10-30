using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MenuSceneController : MonoBehaviour {

	public void OnPlay () {
		LevelManager.Instance.LoadFirstLevel ();
	}
}
