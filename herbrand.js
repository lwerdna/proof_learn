//------------------------------------------------------------------------------
// herbrand.js
//------------------------------------------------------------------------------

var name = 'main';
var proof = makeproof();var proofs = seq();
proofs['main'] = proof;var clipboard = makeproof();
//------------------------------------------------------------------------------
// doinitialize
//------------------------------------------------------------------------------

function doinitialize ()
 {proof = archivetoproof(document.getElementsByTagName('proof')[0]);
  showproof(proof)}
function archivetoproof (archive)
 {var proof = seq('proof');
  stepnumber = 0;
  for (var i=1; i<archive.childNodes.length; i++)
      {if (archive.childNodes[i].nodeName==='STEP')
          {stepnumber = stepnumber + 1;
           var step = archivetostep(stepnumber,archive.childNodes[i]);
           proof[proof.length] = step}};
  return proof}

function archivetostep (n,archive)
 {var sentence = getsubnode(archive,'SENTENCE').textContent;
  var justification = getsubnode(archive,'JUSTIFICATION').textContent;
  var step = seq('step',n,read(sentence),justification);
  for (var i=0; i<archive.childNodes.length; i++)
      {if (archive.childNodes[i].nodeName==='ANTECEDENT')
          {step[step.length] = archive.childNodes[i].textContent*1}};
  return step};

function getsubnode (node,tag)
 {for (var i=0; i<node.childNodes.length; i++)
      {if (node.childNodes[i].nodeName===tag) {return node.childNodes[i]}};
  return false}

//------------------------------------------------------------------------------
// showproof
//------------------------------------------------------------------------------

function showproof (proof)
 {var area = document.getElementById('proof');
  var n = area.childNodes.length;
  for (var i=0; i<n; i++) {area.removeChild(area.childNodes[0])};
  area.appendChild(displayproof(proof));
  showsignature();
  showbuttons()}

function displayproof (proof) {var table = document.createElement('table');
  table.setAttribute('width','640');
  table.setAttribute('cellpadding','0');
  table.setAttribute('cellspacing','0');
  table.setAttribute('border','0');
  displayfirst(1,table);
  displaysteps(1,proof,table);
  displayempty(prooflevel(proof),table);
  return table}

function displaysteps (level,proof,table) {for (var i=1; i<proof.length; i++)      {if (proof[i][3]==='Assumption') {level=level+1};
       if (proof[i][3]==='Implication Introduction') {level=level-1};
       displaystep(level,proof[i],table)};
  return true}

function displaystep (level,item,table) {var row = table.insertRow(table.rows.length);
  row.setAttribute('height','30');
  var cell = row.insertCell(0);
  cell.setAttribute('width',20);
  var widget = document.createElement('input');
  widget.setAttribute('id',item[1]);
  widget.setAttribute('type','checkbox');
  cell.appendChild(widget);
  cell = row.insertCell(1);
  cell.setAttribute('width',24);
  cell.innerHTML = item[1] + '.';
  cell = row.insertCell(2);
  cell.setAttribute('width',380);
  cell.appendChild(displaybarredelement(level,grind(item[2])));
  cell = row.insertCell(3);
  cell.setAttribute('width',216);
  var just = '&nbsp;' + item[3];
  if (item.length > 4)     {just += ': ' + item[4];      for (var j=5; j<item.length; j++) {just += ', ' + item[j]}};
  cell.innerHTML = just;
  return true}

function displayfirst (level,table) {var row = table.insertRow(table.rows.length)
  row.setAttribute('height','30');
  var cell = row.insertCell(0);
  cell.setAttribute('width',20);
  var widget = document.createElement('input');
  widget.setAttribute('type','checkbox');
  widget.setAttribute('onChange','doselectall(this)');
  cell.appendChild(widget);  
  cell = row.insertCell(1);
  cell.setAttribute('width',20);
  cell = row.insertCell(2);
  cell.setAttribute('width',400);
  cell.appendChild(displaybarredelement(level,'<span style="color:#888888">Select All</span>'));
  cell = row.insertCell(3);
  cell.setAttribute('width',200);
  return true}

function displayempty (level,table) {var row = table.insertRow(table.rows.length)
  row.setAttribute('height','30');
  var cell = row.insertCell(0);
  cell.setAttribute('width',20);
  cell = row.insertCell(1);
  cell.setAttribute('width',20);
  cell = row.insertCell(2);
  cell.setAttribute('width',400);
  cell.appendChild(displaybarredelement(level,''));
  cell = row.insertCell(3);
  cell.setAttribute('width',200);
  return true}

