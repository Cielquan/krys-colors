# ============================================================
# Invalid / edge cases
# ============================================================
# fmt:off

namespace
trait
yield

var invalid_escape := "\j"

var invalid_quote_combination = """hello """" world"""

var nester_array: Array[Array[int]]
var nested_dict: Dictionary[String, Array[Vector2]]

@export : invalid
@ export
$
%
foo.
1e
0x
0b
0b_
123abc
# fmt:on
