program FuncionTrigonometrica;

var anguloGrados: real;
var anguloRadianes: real;
var senoVal: real;
var cosenoVal: real;
var tangenteVal: real;

begin
write("Calculadora de funciones trigonométricas");
write("Ingrese un ángulo en grados:");
read(anguloGrados);

anguloRadianes := anguloGrados * 3.1416 / 180;
senoVal := sin(anguloRadianes);
cosenoVal := cos(anguloRadianes);
tangenteVal := tan(anguloRadianes);

writeln("Seno = ", senoVal);


end.
