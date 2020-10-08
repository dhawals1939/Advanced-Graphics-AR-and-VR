const Student = {
  // please fill in your name and NetID
  // your NetID is the part of your email before @princeton.edu
  name: "thesigmaguy",
  netID: "2019201089",
};

Student.updateHTML = function() {
  const studentInfo = this.name + " &lt;" + this.netID + "&gt;";
  document.getElementById("student").innerHTML = studentInfo;
};
