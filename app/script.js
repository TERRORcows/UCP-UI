const btnTab = document.getElementById('top-bar')
const tabContainer = document.getElementById('tab-container')
var packages = []
var package = null
var item = null

// ------------ UI FUNCTIONS ------------

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

function updateButtonsAvailable() {
  //.filter(function(x){return x.nodeName == 'BUTTON'})
  [...$('button')].forEach((btn)=>{
    if (btn.getAttribute('data-required'))
      btn.disabled = !eval(btn.getAttribute('data-required'))
  })
}

// ------------ TEMPORARY DEFINITIONS ------------

async function loadPackageList() {
  packages = await eel.loadPackageList()()
  return packages
}

// ------------ TAB SETUP EVENTS ------------

// TAB 0

async function tab0_browser_setup() {
  const pkgBrowserElement = document.getElementById('tab0-package-browser')
  pkgBrowserElement.innerHTML = ''
  await loadPackageList()
  for (let pkgRAW in packages) {
    let pkg = (packages[pkgRAW])
    pkgBrowserElement.innerHTML += `<li data-pkgid="${pkg.id}" onclick="tab0_set_active_package(this)">${pkg.title}</li>`
  }
}

function tab0_browser_reset() {
  package = null
  item = null
  tab0_browser_setup()
  updateButtonsAvailable()
}

function tab0_set_active_package(e) {
  const packageEls = [...$('#tab0-package-browser li.active')]
  if (packageEls.length)
    packageEls[0].classList.remove('active')
  e.classList.add('active')
  package = packages.filter((x)=>{return x.id == e.getAttribute('data-pkgid')})[0]
  tab1_load_data()
  updateButtonsAvailable()
}

// TAB 1

function tab1_load_data() {
  // fill in forms
  [...$('#tab-package input')].forEach((el)=>{
    if (el.getAttribute('data-packagedata'))
      el.value = eval(el.getAttribute('data-packagedata'))
      // Yes, yes. Eval is terrible. I don't know how to do it otherwise.
  })
  // item list
  let itemlist = $('#item-list ul')[0]
  itemlist.innerHTML = ''
  Object.keys(package.items).forEach((itmRAW)=>{
    let itm = package.items[itmRAW]
    itemlist.innerHTML += `<li data-itemid="${itm.id}" onclick="tab1_set_active_item(this)">${itm.title}<img src="#" style="float: right;"></li>`
  })
  item = null
}

function savePackageAttributes() {
  [...$('#tab-package input')].forEach((el)=>{
    if (el.getAttribute('data-packagedata'))
      eval(el.getAttribute('data-packagedata')+' = el.value')
      // jesus fucking christ this is an abomination
  })
  eel.savePackage(package,package.filename)()
}

function tab1_set_active_item(e) {
  const itemEls = [...$('#item-list li.active')]
  if (itemEls.length)
    itemEls[0].classList.remove('active')
  e.classList.add('active')
  item = package.items.filter((x)=>{return x.id == e.getAttribute('data-itemid')})[0]
  updateButtonsAvailable()
}

// TAB 2

function tab2_load_data() {
  // fill in forms
  [...$('#tab-item input')].forEach((el)=>{
    if (el.getAttribute('data-itemdata'))
      el.value = eval(el.getAttribute('data-itemdata'))
      // Yes, yes. Eval is terrible. I don't know how to do it otherwise.
  })
}

function saveCurrentItem() {
  [...$('#tab-item input')].forEach((el)=>{
    if (el.getAttribute('data-itemdata'))
      eval(el.getAttribute('data-itemdata')+' = el.value')
      // jesus fucking christ this is an abomination
  })
  package.items.filter((x)=>{x.id == item.id})[0] = item
  console.log(package.items)
  eel.savePackage(package,package.filename)()
}

//$('#tab-package-browser ul li').on('click',(x)=>{console.log(x.getAttribute('filename'))})



// APP LAUNCH EVENTS

tab0_browser_reset()