function displaybarredelement (level,stuff)
 {var table = document.createElement('table');
  table.setAttribute('cellspacing','0');
  table.setAttribute('cellpadding','0');
  var row = table.insertRow(0);
  row.setAttribute('height','30');
  for (var i=level; i>0; i--)
      {var cell = row.insertCell(row.cells.length);
       cell.setAttribute('style','border-left:2px solid #000000;padding:5px');
       cell.innerHTML = '&nbsp;'};
  var cell = row.insertCell(row.cells.length);
  cell.innerHTML = stuff;
  cell = row.insertCell(1);
  cell.innerHTML = '&nbsp;';
  return table}

function prooflevel (proof)
 {var level = 1;
  for (var i=1; i<proof.length; i++)
      {if (proof[i][3]==='Assumption') {level=level+1};
       if (proof[i][3]==='Implication Introduction') {level=level-1}};
  return level}

//------------------------------------------------------------------------------
// showsignature
//------------------------------------------------------------------------------

function showsignature ()
 {objectconstants = getobjectconstants(proof);
  functionconstants = getfunctionconstants(proof);
  var area = document.getElementById('objects');
  var n = area.childNodes.length;
  for (var i=0; i<n; i++) {area.removeChild(area.childNodes[0])};
  area.innerHTML = renderconstants(objectconstants);
  area = document.getElementById('functions');
  var n = area.childNodes.length;
  for (var i=0; i<n; i++) {area.removeChild(area.childNodes[0])};
  area.innerHTML = renderconstants(functionconstants);
  return true}

function renderconstants (constants)
 {var exp = '';
  if (constants.length>0) {exp = constants[0]};
  for (var i=1; i<constants.length; i++)
      {exp += ', ' + constants[i]};
  return exp}

//------------------------------------------------------------------------------
// showbuttons
//------------------------------------------------------------------------------

function showbuttons ()
 {objectconstants = getobjectconstants(proof);
  functionconstants = getfunctionconstants(proof);
  if (objectconstants.length===0 && functionconstants.length===0)
     {document.getElementById('dodc').disabled=true;
      document.getElementById('doind').disabled=true};
  if (objectconstants.length>0 && functionconstants.length===0)
     {document.getElementById('dodc').disabled=false;
      document.getElementById('doind').disabled=true}
  if (functionconstants.length>0)
     {document.getElementById('dodc').disabled=true;
      document.getElementById('doind').disabled=false}

  if (prooflevel(proof)===1)
     {document.getElementById('dopremise').disabled=false;
      document.getElementById('doii').disabled=true;
      return true};
  document.getElementById('dopremise').disabled=true;
  document.getElementById('doii').disabled=false;

  return true}

//------------------------------------------------------------------------------
// Step Operations
//------------------------------------------------------------------------------
function dorestore (node)
 {proofs[name] = proof;
  name = node.value;
  proof = proofs[name];
  showproof(proof);
  return true}

//------------------------------------------------------------------------------

function donew ()
 {proofs[name] = proof;
  var current = document.getElementById('current');
  name = prompt('Proof name:');
  proof = makeproof();  proofs[name] = proof;
  var option = document.createElement("option");
  option.text = name;
  current.add(option);
  current.value = name;
  showproof(proof);
  return true}

//------------------------------------------------------------------------------

function doremove ()
 {if (name==='main') {alert('Cannot remove main proof.'); return false};
  if (!confirm('Remove proof ' + name + '?')) {return false};
  var current = document.getElementById('current');
  current.value = name;
  current.remove(current.selectedIndex);
  current.value = 'main';
  proof = proofs['main'];
  showproof(proof);
  return true}

//------------------------------------------------------------------------------

function docopy ()
 {clipboard = deepcopy(proof);
  alert('Proof copied to clipboard.')
  return true}

//------------------------------------------------------------------------------

function dopaste ()
 {proof = deepcopy(clipboard);
  showproof(proof);
  return true}

//------------------------------------------------------------------------------
// Select all
//------------------------------------------------------------------------------

function doselectall (node) {var parity = node.checked;
  for (var i=1; i<proof.length; i++)
      {document.getElementById(i).checked = parity};
  return true}//------------------------------------------------------------------------------
// dopremise
//------------------------------------------------------------------------------
function dopremise () {document.getElementById('premise').style.display = ''}function addpremise () {var exp = read(document.getElementById('newpremise').value);
  if (exp==='error') {alert('Syntax error'); return false};  document.getElementById('premise').style.display = 'none';  proof[proof.length] = makestep(proof.length,exp,'Premise');  showproof(proof)}function unpremise () {document.getElementById('premise').style.display = 'none'}//------------------------------------------------------------------------------
