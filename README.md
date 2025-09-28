# Hand Fighter

This is a simple reaction game built with `Pygame`.

The game prompts the user to show some gesture within a limited time. If the user show the correct gesture within the time limit, they pass the level and the final score is displayed at the end.

The original game is developed in Raspberry Pi, the game need to be refactor in windows.

## Install required library

```
pip install -r requirements.txt
```

## Game Level

- To Design your own level, you can edit the `config.py`

```
["prompt", pop-up timing]
```

- Gesture:
  | Prompt | Gesture |
  |------|------|
  | sword | scissors |
  | fist | rock |
  | shield | paper |

You can design your own level in a list:

```
//Example

Level2Recipe = [["sword", 4], ["fist", 6], ["fist", 7.4], ["fist", 9], ["sword", 10.4], ["sword", 12.8], ["sword", 14.8], ["fist", 16.4], ["sword", 18], ["fist", 20],["fist", 22],["sword", 24],["sword", 26],["sword", 28] ]
```

---

## Gesture Monitoring Model

- We use the model `mediapipe` to detect the gesture.
- `mediapipe` include multiple pretrained model, and we use the hand-gesture model, which use the pixel coordinates to locate the nodes of a hand (x and y coordinates only).

## Development Progress

TODO:

- The basic game logic is implemented
- `score.py`: save the best record of player
- Optimization in fluency is required. (thread / process improvment)
- Game Art Resources Improvment
