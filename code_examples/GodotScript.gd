# Comment

@tool
@icon("res://icon.svg")
class_name SyntaxTesting
extends CharacterBody2D

signal changed(value: int)

enum State {
    IDLE,
    RUNNING,
}

## Doc comment
const PI2 := PI * 2.0
const DATA := { "key": [1, 2, 3], &"name": null }

@export
var name_: String = "Default"

@export_range(0, 100)
var hp: int = 100

@export_group("Combat")
@export
var damage: float = 10.5

@onready var label: Label = %Label

var values_static: Array[String] = ["one", "two"]
static var static_state := State.IDLE

var count: int:
    get:
        return count
    set(v):
        count = clampi(v, 0, 100)


func _ready() -> void:
    var text := "Hello\nWorld"
    var path := $"CanvasLayer/Label"
    var node := %Label
    if path.can_process() and node.can_process():
        print("Yay")

    var callable := func(x: int = 1) -> int:
        return x * 2
    var truth := false

    assert(truth != true)

    if true is not bool and count >= 0:
        print(text)
    else:
        pass

    for item: String in values_static:
        continue

    while null:
        break

    match static_state:
        State.IDLE | 0:
            static_state = State.RUNNING
        _:
            pass

    count = await callable.call(21)
    emit_signal(&"changed", count)

    var result := count if count >= 0 else -count
    print(result)

    print(
        """
        Multiline
        string
    """
    )

    queue_free()


func _input(event: InputEvent) -> void:
    if event.is_action_pressed("jump"):
        create()


static func create() -> SyntaxTesting:
    return SyntaxTesting.new()


class InnerHelper extends SyntaxTesting:
    var value: int = 0


    func _ready() -> void:
        await super()
        self.value = 1


    static func double(val: int) -> int:
        return val * 2


func format_test() -> void:
    var s := "Player: %s HP: %d/%d (%.1f%%)" % [name, hp, 100, 99.9]
    var raw := r"C:\path\to\file"
    var multi := """
Multi
line
string"""
    print(s, "\n", raw, "\n", multi)