// doassumption
//------------------------------------------------------------------------------
function doassumption () {document.getElementById('assumption').style.display = ''}function addassumption () {var exp = read(document.getElementById('newassumption').value);  if (exp==='error') {alert('Syntax error'); return false};  document.getElementById('assumption').style.display = 'none';
  proof[proof.length] = makestep(proof.length,exp,'Assumption');  showproof(proof)}function unassumption () {document.getElementById('assumption').style.display = 'none'}//------------------------------------------------------------------------------
// doreiteration
//------------------------------------------------------------------------------

function doreiteration ()
 {var steps = getcheckedpremises(proof);
  if (steps.length===0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {proof[proof.length]=makestep(proof.length,proof[steps[i]][2],'Reiteration',steps[i])};  showproof(proof);  return true}

function getcheckedstep (proof)
 {for (var i=1; i<proof.length; i++)      {if (document.getElementById(proof[i][1]).checked) {return i}};
  return false}

function getcheckedpremises (proof)
 {var assumptions = getassumptions(proof);
  var steps = seq();
  for (var i=1; i<proof.length; i++)      {if (document.getElementById(i).checked && compatible(i,assumptions))
          {steps[steps.length] = i}};
  return steps}

function getassumptions (proof)
 {var level = 0;
  var assumptions = seq();
  for (var i=proof.length-1; i>0; i--)
      {if (proof[i][3]==='Implication Introduction') {level = level+1};
       if (proof[i][3]==='Assumption')
          {if (level===0) {assumptions = adjoin(i,assumptions)};
           if (level>0) {level = level-1}}};
  return assumptions}

function compatible (item,assumptions)
 {var step = proof[item];
  if (step[3]==='Assumption' && !findq(item,assumptions)) {return false};
  if (step[3]==='Implication Introduction')
     {assumptions = assumptions.slice(0);
      assumptions[assumptions.length] = step[4];
      return compatible(step[5],assumptions)};
  for (var j=4; j<step.length; j++)
      {if (!compatible(step[j],assumptions)) {return false}};
  return true}

//------------------------------------------------------------------------------
// dott
//------------------------------------------------------------------------------

function dott () {document.getElementById('tt').style.display = ''}function addtt () {var conclusion = read(document.getElementById('ttphi').value);  if (conclusion==='error') {alert('Syntax error'); return false};  var steps = getcheckedpremises(proof);  document.getElementById('tt').style.display = 'none';
  var premises=seq();
  for (var i=0; i<steps.length; i++) {premises[i] = proof[steps[i]][2]};
  var step = makestep(proof.length,conclusion,'Truth Table').concat(steps);
  if (entails(maksand(premises),conclusion)) {proof[proof.length] = step};  showproof(proof)}

function entails (p,q)
 {var cl = getconstants(q,getconstants(p,seq()));
  var al = new Array(cl.length);
  return checkentails(p,q,cl,al,0)}

function getconstants (p,cl)
 {if (symbolp(p)) {return adjoinit(p,cl)};
  if (p[0]==='not') {return getconstants(p[1],cl)};
  if (p[0]==='and')
     {for (var i=1; i<p.length; i++) {cl = getconstants(p[i],cl)};
      return cl};
  if (p[0]==='or')
     {for (var i=1; i<p.length; i++) {cl = getconstants(p[i],cl)};
      return cl};
  if (p[0]==='implication')
     {return getconstants(p[2],getconstants(p[1],cl))};
  if (p[0]==='equivalence')
     {return getconstants(p[2],getconstants(p[1],cl))};
  return adjoinit(p,cl)}

function checkentails (p,q,cl,al,n)
 {if (n>=cl.length) {return (!checktruth(p,cl,al)||checktruth(q,cl,al))};
  al[n] = true;
  if (!checkentails(p,q,cl,al,n+1)) {return false};
  al[n] = false;  return checkentails(p,q,cl,al,n+1)}
function checktruth (p,cl,al) {if (symbolp(p)) {return checkvalue(p,cl,al)};  if (p[0]==='not') {return !checktruth(p[1],cl,al)};  if (p[0]==='and')
     {for (var i=1; i<p.length; i++)
          {if (!checktruth(p[i],cl,al)) {return false}};
      return true};
  if (p[0]==='or')
     {for (var i=1; i<p.length; i++)
          {if (checktruth(p[i],cl,al)) {return true}};
      return false};
  if (p[0]==='equivalence')
     {return (checktruth(p[1],cl,al)===checktruth(p[2],cl,al))}  if (p[0]==='implication')
     {return (!checktruth(p[1],cl,al)||checktruth(p[2],cl,al))};  return checkvalue(p,cl,al)}

function checkvalue (p,cl,al)
 {for (var i=0; i<cl.length; i++)
      {if (equalp(p,cl[i])) {return al[i]}}
  return false}

function untt () {document.getElementById('tt').style.display = 'none'}//------------------------------------------------------------------------------
// doshortcut
//------------------------------------------------------------------------------

function doshortcut () {document.getElementById('shortcut').style.display = ''}function addshortcut () {var exp = read(document.getElementById('newconclusion').value);  if (exp==='error') {alert('Syntax error'); return false};  var just = document.getElementById('newjustification').value;
  var steps = getcheckedpremises(proof);  document.getElementById('shortcut').style.display = 'none';  proof[proof.length] = makestep(proof.length,exp,just).concat(steps);  showproof(proof)}

function unshortcut () {document.getElementById('shortcut').style.display = 'none'}//------------------------------------------------------------------------------
// dodelete
//------------------------------------------------------------------------------

function dodelete () {proof = getnewproof(proof);
  showproof(proof);  return true}

function getnewproof (proof)
 {var concordance = seq(0);
  var newproof = makeproof();
  var newstep = 0;
  for (var i=1; i<proof.length; i++)      {if (document.getElementById(i).checked || !checksupport(proof[i],concordance))
          {concordance[i] = false}
       else {newstep=newstep+1;
             concordance[i]=newstep;
             updatesupport(proof[i],concordance);
             newproof[newproof.length]=proof[i]}};
  return newproof}

function checksupport (step,concordance) {for (var j=4; j<step.length; j++)      {if (!concordance[step[j]]) {return false}};  return true}function updatesupport (step,concordance) {step[1] = concordance[step[1]];
  for (var j=4; j<step.length; j++)      {step[j] = concordance[step[j]]};  return true}//------------------------------------------------------------------------------
// doni
//------------------------------------------------------------------------------

function doni () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {for (var j=0; j<steps.length; j++)           {var result = ni(proof[steps[i]][2],proof[steps[j]][2]);            if (result != false)               {proof[proof.length]=makestep(proof.length,result,'Negation Introduction',steps[i],steps[j])}}};  showproof(proof);  return true}

