# Comment

@tool
@icon("res://icon.svg")
class_name SyntaxTesting
extends CharacterBody2D


class Parent:
    func _ready() -> void:
        pass


class Child extends SyntaxTesting.Parent:
    var value: int = 0


    func _ready() -> void:
        breakpoint
        super()
        self.value = 1


    static func double(val: int) -> int:
        return val * 2


enum State {
    IDLE = 1,
    RUNNING,
}

# fmt:off
enum OnelineState { IDLE = 1, RUNNING }
# fmt:on

#region RegionName
signal changed(value: int)
signal ping()
#endregion


## Doc comment
const PI2 := PI * 2.0
const DATA := { "key": [1, 2, 3], &"name": null }

@export
var name_: String = "Default"

@export_range(0, 100)
var hp: int = 100

@export_group("Combat")
@export var damage: float = 10.5

@onready var label: Label = %Label

var values_non_static: Array[String] = ["one", "two"]
static var static_state := State.IDLE

var count: int:
    get:
        return count
    set(v):
        count = clampi(v, 0, 100)


func strings_incl_formatting() -> void:
    var formatted_percent := "Player: %s HP: %d/%d (%.1f%%)" % [name, hp, 100, 99.9]
    var formatted_brackets_num := "Player: {0} HP: {1}/{2} ({3:.1f}%)".format([name, hp, 100, 99.9])
    var formatted_brackets_name := "Player: {name} HP: {hp}/{max_hp} ({percent:.1f}%)".format(
        { "name": name, "hp": hp, "max_hp": 100, "percent": 99.9 }
    )
    var escaped := "Hello\nWorld"
    var raw := r"C:\path\to\file"
    var str_name := &"String"
    var multi := """
Multi
line
string"""
    print(
        "\n".join(
            [
                formatted_percent,
                formatted_brackets_num,
                formatted_brackets_name,
                escaped,
                str_name,
                raw,
                multi,
            ]
        )
    )


func conditions() -> void:
    var result := count if "one" in values_non_static else -count
    print(result)

    var is_member := 1 in values_non_static
    if true is not bool and count >= 0 or is_member:
        print("ok")
    elif false:
        pass
    else:
        return

    match static_state:
        State.IDLE | 0:
            static_state = State.RUNNING
        _:
            pass

    var truth := false
    assert(truth != true)


func loops() -> void:
    for item: String in values_non_static:
        continue

    while len(values_non_static) < 10:
        break


func get_path_nested(val: NodePath) -> NodePath:
    return val


func nodes_and_paths() -> void:
    var node_path := ^"Label"
    var node_path_manual := NodePath("Label")
    var node_lu := get_node(node_path)
    var node_lu2 := get_node(get_path_nested(node_path_manual))
    var node_lu3 := get_node("%Label/%Child:prop")
    var node := $"../CanvasLayer/Label/%Child:prop"
    var node_bare := $CanvasLayer
    var node_bare_multi := $CanvasLayer/Label
    var node_bare_unique := %Label
    var node_bare_unique2 := $%Label
    var node_bare_nested := %Label/%Child

    if (
        node_path
        and node_lu.can_process()
        and node_lu2.can_process()
        and node_lu3.can_process()
        and node.can_process()
        and node_bare.can_process()
        and node_bare_multi.can_process()
        and node_bare_unique.can_process()
        and node_bare_unique2.can_process()
        and node_bare_nested.can_process()
    ):
        print("Yay")


func callables_and_signals() -> void:
    var callable := func(x: int = 1) -> int:
        var num := int(1.0)
        return x * num * 2.0 as int

    count = await callable.call(21)

    emit_signal(&"changed", count)
    emit_signal(&"ping")

    queue_free()


func _input(event: InputEvent) -> void:
    if event.is_action_pressed("jump"):
        create()


static func create() -> SyntaxTesting:
    return SyntaxTesting.new()
