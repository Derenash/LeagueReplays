# League Replay Stats Analyzer

This Python application processes `.rofl` replay files from League of Legends matches, extracts relevant statistical data, and displays it in a web interface.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed Python 3.6 or above.
* You have installed Flask. You can install Flask using `pip install flask`.
* (Include other dependencies or setup requirements here if applicable.)

## Installation

To install the application, follow these steps:

1. Clone the repository to your local machine or download the ZIP file and extract it.
2. Navigate to the application directory.

## Usage

To use the application, follow these steps:

1. Place your `.rofl` replay files into the `replays` directory.
2. Run `main.py` using the command:
```python main.py```

This will process the replay files and start the Flask web server.
3. Open your web browser and go to `http://localhost:5000`. You should see the web interface with the statistics displayed in a table format.

## Features

* Processes `.rofl` files to extract game statistics.
* Displays statistics in an interactive web interface.
* Calculates and displays metrics such as CSPM, GDPM, DPM, KDA, KP%, and vision score.
