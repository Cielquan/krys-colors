@tool @icon("res://icon.svg")
@static_unload
class_name MyNode
extends Node2D

## Script docu summary
##
## Some longer [lb]details[rb].[br]
## Move the [Sprite2D].
## See [annotation @GDScript.@rpc].
## See [constant Color.RED].
## See [enum Mesh.ArrayType].
## Get [member Node2D.scale].
## Call [method Node3D.hide].
## Use [constructor Color.Color].
## Use [operator Color.operator *].
## Emit [signal Node.renamed].
## See [theme_item Label.font].
## Takes [param size] for the size.
##
## @tutorial:             https://example.com/tutorial_1
## @tutorial(Tutorial 2): https://example.c
## @deprecated: Use [Parent] insteadom/tutorial_2
## @deprecated.
## @experimental
## @experimental: Take care
## @experimental : Invalid with space before : should not highlight
## Tags following text are invalid: @experimental
##
## [b]bold[/b]
## [i]italic[/i]
## [u]underline[/u]
## [s]strikethrough[/s]
## [font=res://mono.ttf]
##      [color=red]Error![/color]
##      LICENSE
## [/font]
## [img width=32]res://icon.svg[/img]
## [url]https://example.com[/url]
## [url=https://example.com]Website[/url]
## [center]2 + 2 = 4[/center]
## Press [kbd]Ctrl + C[/kbd].
## Returns [code]true[/code].
## [codeblock lang=gdscript]
## if true and 1:
##     print("Hi")
## [/codeblock]

# Normal comment

#region RegionName
signal ping() # Inline normal comment
signal changed(value: int) ## @experimental Inline doc comment
#endregion

enum State {
    IDLE = 1 << 2, # inline comment
    RUNNING,
}

# fmt:off
enum { IDLE = 1, RUNNING }; # Unnamed & oneliner, Semicolon is generally optional
# fmt:on

const MyScript = preload("res://my_script.gd")
var MyScript2 := load("res://my_script2.gd")

const PI2: float = PI * 2.0
const DATA := { "key": [1, 2, 3], 1: 2, &"name": null }
const DEPRECATED := Color8(1, 1, 1)

static var count: int = PI:
    get:
        return count * PI2
    set(v):
        count = clampi(v, 0, 100)

static var _static_state := State.IDLE

@export
var name_: String = "Default"

@export_range(0, 100)
var hp: int = 100

@export_group("Combat")
@export var damage: float = 10.5
var a
var a1: Array[Dictionary]
var a2: Array[MyNode]
var a3: Array[MyNode.InnerClass]
var d: Dictionary[String, Variant]

var my_file_ref

var Character = load("res://path/to/character.gd")

var values_non_static: Array[String] = ["one", "two"]

var velocity: Vector2 = Vector2(0, 0)

var milliseconds: int = 0
var seconds: int:
    set(value):
        milliseconds = value * 1000

var warns_when_changed:
    get:
        return warns_when_changed
    set(value):
        warns_when_changed = value

# Alternative syntax for getter/setter, where `get_my_prop` / `set_my_prop` are functions
var my_prop:
    get = get_my_prop, set = set_my_prop

# fmt:off
var my_prop2:
    get = get_my_prop2,
    set = set_my_prop2
# fmt:on

@onready var label: Label = %Label


static func _static_init() -> void:
    pass


func _init() -> void:
    pass


func _ready():
    var f = FileAccess.open("user://example_file.json", FileAccess.READ)
    my_file_ref = weakref(f)

    await get_tree().create_timer(0.5).timeout


func _physics_process(delta: float) -> void:
    velocity = velocity.lerp(Vector2.ZERO, delta * 0.9)


func _input(event: InputEvent) -> void:
    if event.is_action_pressed("jump"):
        create()


@abstract func abstr() -> void


@abstract
func abstr2() -> void


func custom_overridden_func() -> void:
    pass


func create() -> MyNode:
    return MyNode.new()


func _this_is_called_later():
    var my_file = my_file_ref.get_ref()
    if my_file:
        my_file.close()


func _numbers() -> float:
    var int_ := 01
    var hex := 0xDEADbeef00 + 0XdeadBEEF11
    var bin := 0b010101 + 0B010101
    var float_ := 01.0 + 1. + .1
    var scientific := 01.1e-10 + 2.2E+010 + 1E10
    var long := 01_000_000_.1_5_e-1_5_ + 0xdead_beef_00_ + 0b0101_0101_

    return int_ + hex + bin + float_ + scientific + long