function ni (p,q) {if (!symbolp(p) && p[0]=='implication' && !symbolp(q) && q[0]=='implication' &&
      equalp(p[1],q[1]) && complementaryp(p[2],q[2]))     {return makenegation(p[1])};   return false}

function complementaryp (p,q)
 {return (!symbolp(q) && q[0]=='not' && equalp(p,q[1]))}

//------------------------------------------------------------------------------
// done
//------------------------------------------------------------------------------
function done () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {var result = ne(proof[steps[i]][2]);       if (result != false)          {proof[proof.length]=makestep(proof.length,result,'Negation Elimination',steps[i])}};  showproof(proof);  return true}

function ne (p) {if (!symbolp(p) && p[0] == 'not' && !symbolp(p[1]) && p[1][0] == 'not')     {return p[1][1]}  else return false}//------------------------------------------------------------------------------
// doai
//------------------------------------------------------------------------------

function doai () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {for (var j=0; j<steps.length; j++)           {var result = ai(proof[steps[i]][2],proof[steps[j]][2]);            if (result!==false)               {proof[proof.length]=makestep(proof.length,result,'And Introduction',steps[i],steps[j])}}};  showproof(proof);  return true}

function ai (p,q) {return makeconjunction(p,q)}//------------------------------------------------------------------------------
// doae
//------------------------------------------------------------------------------
function doae () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {var results = ae(proof[steps[i]][2]);       for (var j=0; j<results.length; j++)           {proof[proof.length]=makestep(proof.length,results[j],'And Elimination',steps[i])}};  showproof(proof);  return true}
function ae (p) {if (!symbolp(p) && p[0] == 'and') {return p.slice(1,p.length)}  return empty()}//------------------------------------------------------------------------------
// dooi
//------------------------------------------------------------------------------

function dooi () {document.getElementById('oi').style.display = ''}function addoi () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  var exp = read(document.getElementById('newoi').value);  if (exp==='error') {alert('Syntax error'); return false};  document.getElementById('oi').style.display = 'none';  for (var i=0; i<steps.length; i++)      {var result = oi(proof[steps[i]][2],exp);       proof[proof.length]=makestep(proof.length,result,'Or Introduction',steps[i]);
       result = oi(exp,proof[steps[i]][2]);
       proof[proof.length]=makestep(proof.length,result,'Or Introduction',steps[i])};  showproof(proof);  return true}

function oi (p,q) {return makedisjunction(p,q)}

