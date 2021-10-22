% 3.4 Practical Session 

% Imagine that the following knowledge base describes a maze. The facts determine which points are connected, that is, from which points you can get to which other points in one step. Furthermore, imagine that all paths are one-way streets, so that you can only walk them in one direction. So, you can get from point 1 to point 2, but not the other way round.

connected(1,2).
connected(3,4).
connected(5,6).
connected(7,8).
connected(9,10).
connected(12,13).
connected(13,14).
connected(15,16).
connected(17,18).
connected(19,20).
connected(4,1).
connected(6,3).
connected(4,7).
connected(6,11).
connected(14,9).
connected(11,15).
connected(16,12).
connected(14,17).
connected(16,19).

% Write a predicate path/2 that tells you from which points in the maze you can get to which other points when chaining together connections given in the above knowledge base. Can you get from point 5 to point 10? Which other point can you get to when starting at point 1? And which points can be reached from point 13?
path(Start,Finish) :- connected(Start,Finish).
path(Start,Finish) :- connected(Start,Temp), path(Temp,Finish).



% 
   byCar(auckland,hamilton).
   byCar(hamilton,raglan).
   byCar(valmont,saarbruecken).
   byCar(valmont,metz).
   
   byTrain(metz,frankfurt).
   byTrain(saarbruecken,frankfurt).
   byTrain(metz,paris).
   byTrain(saarbruecken,paris).
   
   byPlane(frankfurt,bangkok).
   byPlane(frankfurt,singapore).
   byPlane(paris,losAngeles).
   byPlane(bangkok,auckland).
   byPlane(singapore,auckland).
   byPlane(losAngeles,auckland).

% Write a predicate travel/2 which determines whether it is possible to travel from one place to another by chaining together car, train, and plane journeys. For example, your program should answer yes to the query travel(valmont,raglan) . 

connect(Start,Finish) :- byCar(Start,Finish).
connect(Start,Finish) :- byTrain(Start,Finish).
connect(Start,Finish) :- byPlane(Start,Finish).

travel(Start,Finish) :- connect(Start,Finish).
travel(Start,Finish) :- connect(Start,Temp), travel(Temp,Finish).

% So, by using travel/2 to query the above database, you can find out that it is possible to go from Valmont to Raglan. If you are planning such a voyage, that’s already something useful to know, but you would probably prefer to have the precise route from Valmont to Raglan. Write a predicate travel/3 which tells you which route to take when travelling from one place to another. For example, the program should respond
%   X  =  go(valmont,metz,
%                 go(metz,paris,
%                       go(paris,losAngeles)))
%
%to the query travel(valmont,losAngeles,X) . 

% go/3 is a "go/3 chain", terminated by a "go/2"
%go(X,Y,go(Y,Z)) :- connected(X,Y), connected(Y,Z)
%go(A,Z,go(A,T,)) :- connected(

%travel(Start, Finish, go(Start, Finish)) :- go(Start, Finish).
%travel(Start, Finish, go(Start, Temp, go(Temp, Finish))) :- go(Start, Temp, go(Temp, Finish)).

%travel(Start, Finish, go(Start, Second)) :- go(Start, Second), travel(Temp, Finish, go(Start, Temp, 
