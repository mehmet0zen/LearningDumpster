 
 //SITE PASSWORD
var password = "ilovecoding";
var passwordPopup = prompt("Please enter the password", "");
if (passwordPopup == null) {
  window.open("/Users/mehmetozen/Developer/WebDev/Coding Class/index.html", "_self")
}
while (passwordPopup.toLowerCase() != password) {
  window.alert("!INCORRECT!");
  passwordPopup = prompt("Please enter the correct password", "");
  if (passwordPopup == null) {
    window.open("/Users/mehmetozen/Developer/WebDev/Coding Class/index.html", "_self")
  }
}
var storedItem = localStorage.getItem("storedItem");

  const POST = {
    submit: document.getElementById('post-button'),
    devName: document.getElementById('dev'),
    projectLink: document.getElementById('project-link'),
    grade: document.getElementById('student-grade')
  };

  function eventListeners() {
    POST.projectLink.addEventListener("keyup", RetryPreview);
    POST.devName.addEventListener("keyup", can_submit);
  }
  eventListeners();
  let cansubmit = false;
  function can_submit() {
    let submit = POST.submit.value.trim();
    let projectLink = POST.projectLink.value.trim();
    let devName = POST.devName.value.trim();
    if (projectLink.length > 5 && devName.length > 4) {
      POST.submit.classList.remove('disable');
      submit.disabled = false;
      cansubmit = true;
    } else {
      POST.submit.classList.add('disable');
      submit.disabled = true;
      cansubmit = false;
    }
  }
  var allposts = [];

  POST.submit.addEventListener("click", function submitClicked(e) {
    // e.preventDefault();
    if (cansubmit) {
      let post = {
        link : POST.projectLink.value.trim(),
        developer : POST.devName.value.trim(),
        grade : POST.grade.value.trim(),
        projectID : POST.projectLink.value.replace('https://makecode.com/','')
      }
      let posts = document.getElementById('projects');
      posts.innerHTML += '<div class="skills post"><div style="margin:auto;"><h4 style="margin-top:auto;">' + post.developer + '</h3><a style="color:#5380fc;" href="' + POST.projectLink.value + '">link</a></div><div style="position:relative;width:200px;height:220px;overflow:hidden;margin-left:10%;margin-bottom:5%;"><iframe style="position:absolute;top:0;left:0;width:100%;height:100%;"src="https://arcade.makecode.com/---run?id=' + post.projectID + '" allowfullscreen="allowfullscreen" sandbox="allow-popups allow-forms allow-scripts allow-same-origin"frameborder="0"></iframe></div></div>';
      allposts.push(post);
      localStorage.setItem("storedItem", allposts);
      console.log(allposts);
      POST.projectLink.value = '';
      POST.devName.value = '';
      POST.grade.value = 1;
      document.getElementById('preview-hidden').classList.add('hidden');
      POST.submit.classList.add('disable');
      cansubmit = false;
    }
  });
  
  function getData() {
    console.log(storedItem);
  }

  function RetryPreview() {
    can_submit();
    document.getElementById('preview-hidden').classList.remove('hidden');
    var projectID = document.getElementById('project-link').value.replace('https://makecode.com/','');
    var source = document.getElementById('preview-game');
    var src = 'https://arcade.makecode.com/---run?id=' + projectID;

    source.src = src;
  }
