Mobile Automation Testing with Appium, Android SDK, Google Chrome, and Continuous Integration (CI) Pipelines
This repository provides a Dockerfile to build a fully automated environment for mobile application testing using Appium, Android SDK, and Google Chrome. The setup is optimized for both manual and CI-based mobile testing, running in a Linux-based container. This allows easy scaling for testing across multiple devices, emulators, or web environments.

Features:
Dockerized Testing Environment: The environment is fully containerized, meaning you can run the entire setup on any system that supports Docker. This makes the setup process quick, reproducible, and portable.

Appium: Installs Appium 1.22.3, an open-source mobile application automation tool. Appium is configured for both Android and iOS mobile testing.

Android SDK: Installs Android SDK tools, platform-tools, and build-tools, allowing for seamless Android application testing and device management.

Google Chrome & ChromeDriver: Google Chrome and ChromeDriver are installed for web automation with Appium, ensuring compatibility with mobile web testing.

Node.js & NPM: Installs Node.js 22.5.1 and NPM, required to run Appium and install additional packages or dependencies as needed.

Python 3.8: Installs Python 3.8 and required dependencies from the requirements.txt to run Python-based automation scripts.

Automated Resource Setup: The Dockerfile creates symbolic links to necessary resources like Page Objects for automation. It also sets up the PYTHONPATH for easy integration with the automation scripts.

Linux Container Setup: The entire system is configured to run in a Linux container (Ubuntu 20.04), providing a lightweight, efficient environment for running your tests.

CI/CD Pipelines: This setup integrates seamlessly with CI/CD pipelines, making it easy to run your mobile tests automatically on every commit or pull request. The pipelines can be configured using services like GitHub Actions, Jenkins, or any other CI tool to trigger the tests on connected devices or emulators.

CI/CD Pipeline Integration:
To support automated testing and continuous integration, the repository can be easily connected to your CI/CD pipelines to run mobile tests automatically upon code commits, pull requests, or other triggers.

Pipeline Integration: The containerized setup works well with modern CI/CD tools. Using services like GitHub Actions, Jenkins, or GitLab CI, you can automate your mobile testing by:

Triggering tests on every commit.
Running tests in parallel on multiple devices or emulators.
Automatically installing and configuring Appium, Android SDK, Google Chrome, and any required dependencies.
Linux-based Containerized Environment: Since the setup is containerized in a Linux-based environment (Ubuntu 20.04), it works seamlessly with Linux-based CI servers, ensuring consistent behavior across environments and minimizing "works on my machine" issues.

Run Tests in Parallel: By integrating the setup with your CI pipeline, you can run tests across multiple devices/emulators simultaneously, speeding up your testing process and enabling efficient feedback loops.
How to Build and Use the Docker Image:
Clone the repository:

bash
Copy
git clone https://github.com/your-username/appium-android-sdk-docker.git
cd appium-android-sdk-docker
Build the Docker image:

bash
Copy
docker build -t appium-android-sdk .
Run the container:

bash
Copy
docker run -it appium-android-sdk
This will start a container with the testing environment set up. You can now run your Appium tests from within the container.

Use the container for testing:

Connect your Android device or emulator.
Run your Appium test scripts or use Python-based automation scripts.
CI/CD Pipeline Example with GitHub Actions:
To integrate this setup with a GitHub Actions pipeline for running tests on every push, you can create a .github/workflows/test.yml file with the following example configuration:

yaml
Copy
name: Run Mobile Tests

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Docker environment
      run: |
        docker build -t appium-android-sdk .
        docker run -it appium-android-sdk

    - name: Run mobile tests
      run: |
        # Commands to run your Appium tests or automation scripts
        python3 -m unittest discover -s tests/
This workflow automatically builds the Docker image and runs your tests when changes are pushed to the main branch or on pull requests.

Dependencies:
Appium 1.22.3
Node.js (22.5.1)
Python 3.8
Android SDK
Google Chrome & ChromeDriver
This is a Python script written and maintained by Anitha.Damarla.
