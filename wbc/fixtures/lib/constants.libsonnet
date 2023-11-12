local colors = import "color.libsonnet";

local BORDER = {
        double: "double",
        thin: "thin",
        thick: "thick"
    };

local FACES = {
    tahoma: "Tahoma",
    arial: "Arial",
    calibri: "Calibri"
};

{
    BORDER: BORDER,
    COLORS: colors,
    FACES: FACES
}