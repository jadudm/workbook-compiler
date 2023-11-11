local colors = import "color.libsonnet";

local BORDER = {
        double: "double",
        thin: "thin",
        thick: "thick"
    };


{
    BORDER: BORDER,
    COLORS: colors
}