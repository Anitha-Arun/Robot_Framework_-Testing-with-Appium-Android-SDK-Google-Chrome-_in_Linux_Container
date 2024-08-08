FROM ubuntu:20.04

# Suppress interaction with the package manager
ENV DEBIAN_FRONTEND=noninteractive

# Update packages and install necessary tools
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    tar \
    gzip \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    fonts-liberation \
    xdg-utils \
    curl \
    net-tools \
    iputils-ping \
    telnet \
    grep \
    psmisc \
    software-properties-common \
    gnupg2 \
    procps \
    lsof \
    openjdk-11-jdk \
    python3.8 \
    python3.8-distutils \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and Appium
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g appium@1.22.3 --unsafe-perm=true && \
    npm install -g @appium/doctor

# Install optional dependencies
RUN apt-get update && apt-get install -y ffmpeg gstreamer1.0-tools && rm -rf /var/lib/apt/lists/*

# Install Google Chrome and ChromeDriver
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Set up Android SDK
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/latest

RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O android-sdk.zip && \
    unzip -o android-sdk.zip -d ${ANDROID_HOME}/cmdline-tools && \
    mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/latest && \
    rm android-sdk.zip && \
    wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip && \
    unzip -o platform-tools-latest-linux.zip -d ${ANDROID_HOME} && \
    rm platform-tools-latest-linux.zip

# Install Build Tools and SDK Packages
RUN yes | ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager --licenses --sdk_root=${ANDROID_HOME} && \
    ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager "platform-tools" "build-tools;30.0.3" "emulator" --verbose

# Verify Build Tools Installation
RUN ls -l ${ANDROID_HOME}/build-tools/30.0.3 && \
    ls -l ${ANDROID_HOME}/cmdline-tools/latest/bin

# Set PYTHONPATH
ENV PYTHONPATH=/app/PartnerDevices_Automation/Libraries:/app/PartnerDevices_Automation/resources/keywords:/app/PartnerDevices_Automation:/usr/lib/python3.8

# Install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Ensure these commands are in the system PATH
ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /app

CMD ["/bin/bash"]
