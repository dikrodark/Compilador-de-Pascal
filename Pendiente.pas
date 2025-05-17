program CalculoPendiente;

uses crt;  (* Usa la unidad crt para control de pantalla *)

var
  x1: real;  (* Coordenada x del primer punto *)
  y1: real;  (* Coordenada y del primer punto *)
  x2: real;  (* Coordenada x del segundo punto *)
  y2: real;  (* Coordenada y del segundo punto *)
  m: real;   (* Variable para almacenar la pendiente *)

  begin
  (* Asignación de valores de ejemplo *)
  x1 := 2.0;  
  y1 := 3.0;
  x2 := 4.0;
  y2 := 6.0;

  (* Condicional para calcular pendiente *)
  if x2 = x1 then
    m := 0.0  (* Pendiente indefinida *)
  else
    m := (y2 - y1) / (x2 - x1);

  end
