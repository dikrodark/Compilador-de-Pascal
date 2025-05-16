program FuncionesTrigonométricas;

uses
  crt, math;  { math para funciones trigonométricas }

var
  anguloGrados, anguloRadianes, senoVal, cosenoVal, tangenteVal: real;

begin
  clrscr;

  writeln('Calculadora de funciones trigonométricas');
  writeln('Ingrese un ángulo en grados:');
  readln(anguloGrados);

  { Convertir grados a radianes: rad = grados * pi / 180 }
  anguloRadianes := anguloGrados * Pi / 180;

  senoVal := sin(anguloRadianes);
  cosenoVal := cos(anguloRadianes);
  tangenteVal := tan(anguloRadianes);

  writeln('Seno(', anguloGrados:0:2, ') = ', senoVal:0:4);
  writeln('Coseno(', anguloGrados:0:2, ') = ', cosenoVal:0:4);
  writeln('Tangente(', anguloGrados:0:2, ') = ', tangenteVal:0:4);

  readln;
end.
