local make_type(type) = {"type": type};

local Workbook = make_type("workbook");
local Sheet = make_type("sheet");
local LinearRange = make_type("linear_range");
local Cell = make_type("cell");
local Contents = make_type("contents");

local NamedStyle = make_type("named_style");
local Border = make_type("border");
local Side = make_type("side");
local PatternFill = make_type("pattern_fill");

local Formula = make_type("formula");
local Application = make_type("application");
local BinOp = make_type("binop");

local make_opera_type(type) = { "type": "operand:" + type };

local Null = make_opera_type("null");
local Integer = make_opera_type("integer");
local Boolean = make_opera_type("boolean");
local String = make_opera_type("string");
local NamedRange = make_opera_type("named_range");


{
    Workbook: Workbook,
    Sheet: Sheet,
    LinearRange: LinearRange,
    Cell: Cell,
    Contents: Contents,

    NamedStyle: NamedStyle,
    Border: Border,
    Side: Side,
    PatternFill: PatternFill,

    Formula: Formula,
    Application: Application,
    BinOp: BinOp,

    Null: Null,
    Integer: Integer,
    Boolean: Boolean,
    String: String,
    NamedRange: NamedRange
}