program CalculoPendiente;

uses crt;  (* Usa la unidad crt para control de pantalla *)

var
  x1: real;  (* Coordenada x del primer punto *)
  y1: real;  (* Coordenada y del primer punto *)
  x2: real;  (* Coordenada x del segundo punto *)
  y2: real;  (* Coordenada y del segundo punto *)
  m: real;   (* Variable para almacenar la pendiente *)

begin
  clrscr;  (* Limpia la pantalla *)

  writeln('Calculo de la pendiente (m) entre dos puntos');  (* Mensaje inicial *)

  (* Solicitar al usuario ingresar las coordenadas del primer punto *)
  write('Ingresa el valor de x1: ');
  readln(x1);
  
  write('Ingresa el valor de y1: ');
  readln(y1);
  
  (* Solicitar al usuario ingresar las coordenadas del segundo punto *)
  write('Ingresa el valor de x2: ');
  readln(x2);
  
  write('Ingresa el valor de y2: ');
  readln(y2);
  
  (* Validar si la pendiente es indefinida (división entre cero) *)
  if x2 = x1 then
    writeln('La pendiente m es indefinida (division entre cero).')
  else
  begin
    (* Calcular la pendiente m usando la fórmula (y2 - y1) / (x2 - x1) *)
    m := (y2 - y1) / (x2 - x1);
    (* Mostrar el valor calculado de la pendiente con 2 decimales *)
    writeln('El valor de la pendiente m es: ', m:0:2);
  end;

  readln;  (* Esperar que el usuario presione una tecla antes de cerrar *)
end.
