# GestureTunes

GestureTunes is a Python project that tracks the user's hands using the OpenCV library and creates music based on the number of fingers detected on each hand. The project uses two different instruments: a sitar sound for the left hand and a piano sound for the right hand. If only one hand is detected, the instrument used will depend on the position of the hand on the screen. If the hand is on the left side of the screen, the sitar sound will be used, and if the hand is on the right side, the piano sound will be used.

## Installation

To install GestureTunes, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Run the following command in your terminal: `pip install -r requirements.txt`

## Usage

1. Navigate to the project directory.
2. Run the following command in your terminal: `python main.py`
3. Once the script is running, you should see a message like this: `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`
4. Open your web browser and go to the URL displayed in the message.
5. Place your hand in front of the camera to hear the musical notes corresponding to the fingercounts.

## Libraries Used

GestureTunes uses the following libraries:

- Flask
- OpenCV
- Pygame

## Contributing

Contributions are always welcome! If you have any suggestions or find any bugs, please create a new issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
