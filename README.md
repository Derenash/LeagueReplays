# League Replay Stats Analyzer

The League Replay Stats Analyzer is a Python application that processes `.rofl` replay files from League of Legends matches, extracts relevant statistical data, and displays it in a user-friendly web interface. It provides valuable insights into player performance and game metrics.

## Features

- Processes `.rofl` files to extract game statistics
- Displays statistics in an interactive web interface
- Calculates and displays metrics such as CSPM (Creep Score per Minute), GDPM (Gold per Minute), DPM (Damage per Minute), KDA (Kill/Death/Assist Ratio), KP% (Kill Participation Percentage), and Vision Score
- Supports player alias configuration for accurate tracking and comparison of player statistics

## Prerequisites

Before running the application, ensure you have the following:

- Python 3.6 or above installed
- Flask installed (`pip install flask`)

## Installation

To install the League Replay Stats Analyzer, follow these steps:

1. Clone the repository to your local machine or download the ZIP file and extract it.
2. Navigate to the application directory.

## Usage

To use the League Replay Stats Analyzer, follow these steps:

1. Place your `.rofl` replay files into the `replays` directory.

2. Configure player aliases (optional but recommended):
   - For accurate tracking and comparison of player statistics, it's essential to configure player aliases, especially when players use multiple in-game names.
   - Locate the `info` directory within the application folder.
   - Open or create a file named `players.json`.
   - Edit the file to include a list of player aliases in the following format:

     ```json
     {
       "John": [
         "JohnMainAccount",
         "JohnFakeAccount",
         "JohnThirdAccount"
       ],
       "James": [
         "Darksider23"
       ]
     }
     ```

3. Run the application:
   - Open a terminal or command prompt.
   - Navigate to the application directory.
   - Run the following command:

     ```
     python main.py
     ```

   - This will process the replay files and start the Flask web server.

4. Access the web interface:
   - Open your web browser.
   - Go to `http://localhost:5000`.
   - You should see the web interface with the statistics displayed in a table format.