func _special_number_const() -> float:
    var constants := PI + TAU
    var endless := INF
    var no_num := NAN

    return constants + endless + no_num


func _strings() -> void:
    var single := 'Single "'
    var escapes := "Hello\nWorld \u0832 \U000832 \n \t \r \a \b \f \v \" \' \\"
    var raw := r"C:\path\to\file"
    var raw_special_escapes := r"\"\'\\"
    # Below is line continuation
    var string_name := &"String"
    var multi_line := """\
Multi
line
string starting on first row because of \\ \n
"'
"""

    print("\n".join([single, escapes, string_name, raw, raw_special_escapes, multi_line]))


func _formatted_strings() -> void:
    var formatted_percent := "Player: \
        %-+010d HP: %*.*d/%0*d (%.1f%%)" % [name, hp, 100, 99.9]
    # Format specifiers in bracket syntax not supported, so no special scopes (v4.7)
    var formatted_brackets_num := "Player: {0} HP: {1}/{2} ({3:.1f}%)".format([name, hp, 100, 99.9])
    var formatted_brackets_name := "Player: {name} HP: {hp}/{max_hp} ({percent:.1f}%)".format(
        { "name": name, "hp": hp, "max_hp": 100, "percent": 99.9 }
    )
    print("\n".join([formatted_percent, formatted_brackets_num, formatted_brackets_name]))


func _get_path_nested(val: NodePath) -> NodePath:
    return val


func _nodes_and_node_paths() -> void:
    ## asfonasf onasfo naösofn asöofn ason
    var node_path := ^"Lab\
        \nel"
    var node_path_manual := NodePath("Label")

    var node_lu := get_node(node_path)
    var node_lu2 := get_node(_get_path_nested(node_path_manual))
    var node_lu3 := get_node("%Label/\
        %Child:prop")
    if (
        node_lu.can_process()
        and node_lu2.can_process()
        and node_lu3.can_process()
    ):
        print("Yay")

    var node_stringified := $"../{prefix}Canvas\nLayer/\
        %Label\u1234/%Child%d:prop"
    var node_bare := $CanvasLayer
    var node_bare_multi := $CanvasLayer/Label
    if (
        node_stringified.can_process()
        and node_bare.can_process()
        and node_bare_multi.can_process()
    ):
        print("Yay")

    var node_unique := %"Label"
    var node_bare_unique := %Label
    var node_bare_unique2 := $%Label
    var node_bare_unique_nested := %Label/\
        %Child
    if (
        node_unique.can_process()
        and node_bare_unique.\
            can_process()
        and node_bare_unique2.can_process()
        and node_bare_unique_nested.can_process()
    ):
        print("Yay")


func _conditionals(val: Node) -> void:
    if (true and not false) or null:
        pass
    elif true && (!false || null):
        pass
    else:
        pass

    var val2: Node = null
    if val is Node2D and val2 is not Array[Node3D]:
        pass

    if 1 in [1, 2] and 3 not in [1, 2]:
        pass

    @warning_ignore("unused_variable") var ternary := 1 if true else 0


func _match() -> void:
    match _static_state:
        State.IDLE | State.RUNNING:
            _static_state = State.RUNNING
        TYPE_INT, TYPE_FLOAT:
            pass
        var new_var:
            print("Bind value into 'new_var'", new_var)
        @warning_ignore(("unreachable_pattern"))
        _:
            print("Default/Fallback")

    match [1, 2, 3]:
        []:
            print("Empty array")
        [1, 3, "test", null]:
            print("Very specific array")
        [var start, _, "test"]:
            print("First element is ", start, ", and the last is \"test\"")
        [42, ..]:
            print("Open ended array")

    match { "name": "Godot", "age": 4 }:
        { }:
            print("Empty dict")
        { "name": "Dennis" }:
            print("The name is Dennis")
        { "name": "Dennis", "age": var age }:
            print("Dennis is ", age, " years old.")
        { "name", "age" }:
            print("Has a name and an age, but it's not Dennis :(")
        { "key": "godotisawesome", .. }:
            print("I only checked for one entry and ignored the rest")

    var point := [1, 2]
    match point:
        [0, 0]:
            print("Origin")
        [_, 0]:
            print("Point on X-axis")
        [0, _]:
            print("Point on Y-axis")
        [var x, var y] when y == x:
            print("Point on line y = x")
        [var x, var y] when y == -x:
            print("Point on line y = -x")
        [var x, var y]:
            print("Point (%s, %s)" % [x, y])


