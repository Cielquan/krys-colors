# Comment

@tool
@icon("res://icon.svg")
class_name SyntaxTest
extends Node

signal changed(value: int)

enum State {
	IDLE,
	RUNNING,
}

## Doc comment
const PI2 := PI * 2.0
const DATA := { "key": [1, 2, 3], &"name": null }

@export
var name: String = "Default"

@export_range(0, 100)
var hp: int = 100

@export_group("Combat")
@export
var damage: float = 10.5

@onready var label: Label = %Label

var values: Array[String] = ["one", "two"]
static var _state := State.IDLE

var value: int:
	get:
		return count
	set(v):
		count = clampi(v, 0, 100)


func _ready() -> void:
	var text := "Hello\nWorld"
	var path := $"CanvasLayer/Label"
	var node := %Label
	var callable := func(x: int = 1) -> int:
		return x * 2

	if true and count >= 0:
		print(text)
	else:
		pass

	for item: String in values:
		continue

	while null:
		break

	match state:
		State.IDLE | 0:
			state = State.RUNNING
		_:
			pass

	count = await callable.call(21)
	emit_signal(&"changed", count)

	var result := count if count >= 0 else -count

	print(
		"""
        Multiline
        string
    """
	)

	queue_free()


func _input(event: InputEvent) -> void:
	if event.is_action_pressed("jump"):
		_jump()


static func create() -> MyNode:
	return MyNode.new()


class InnerHelper:
	var value: int = 0


	func double() -> int:
		return value * 2


func format_test() -> void:
	var s := "Player: %s HP: %d/%d (%.1f%%)" % [name, hp, 100, 99.9]
	var raw := r"C:\path\to\file"
	var multi := """
Multi
line
string"""
	print(s, "\n", raw, "\n", multi)
