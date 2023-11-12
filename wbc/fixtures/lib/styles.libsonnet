local C = import 'constructors.libsonnet';
local const = import "constants.libsonnet";
local COLORS = const.COLORS;

local white_on_black = C.NamedStyle(
    'white_on_black',
    border=null,
    font=C.Font(face=const.FACES.tahoma, color=COLORS.white),
    fill=C.SolidFill(COLORS.black)
  ); 

local bold_white_on_blue = C.NamedStyle(
    'bold_white_on_blue',
    border=null,
    font=C.Font(face=const.FACES.tahoma, color=COLORS.white, bold=true),
    fill=C.SolidFill(COLORS.blue)
  ); 

{
    white_on_black: white_on_black,
    bold_white_on_blue: bold_white_on_blue
}