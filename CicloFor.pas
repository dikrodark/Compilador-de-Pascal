program CicloForBasico;

uses crt;

var
  i: integer;

begin
  clrscr;
  writeln('Mostrando los numeros del 1 al 10:');
  
  for i := 1 to 10 do
  begin
    writeln('Numero: ', i);
  end;

  readln;
end.
