# TRANSLATOR

TRANSLATOR is an API for translating text, subtitles in SRT format, and SRT files.

## Table of Contents
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Running The Application](#running-the-application)
- [Running with Docker](#running-with-docker)
- [Documentation](#documentation)
- [Technologies Used](#technologies-used)
- [License](#license)


## Getting Started

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/your-repository/translator.git
cd translator
```
### Step 2: Set Up Environment Variables
Create a .env file by copying the contents from the .env.example:

```bash
cp .env.example .env
```
Fill in the necessary environment variables in the .env file.

### Step 3: Install ffmpeg
To use the ffmpeg functionality, you need to install ffmpeg on your machine.

#### For macOS: Use Homebrew:
```bash
brew install ffmpeg
```

#### For Ubuntu/Debian: Use APT:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### For Windows:
You can download a build from [FFmpeg's official website](https://ffmpeg.org/download.html) and follow the installation instructions.


### Step 4: Set Up a Virtual Environment
To create a virtual environment, run the following commands:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### Step 5: Install Dependencies
Once the virtual environment is activated, install the project dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

To run the tests using pytest, ensure your virtual environment is activated, then execute the following command:

```bash
pytest
```

This will discover and run all tests in the project.

## Running the Application
To run the application normally (without Docker), use the following command:

```bash
python main.py
```
Make sure your environment variables are set and your virtual environment is activated before running this command.

## Running with Docker
To deploy the project in Docker, run the following command:

```bash
docker-compose up --build
```
This command will build the containers and start the API.

### Stopping the Docker Container
To stop the container, use the command:
```bash
docker-compose stop translator
```

## Documentation
API documentation will be available at [127.0.0.1:80/docs](http://127.0.0.1:80/docs)

## Technologies Used
The project is built using the following technologies:

* `Python 3.10+`
* `FastAPI`
* `Docker`
* `pytest`
* `ffmpeg`

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.