using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Orb : MonoBehaviour {

	public float speed = 100f;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		transform.RotateAround (transform.position, Vector3.up, speed * Time.deltaTime);
		transform.RotateAround (transform.position, Vector3.right, speed * Time.deltaTime);
		transform.RotateAround (transform.position, Vector3.forward, speed * Time.deltaTime);
	}
}