function unoi () {document.getElementById('oi').style.display = 'none'}//------------------------------------------------------------------------------
// dooe
//------------------------------------------------------------------------------
function dooe () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};
  for (var i=0; i<steps.length; i++)      {if (proof[steps[i]][2][0]==='or')
          {for (var j=0; j<steps.length; j++)
               {if (!symbolp(proof[steps[j]][2]) &&
                    proof[steps[j]][2][0]==='implication' &&
                    equalp(proof[steps[j]][2][1],proof[steps[i]][2][1]))
                   {for (var k=0; k<steps.length; k++)
                        {if (!symbolp(proof[steps[k]][2]) &&
                             proof[steps[k]][2][0]=='implication' &&
                             equalp(proof[steps[k]][2][1],proof[steps[i]][2][2]) &&
                             equalp(proof[steps[k]][2][2],proof[steps[j]][2][2]))
                         proof[proof.length]=makestep(proof.length,proof[steps[k]][2][2],
                                                        'Or Elimination',
                                                         steps[i],
                                                         steps[j],
                                                         steps[k])}}}}};  showproof(proof);
  return true}

//------------------------------------------------------------------------------
// doii
//------------------------------------------------------------------------------
function doii () {if (prooflevel(proof)===1)     {alert('No compatible rows selected.'); return false};
  var start = getassumption(proof);
  if (start)
     {var result = makeimplication(proof[start][2],proof[proof.length-1][2])};
      proof[proof.length]=makestep(proof.length,result,'Implication Introduction',start,proof.length-1);
  showproof(proof);
  return true}
function getassumption (proof)
 {var level = 0;
  for (var i=proof.length-1; i>0; i--)
      {if (proof[i][3]==='Implication Introduction') {level = level+1};
       if (proof[i][3]==='Assumption')
          {if (level===0) {return i} else {level = level-1}}};
  return false}

//------------------------------------------------------------------------------
// doie
//------------------------------------------------------------------------------

function doie () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {for (var j=0; j<steps.length; j++)           {var result = mp(proof[steps[i]][2],proof[steps[j]][2]);            if (result != false)               {proof[proof.length]=makestep(proof.length,result,'Implication Elimination',steps[i],steps[j])}}};  showproof(proof);  return true}function mp (p,q) {if (!symbolp(p) && p[0] == 'implication' && equalp(p[1],q))     {return p[2]}  else return false}//------------------------------------------------------------------------------
// dobi
//------------------------------------------------------------------------------

function dobi () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {for (var j=0; j<steps.length; j++)           {var result = bi(proof[steps[i]][2],proof[steps[j]][2]);            if (result != false)               {proof[proof.length]=makestep(proof.length,result,'Biconditional Introduction',steps[i],steps[j])}}};  showproof(proof);  return true}function bi (p,q) {if (!symbolp(p) && p[0] == 'implication' &&
      !symbolp(q) && q[0] == 'implication' &&
      equalp(p[1],q[2]) && equalp(p[2],q[1]))     {return makeequivalence(p[1],p[2])};  return false}//------------------------------------------------------------------------------
// dobe
//------------------------------------------------------------------------------

function dobe () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {var results = be(proof[steps[i]][2]);       for (var j=0; j<results.length; j++)           {proof[proof.length]=makestep(proof.length,results[j],'Biconditional Elimination',steps[i])}};  showproof(proof);  return true}

function be (p) {if (!symbolp(p) && p[0] == 'equivalence')     {return seq(makeimplication(p[1],p[2]),makeimplication(p[2],p[1]))};  return empty()}

//------------------------------------------------------------------------------
// doqi
//------------------------------------------------------------------------------
function doqi () {document.getElementById('qi').style.display = ''}function addqi () {var tau = read(document.getElementById('qitau').value);  if (tau==='error') {alert('Syntax error'); return false};  document.getElementById('qi').style.display = 'none';  var result = makeequality(tau,tau);
  proof[proof.length]=makestep(proof.length,result,'Equality Introduction');  showproof(proof);  return true}function unqi () {document.getElementById('qi').style.display = 'none'}//------------------------------------------------------------------------------
// doqe
//------------------------------------------------------------------------------

function doqe () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {var eqn = proof[steps[i]][2];
       if (!symbolp(eqn) && eqn[0]=='equal')
          {var sigma = eqn[1];
           var tau = eqn[2];
           for (var j=0; j<steps.length; j++)
               {if (i!=j)
                   {var results = substitutions(sigma,tau,proof[steps[j]][2]);                    for (var k=1; k<results.length; k++)                        {proof[proof.length]=makestep(proof.length,results[k],'Equality Elimination',steps[j],steps[i])}}};
           for (var j=0; j<steps.length; j++)
               {if (i!=j)
                   {var results = substitutions(tau,sigma,proof[steps[j]][2]);                    for (var k=1; k<results.length; k++)                        {proof[proof.length]=makestep(proof.length,results[k],'Equality Elimination',steps[j],steps[i])}}}}};  showproof(proof);  return true}

