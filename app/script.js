const btnTab = document.getElementById('top-bar')
const tabContainer = document.getElementById('tab-container')
var package = null
var item = null

// UI FUNCTIONS

function setTab(tabID) {
  [...btnTab.children].forEach(function(x,y){
    if (y == tabID+1)
      x.classList.add('active')
    else
      x.classList.remove('active')
  });
  [...tabContainer.children].forEach(function(x,y){
    if (y == tabID) {
      if (x.getAttribute('data-onTabbed'))
        eval(x.getAttribute('data-onTabbed'))
        //eval is bad, but I can't execute a string.
      x.classList.add('active')
    }
    else
      x.classList.remove('active')
  })
}

function updateTabsAvailable() {
  let btns = btnTab.children.filter(function(x){return x.nodeName == 'BUTTON'})
  for (let btn in btns) {
    console.log(btnTab.children[btn])
    if (btnTab.children[btn].getAttribute('data-required'))
      btnTab.children[btn].disabled = eval(btnTab.children[btn].getAttribute('data-required'))
  }
}

// TEMPORARY DEFINITIONS

function loadPackageList() {
  return [examplePkg,examplePkg2]
}

var examplePkg = {
  "title":"gaming",
  "description":"gaming",
  "items":[

  ]
}

var examplePkg2 = {
  "title":"gaming",
  "description":"gaming",
  "items":[

  ]
}

// TAB SETUP EVENTS

function tab0_browser_setup() {
  const pkgBrowserElement = document.getElementById('tab0-package-browser')
  pkgBrowserElement.innerHTML = ''
  const packages = loadPackageList()
  for (let pkg in packages) {
    pkgBrowserElement.innerHTML += `<li data-index="${pkg}" onclick="tab0_set_active_package(this)">${packages[pkg].title}</li>`
  }
}

function tab0_browser_reset() {
  package = null
  tab0_browser_setup()
  updateTabsAvailable()
}

function tab0_set_active_package(e) {
  const packageEls = [...$('#tab0-package-browser li.active')]
  if (packageEls.length)
    packageEls[0].classList.remove('active')
  e.classList.add('active')
  updateTabsAvailable()
}

//$('#tab-package-browser ul li').on('click',(x)=>{console.log(x.getAttribute('filename'))})



// APP LAUNCH EVENTS

tab0_browser_reset()
