# Chess2

Chess2 is a chess game developed using `pygame-ce`, a fork of `pygame`. This project is licensed under the MIT license.

# Requirements

* Python 3.9 or higher (3.10+ recommended)
* `pygame-ce` library version 2.1.3 or higher
* Stockfish binaries (need to be downloaded manually for AI functionality)
* `stockfish` library version 3 or higher
* `chess` library version 1.9 or higher

# Installation

Follow these steps to install pygame-ce and run the Chess2 project:

1. Uninstall `pygame` (if already installed):
    ```shell
    pip uninstall pygame
    ```

2. Install requirements:
    ```shell
    pip install pygame-ce, chess, stockfish
    ```

3. Clone this repository:
    ```shell
    git clone https://github.com/mmdmoa/Chess2.git
    ```

4. Navigate to the project directory: 
    ```shell
    cd Chess2
    ```
5. Download the Stockfish binaries from the official website (https://stockfishchess.org/). Make sure to choose the appropriate version for your operating system.

6. Change the StockfishPath variable:
    * Open the assets.py file located in the core directory of the Chess2 project.
    * Locate the StockfishPath variable and replace it with the path to the downloaded Stockfish binaries on your system.
    * Save the file.

7. Run the Chess2 game:
    ```shell
    python main.py
    ```
### Attention
Please note that the AI functionality requires the Stockfish binaries to 
be manually downloaded and the `StockfishPath` variable in `assets.py` to be updated with the correct path.
Even without the AI, the game will still run perfectly, providing a complete chess game experience.

# Android Version

An Android version of this project is planned for the future. Buildozer will be used to develop the Android version.
# Contributing

Contributions to this project are welcome. Feel free to open issues and pull requests on the GitHub repository.
# License

This project is licensed under the terms of the MIT license. Please see the LICENSE file for more information.

# Credits

pygame-ce (https://github.com/pygame-community/pygame-ce) for providing the framework used in this project
Stockfish (https://stockfishchess.org/) for providing the chess engine used in this project (manual download required for AI functionality