//------------------------------------------------------------------------------
// doui
//------------------------------------------------------------------------------

function doui () {document.getElementById('ui').style.display = ''}function addui () {var nu = read(document.getElementById('uinu').value);  if (nu==='error') {alert('Syntax error'); return false};  if (!varp(nu)) {alert(grind(nu) + ' is not a variable.'); return false};  document.getElementById('ui').style.display = 'none';
  var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {var result = ui(nu,proof[steps[i]][2]);       if (result != false)
          {proof[proof.length]=makestep(proof.length,result,'Universal Introduction',steps[i])}};  showproof(proof);  return true}

function ui (nu,phi)
 {if (amongp(nu,phi) && trapped(nu,proof)) {return false};
  return makeuniversal(nu,phi)}

function trapped (nu,proof)
 {var step = proof.length-1;
  while (step && step>0)
   {if (proof[step][3]==='Assumption' &&
        find(nu,freevars(proof[step][2],[],nil)))
       {return true};
    step = backskip(proof,step)};
  return false}

function backskip (proof,step)
 {if (proof[step][3]==='Implication Introduction')
     {var level=1;
      for (var i=step-1; i>1; i--)
          {if (level<=0) {return i};
           if (proof[i][3]==='Implication Introduction') {level=level+1};
           if (proof[i][3]==='Assumption') {level=level-1}};
      return false};
  return step-1}
function unui () {document.getElementById('ui').style.display = 'none'}
//------------------------------------------------------------------------------
// doue
//------------------------------------------------------------------------------

function doue () {document.getElementById('ue').style.display = ''}function addue () {var tau = read(document.getElementById('uetau').value);  if (tau==='error') {alert('Syntax error'); return false};  document.getElementById('ue').style.display = 'none';  var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {if (proof[steps[i]][2][0]==='forall')
          {var nu = proof[steps[i]][2][1];
           var phi = proof[steps[i]][2][2];
           if (substitutablep(tau,nu,phi))
              {var result = subst(tau,nu,phi);               proof[proof.length]=makestep(proof.length,result,'Universal Elimination',steps[i])}}};  showproof(proof);  return true}

function unue () {document.getElementById('ue').style.display = 'none'}
//------------------------------------------------------------------------------
// doei
//------------------------------------------------------------------------------
function doei () {document.getElementById('ei').style.display = ''}function addei () {var tau = read(document.getElementById('egtau').value);  if (tau==='error') {alert('Syntax error'); return false};  var nu = read(document.getElementById('egnu').value);  if (nu==='error') {alert('Syntax error'); return false};  if (!varp(nu)) {alert(grind(nu) + ' is not a variable.'); return false};  document.getElementById('ei').style.display = 'none';  var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {var results = substitutions(tau,nu,proof[steps[i]][2]);       for (var j=1; j<results.length; j++)           {var result = makeexistential(nu,results[j]);
            proof[proof.length]=makestep(proof.length,result,'Existential Introduction',steps[i])}};  showproof(proof);  return true}function unei () {document.getElementById('ei').style.display = 'none'}//------------------------------------------------------------------------------
// doee
//------------------------------------------------------------------------------
function doee () {var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};  for (var i=0; i<steps.length; i++)      {var result = ee(proof[steps[i]][2]);       if (result!=false)          {proof[proof.length]=makestep(proof.length,result,'Existential Elimination',steps[i])}};  showproof(proof);  return true}

function ee (p) {if (!symbolp(p) && p[0]==='exists')
     {var sk = freevars(p,[newsym()],nil);
      if (sk.length===1) {sk = seq('skolem',sk[0])} else {sk = seq('skolem',sk)};
      return subst(sk,p[1],p[2])};
  return false}
//------------------------------------------------------------------------------
// dodc
//------------------------------------------------------------------------------
var objectconstants = seq()
var functionconstants = seq()
function dodc () {document.getElementById('dc').style.display = ''}function adddc () {var psi = read(document.getElementById('dcphi').value);  if (psi==='error') {alert('Syntax error'); return false};  var nu = psi[1];  var phi = psi[2];  document.getElementById('dc').style.display = 'none';  var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};
  var just = dcp(nu,phi,steps);
  var step = makestep(proof.length,psi,'Domain Closure').concat(just);
  if (just) {proof[proof.length]=step};  showproof(proof);  return true}

function dcp (nu,phi,steps)
 {var just=seq();
  for (var i=0; i<objectconstants.length; i++)      {var step = included(subst(objectconstants[i],nu,phi),steps);
       if (step===false) {return false};
       just[just.length]=step};
  return just}

function included (chi,steps)
 {for (i=0; i<steps.length; i++)
      {if (equalp(proof[steps[i]][2],chi)) {return steps[i]}};
  return false}function undc () {document.getElementById('dc').style.display = 'none'}

