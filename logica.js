//------------------------------------------------------------------------------

  exp[0] = 'step';

function maksand (s)

function maksor (s)

function adjoin (x,s)
  for (var i=0; i<z.length; i++)

function substit (x,y,z)
  for (var i=0; i<z.length; i++)
  if (r[0]==='forall' && (amongp(r[1],p) || amongp(r[1],q))) {return seq(r)};
  if (r[0]==='exists' && (amongp(r[1],p) || amongp(r[1],q))) {return seq(r)};
  return substitutionsexp(p,q,r,0)}

function substitutablep (x,y,z)
  if (z[0]==='not') {return substitutablep(x,y,z[1])};
     {for (var i=1; i<z.length; i++)
      return true};
     {return substitutablep(x,y,z[1]) && substitutablep(x,y,z[2])};
     {return (z[1]===y || substitutablep(x,y,z[2]))};
     {return (z[1]===y || !amongp(z[1],x) && substitutablep(x,y,z[2]))};

//------------------------------------------------------------------------------
// Lists
//------------------------------------------------------------------------------


function amongp (x,y)
 {if (symbolp(y)) {return x==y};
  for (var i=0; i<y.length; i++) {if (amongp(x,y[i])) {return true}}
  return false}
     {var result = seq('and');
      for (var i=1; i<p.length; i++) {result.push(implicationsout(p[i]))};
      return result};
     {var result = seq('or');
      for (var i=1; i<p.length; i++) {result.push(implicationsout(p[i]))};
      return result};
     {var result = seq('and');
      for (var i=1; i<p.length; i++) {result.push(negationsin(p[i]))};
      return result};
     {var result = seq('or');
      for (var i=1; i<p.length; i++) {result.push(negationsin(p[i]))};
      return result};
     {var result = seq('or');
      for (var i=1; i<p.length; i++) {result.push(negate(p[i]))};
      return result};
     {var result = seq('and');
      for (var i=1; i<p.length; i++) {result.push(negate(p[i]))};
      return result};

function stdize (p,al,bl)
 {if (varp(p))
     {var dum = assoc(p,bl);
      if (dum) {return cdr(dum)};
      return p};
  if (symbolp(p)) {return p};
  if (p[0]==='forall' || p[0]==='exists')
     {if (find(p[1],al))
         {var replacement = newvar();
          bl = acons(p[1],replacement,bl);
          return seq(p[0],replacement,stdize(p[2],al,bl))};
      al.push(p[1]);
      return seq(p[0],p[1],stdize(p[2],al,bl))};
  var out = seq(p[0]);
  for (var i=1; i<p.length; i++)
      {out.push(stdize(p[i],al,bl))};
  return out}

 {if (varp(p))
     {if (memberp(p,al)) {return al};
      if (memberp(p,bl)) {return al};
      return cons(p,al)};
  if (symbolp(p)) {return al};
  if (p[0] == 'forall') {return freevariables(p[2],al,cons(p[1],bl))};
  if (p[0] == 'exists') {return freevariables(p[2],al,cons(p[1],bl))};
  for (var i=1; i<p.length; i++) {al = freevariables(p[i],al,bl)};
  return al}


     {var result = seq('and');
      for (var i=1; i<p.length; i++) {result.push(disexistentialize(p[i],al,bl))};
      return result};
  if (p[0] == 'or')
     {var result = seq('or');
      for (var i=1; i<p.length; i++) {result.push(disexistentialize(p[i],al,bl))};
      return result};
     {var result = seq('and');
      for (var i=1; i<p.length; i++) {result.push(allsout(p[i]))};
      return result};
  if (p[0] == 'or')
     {var result = seq('or');
      for (var i=1; i<p.length; i++) {result.push(allsout(p[i]))};
      return result};
  if (p[0] == 'forall') {return allsout(p[2])};

function uniquify (ins)
function readdata (str)

    else if (charcode===93) {output[output.length] = ']'; cur++}

function parse (str)
       else {exp[exp.length] = parsexp('lparen','rparen')}};
  var left = parseprefix(rop);
    else if (!find(input[current],infixes)) {return left}
    else {throw 'error'}};

function parseprefix (rop)
  if (left==='[') {return parseskolem()};
  if (identifierp(left)) {current++; return left};
  throw 'error'}

    else {throw 'error'}};
 {current++;
  var sk = parsexp('comma','comma');
  if (input[current]!==']') {throw 'error'};
  current++;
  return seq('skolem',sk)}

function parseparenexp ()
 {current++;
  current++;
  return left}


function parseinfix (left,op,rop)
  var variable = left.slice(1,left.length);
     {return makeuniversal(variable,parsexp(':',rop))};
     {return makeexistential(variable,parsexp(':',rop))};

var tokens = [':','~','&','|','=>','<=>','[',']','comma','lparen','rparen','.','{','}']

function identifierp (x) {return !find(x,tokens)}


function precedencep (lop,rop)
      {if (precedence[i]===rop) {return false};
       if (precedence[i]===lop) {return true}};
  return false}


function grindskolem (p)
  var parens = parenp(lop,'&',rop);
  if (parens) {exp = '('};
  if (parens) {exp = exp + ')'};
function grindor (p,lop,rop)
  var parens = parenp(lop,'|',rop);
  if (parens) {exp = '('};
  if (parens) {exp = exp + ')'};


function printseq (p)
  if (p===false) {return 'false'};
  if (typeof p == 'number') {return p};

//------------------------------------------------------------------------------