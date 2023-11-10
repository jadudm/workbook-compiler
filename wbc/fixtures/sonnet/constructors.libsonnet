local Types = import "types.libsonnet";

local Workbook(name, shs) = 
    Types.Workbook + {
        name: name,
        "sheets": shs
    };

local Sheet(name, rs) = 
    Types.Sheet + {
        name: name,
        "ranges": rs
    };

{
    Workbook:: Workbook,
    Sheet:: Sheet,
}