//------------------------------------------------------------------------------

function getobjectconstants (item)
 {var results = seq();
  for (var i=1; i<item.length; i++)
      {results = getobjectssent(item[i][2],results)};
  return results};

function getobjectssent (p,results)
 {if (symbolp(p)) {return results};
  if (p[0]=='not') {return getobjectslogical(p,results)};
  if (p[0]=='and') {return getobjectslogical(p,results)};
  if (p[0]=='or') {return getobjectslogical(p,results)};
  if (p[0]=='implication') {return getobjectslogical(p,results)};
  if (p[0]=='equivalence') {return getobjectslogical(p,results)};
  if (p[0]=='forall') {return getobjectslogical(p[2],results)};
  if (p[0]=='exists') {return getobjectslogical(p[2],results)};
  if (p[0]=='clause') {return getobjectslogical(p,results)};
  return getobjectsterm(p,results)}

function getobjectslogical (p,results)
 {for (var i=1; i<p.length; i++)
      {results = getobjectssent(p[i],results)};
  return results}

function getobjectsterm (x,results)
 {if (symbolp(x) && !varp(x)) {return adjoin(x,results)};
  if (symbolp(x)) {return results};
  for (var i=1; i<x.length; i++)
      {results = getobjectsterm(x[i],results)};
  return results}//------------------------------------------------------------------------------

function getfunctionconstants (item)
 {var results = seq();
  for (var i=1; i<item.length; i++)
      {results = getfunctionssent(item[i][2],results)};
  return results};

function getfunctionssent (p,results)
 {if (symbolp(p)) {return results};
  if (p[0]=='not') {return getfunctionslogical(p,results)};
  if (p[0]=='and') {return getfunctionslogical(p,results)};
  if (p[0]=='or') {return getfunctionslogical(p,results)};
  if (p[0]=='implication') {return getfunctionslogical(p,results)};
  if (p[0]=='equivalence') {return getfunctionslogical(p,results)};
  if (p[0]=='forall') {return getfunctionslogical(p[2],results)};
  if (p[0]=='exists') {return getfunctionslogical(p[2],results)};
  if (p[0]=='clause') {return getfunctionslogical(p,results)};
  for (var i=1; i<p.length; i++)
      {results = getfunctionsterm(p[i],results)};
  return results}

function getfunctionslogical (p,results)
 {for (var i=1; i<p.length; i++)
      {results = getfunctionssent(p[i],results)};
  return results}

function getfunctionsterm (x,results)
 {if (symbolp(x)) {return results};
  results = adjoin(x[0],results);
  for (var i=1; i<x.length; i++)
      {results = getfunctionsterm(x[i],results)};
  return results}//------------------------------------------------------------------------------
// doind
//------------------------------------------------------------------------------

function doind () {document.getElementById('ind').style.display = ''}function addind () {var psi = read(document.getElementById('indphi').value);  if (psi==='error') {alert('Syntax error'); return false};  var nu = psi[1];  var phi = psi[2];  document.getElementById('ind').style.display = 'none';  var steps = getcheckedpremises(proof);
  if (steps.length==0)     {alert('No compatible rows selected.'); return false};
  var step = makestep(proof.length,psi,'Induction');
  var base = dcp(nu,phi,steps);
  var inductive = ind(nu,phi,steps);
  if (base && inductive) {proof[proof.length]=step.concat(base,inductive)};  showproof(proof);  return true}

function ind (nu,phi,steps)
 {var just=seq();
  for (var i=0; i<functionconstants.length; i++)      {var step = coveredp(functionconstants[i],nu,phi,steps);
       if (step===false) {return false};
       just[just.length]=step};
  return just}

function coveredp (pi,nu,phi,steps)
 {var pattern = seq('implication',phi,subst(seq(pi,nu),nu,phi));
  for (i=0; i<steps.length; i++)
      {var item = proof[steps[i]][2];
       if (!symbolp(item) && item[0]=='forall' && similarp(pattern,item[2],nu,item[1]))
          {return steps[i]}};
  return false}

function coveredp (pi,nu,phi,steps)
 {var arity = getarity(pi,proof);
  if (!arity) {return false};
  if (arity===1) {return onecoveredp(pi,nu,phi,steps)};
  if (arity===2) {return twocoveredp(pi,nu,phi,steps)};
  return false}

function getarity (pi,exp)
 {if (symbolp(exp)) {return false};
  if (exp.length===0) {return false};
  if (exp[0]===pi) {return exp.length-1};
  for (var i=1; i<exp.length; i++)
      {var ans = getarity(pi,exp[i]);
       if (ans) {return ans}}
  return false} 