func _loops() -> void:
    for item in values_non_static:
        continue

    for item: String in values_non_static:
        continue

    while len(values_non_static) < 10:
        break


func _flow() -> void:
    assert(false != true, "Not true!")

    breakpoint


func _signals() -> void:
    ping.connect(_flow)
    emit_signal(&"changed", count)
    emit_signal(&"ping")
    ping.disconnect(_flow)


func _callables(function: Callable) -> void:
    function.callv([1, 2])

    var callable := func(x: int = 1) -> int:
        var num := int(1.0)
        return x * num * 2.0 as int

    count = await callable.call(21)

    var callable2 := func give_back (x):
        return x

    count = callable2.call(count)

    var callable3 = func():
        return 42

    queue_free()


func _parameters(_normal, _default = 1, ... args) -> void:
    pass


func _parameters_typed(_normal: String, _default: int = 1, ... args: Array) -> Array:
    return args


func _type_casts() -> void:
    var d: Dictionary = { "foo": 1 as float, "bar": 2 as float }
    var v = (d as Dictionary[String, Variant]).get("foo")

    var n := (1.0 as int) * 2.0 as int * 2

    var x: Variant = null
    x = x as Node
    x = x as Array[String]
    x = x as Array[Dictionary[String, int]]
    x = x as MyClass
    x = (x as MyClass.SubType)


func _primitives() -> String:
    var str_: String = str("")
    var string: String = String("")
    var node_path: NodePath = NodePath("")
    var int_: int = int(0)
    var float_: float = float(0)
    var bool_: bool = bool(0)

    return str(str_, string, node_path, int_, float_, bool_)


func _builtins() -> void:
    var pink := Color(255, 0, 255)
    var vec: Vector2i = Vector2i(1, 2)


func _substription() -> int:
    var arr: Array[int] = [1, 2]
    var val = arr[0]

    var dict = { "key": "value" }
    var val2 = dict["key"]
    var val3 = dict.get("key")

    print(val2 + val3)

    return val


func _punctuation() -> void:
    foo.bar
    foo.bar.baz
    foo().bar
    foo[0].bar()
    foo()[0]

    #fmt:off
    foo(
        bar,
        (baz)
    )

    foo({
        "x": 1
    })
    #fmt:on


func _arithemitic_operators() -> int:
    return 01 + 10 - 2 * 3 ** 4 / 5 % 6


func _arithemitic_operators_assigning() -> int:
    var v := 0
    v += 1
    v -= 1
    v *= 1
    v **= 1
    v /= 1
    v %= 1
    return v


func _bitwise_operators() -> int:
    return ~(1 >> 1 << 1 & 1 ^ 1 | 1)


func _bitwise_operators_assigning() -> int:
    var v := 0
    v >>= 1
    v <<= 1
    v &= 1
    v ^= 1
    v |= 1
    return v


func _comparison() -> bool:
    return 1 == 1.0 and 1 != 2 and 1 < 2 and 1 <= 2 and 2 >= 1 and 2 > 1


func _builtin_const() -> int:
    return (
        SIDE_BOTTOM + MOUSE_BUTTON_LEFT + KEY_0 + FAILED + TYPE_AABB
        + MIDI_MESSAGE_ACTIVE_SENSING + KEY_CODE_MASK + PROPERTY_HINT_NODE_PATH_TO_EDITED_NODE
    )


func _builtin_enum() -> int:
    var c := Side.SIDE_BOTTOM
    return (
        Side.SIDE_BOTTOM + MouseButton.MOUSE_BUTTON_LEFT + Key.KEY_0 + Error.FAILED
        + Variant.Type.TYPE_AABB + MIDIMessage.MIDI_MESSAGE_ACTIVE_SENSING
        + KeyModifierMask.KEY_CODE_MASK + PropertyHint.PROPERTY_HINT_NODE_PATH_TO_EDITED_NODE
    )


class Parent:
    var val = 0


    func _ready() -> void:
        pass


    func do_this(_value) -> void:
        pass


class Child extends MyNode.Parent:
    var value: int = 0


    static func double(val: int) -> int:
        return val * 2


    func _ready() -> void:
        super()
        super._ready()
        self.value = 1
        self.do_that()
        self.value.to_string()


    func do_that() -> void:
        super.do_this(1)


class Foo1 extends Node2D:
    pass


class Foo2 extends MyNamespace.SomeClass:
    pass


class Foo3 extends "res://foo.gd":
    pass


class Foo4 extends "node_2d.gd".Node2D:
    pass
