//------------------------------------------------------------------------------
// doinitialize
//------------------------------------------------------------------------------

function doinitialize ()
 {var archive = archivetoproof(document.getElementsByTagName('proof')[0]);
  proof = getstart(archive);
  showproof(proof);
  goal = getgoal(archive);  document.getElementById('goal').innerHTML = '&nbsp;&nbsp;' + goal;
  return true}

function getstart (proof)
 {var start = seq('proof');
  for (var i=0; i<proof.length; i++)
      {if (proof[i][3]=='Premise') {start[start.length] = proof[i]}};
  return start}

function getgoal (proof)
 {return grind(proof[proof.length-1][2])}

//------------------------------------------------------------------------------
// showproof
//------------------------------------------------------------------------------

function showproof (proof)
 {var area = document.getElementById('proof');
  var n = area.childNodes.length;
  for (var i=0; i<n; i++) {area.removeChild(area.childNodes[0])};
  area.appendChild(displayproof(proof));
  //showsignature();
  showbuttons();
  showgrades()}

//------------------------------------------------------------------------------
// showanswer
//------------------------------------------------------------------------------
function showanswer ()
 {proof = archivetoproof(document.getElementsByTagName('proof')[0]);
  showproof(proof)}

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
     {document.getElementById('dopremise').disabled=true;
      document.getElementById('doii').disabled=true;
      return true};
  document.getElementById('dopremise').disabled=true;
  document.getElementById('doii').disabled=false;

  return true}

//------------------------------------------------------------------------------
// showgrades
//------------------------------------------------------------------------------

function showgrades ()
 {var status=document.getElementById('status');
  if (conclusionp(read(goal),proof))
     {status.innerHTML='Complete';
      status.style.color='#00ff00'}
     else {status.innerHTML='Incomplete';
           status.style.color='#ff0000'};
  return true}

function conclusionp (p,proof)
 {var depth = 0;
  for (var i=1; i<proof.length; i++)
      {if (proof[i][3]==='Assumption') {depth = depth+1};
       if (proof[i][3]==='Implication Introduction') {depth = depth-1};
       if (depth===0 && equalp(proof[i][2],p)) {return true}};
  return false}

//------------------------------------------------------------------------------// computegrade//------------------------------------------------------------------------------

function computegrade ()
 {var status=document.getElementById('status');
  if (status.innerHTML==='Complete') {return 1.0};
  return 0.0}

//------------------------------------------------------------------------------
// toggleinstructions
//------------------------------------------------------------------------------

function toggleinstructions (toggle)
 {if (toggle.innerHTML == 'Hide Instructions')
     {toggle.innerHTML = 'Show Instructions';
      document.getElementById('instructions').style.display='none';
      return true};
  toggle.innerHTML='Hide Instructions';
  document.getElementById('instructions').style.display='';
  return true}

//------------------------------------------------------------------------------
// doreset
//------------------------------------------------------------------------------
function doreset () {doinitialize()}

//------------------------------------------------------------------------------
// End of Script
//------------------------------------------------------------------------------