function onecoveredp (pi,nu,phi,steps)
 {var pattern = seq('implication',phi,subst(seq(pi,nu),nu,phi));
  for (i=0; i<steps.length; i++)
      {var item = proof[steps[i]][2];
       if (!symbolp(item) && item[0]=='forall' && similarp(pattern,item[2],nu,item[1]))
          {return steps[i]}};
  return false}

function similarp (p,q,x,y) {if (p==x) {return q==y};
  if (symbolp(p)) {if (symbolp(q)) {return p==q} else {return false}};  if (symbolp(q)) {return false};
  if (p.length != q.length) {return false};  for (var i=0; i<p.length; i++) {if (!similarp(p[i],q[i],x,y)) {return false}};  return true}

function twocoveredp (pi,nu,phi,steps)
 {var var1 = newvar();
  var var2 = newvar();
  var test1 = subst(var1,nu,phi);
  var test2 = subst(var2,nu,phi);
  var conclusion = subst(seq(pi,var1,var2),nu,phi);
  var pattern = seq('implication',seq('and',test1,test2),conclusion);
  for (i=0; i<steps.length; i++)
      {var item = proof[steps[i]][2];
       if (!symbolp(item) && item[0]=='forall' &&
           !symbolp(item[2]) && item[2][0]==='forall' &&
           bisimilarp(pattern,item[2][2],var1,item[1],var2,item[2][1]))
          {return steps[i]}};
  return false}

function bisimilarp (p,q,u,x,v,y) {if (p==u) {return q===x};
  if (p==v) {return q===y};
  if (symbolp(p)) {if (symbolp(q)) {return p===q} else {return false}};  if (symbolp(q)) {return false};
  if (p.length != q.length) {return false};  for (var i=0; i<p.length; i++)
      {if (!bisimilarp(p[i],q[i],u,x,v,y)) {return false}};  return true}

function unind () {document.getElementById('ind').style.display = 'none'}//------------------------------------------------------------------------------
// doload
//------------------------------------------------------------------------------

function doload ()
 {document.getElementById('operation').style.display = '';
  return true}

function dofileselect (fileobj) {var reader = new FileReader();
  reader.onload = handleload;
  reader.readAsText(fileobj.files[0]);
  return true}

function handleload (evt)
 {var fileobj = document.getElementById('selector').files[0];
  var filename = fileobj.name;
  var filetype = fileobj.type;
  document.getElementById('proof').innerHTML = evt.target.result;
  unload();
  doinitialize()}

function unload () {document.getElementById('operation').style.display = 'none'}
//------------------------------------------------------------------------------
// doreset
//------------------------------------------------------------------------------
function doreset () {doinitialize()}

//------------------------------------------------------------------------------
// doxml
//------------------------------------------------------------------------------

function doxml () {var win = window.open();  //win.document.open('text/html');  win.document.writeln('<xmp>');  step = 0;  win.document.write(xmlize(proof,0));
  win.document.writeln('</xmp>');  win.document.close()}function xmlize (item,n) {if (item[0]=='step') {return xmlstep(item,n)};
  if (item[0]=='proof') {return xmlproof(item,n)};
  return ''}

function xmlstep (line,n)
 {step=step+1;
  var exp = '';
  exp += spaces(n) + '<step>\n';  exp += spaces(n) + '  <number>' + step + '</number>\n';  exp += spaces(n) + '  <sentence>' + grind(line[2]) + '</sentence>\n';  exp += spaces(n) + '  <justification>' + prettify(line[3]) + '</justification>\n';  for (var j=4; j<line.length; j++)      {exp += spaces(n) + '  <antecedent>' + line[j] + '</antecedent>\n'};  exp += spaces(n) + '</step>\n';  return exp}function xmlproof (proof,n)
 {var exp = '';  exp += spaces(n) + '<proof>\n';  for (var i=1; i<proof.length; i++)
      {exp += xmlize(proof[i],n+1)};  exp += spaces(n) + '</proof>\n';  return exp}

function spaces (n)
 {exp = '';
  for (var i=0; i<n; i++) {exp += '  '};
  return exp}

//------------------------------------------------------------------------------
// Miscellaneous
//------------------------------------------------------------------------------

function deepcopy (x)
 {if (!(x instanceof Array)) {return x};
  var out = new Array(x.length)
  for (var i=0; i<x.length; i++) {out[i] = deepcopy(x[i])};
  return out}

function printseq (p) {if (typeof p == 'number') {return p};  if (typeof p == 'string') {return '"' + p + '"'};  var n = p.length;  var exp = '(';  if (n>0) {exp += printseq(p[0])};  for (var i=1; i<n; i++)      {exp = exp + ' ' + printseq(p[i])}  exp += ')';  return exp}

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
