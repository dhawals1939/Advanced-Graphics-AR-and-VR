using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Door : TriggableObject {

	public GameObject doorTop;
	public GameObject doorBottom;
	public float openedHeightTop;
	public float openedHeightBottom;
	public float speed = 3f;

	private Vector3 targetPositionTop;
	private Vector3 targetPositionBottom;

	// Use this for initialization
	void Start () {
		targetPositionTop = Vector3.zero;
		targetPositionBottom = Vector3.zero;
	}
	
	// Update is called once per frame
	void Update () {
		doorTop.transform.localPosition = Vector3.Lerp (doorTop.transform.localPosition, targetPositionTop, Time.deltaTime * speed);
		doorBottom.transform.localPosition = Vector3.Lerp (doorBottom.transform.localPosition, targetPositionBottom, Time.deltaTime * speed);
	}

	public override void OnTrigger () {
		base.OnTrigger ();

		targetPositionTop = new Vector3 (0, openedHeightTop, 0);
		targetPositionBottom = new Vector3 (0, openedHeightBottom, 0);
	}

	public override void OnUntrigger () {
		base.OnUntrigger ();

		targetPositionTop = Vector3.zero;
		targetPositionBottom = Vector3.zero;
	}
}
