from typing import TypedDict, List

class UwuLevel(TypedDict):
  stutter_chance: float
  face_chance: float
  action_chance: float
  exclamation_chance: float
  nsfw_actions: bool

levels: List[UwuLevel] = [
  {
    "stutter_chance": 0.1,
    "face_chance": 0.05,
    "action_chance": 0.1,
    "exclamation_chance": 0.5,
    "nsfw_actions": False,
  },
  {
    "stutter_chance": 0.3,
    "face_chance": 0.2,
    "action_chance": 0.3,
    "exclamation_chance": 0.8,
    "nsfw_actions": False,
  },
    {
    "stutter_chance": 0.3,
    "face_chance": 0.2,
    "action_chance": 0.3,
    "exclamation_chance": 0.8,
    "nsfw_actions": True,
  },
  {
    "stutter_chance": 0.5,
    "face_chance": 0.4,
    "action_chance": 0.5,
    "exclamation_chance": 1,
    "nsfw_actions": True,
  },
  {
    "stutter_chance": 1,
    "face_chance": 1,
    "action_chance": 1,
    "exclamation_chance": 1,
    "nsfw_actions": True,
  },
]
  