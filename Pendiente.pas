program CalculoPendiente;

var x1: real;
var x2: real;
var y1: real;
var y2: real;
var m: real;


begin 
write("Escriba el valor de x1: ");
read(x1);
write("Escriba el valor de x2: ");
read(x2);
write("Escriba el valor de y1: ");
read(y1);
write("Escriba el valor de y2: ");
read(y2);
m := (y2 - y1) / (x2 - x1);
writeln("La pendiente es: ", m);
end.
