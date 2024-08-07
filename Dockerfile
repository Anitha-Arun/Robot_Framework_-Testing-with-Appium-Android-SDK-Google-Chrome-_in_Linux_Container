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
    openjdk-11-jdk \
    python3.8 \
    python3.8-distutils \
    python3-pip \
    curl \
    net-tools \
    iputils-ping \
    grep \
    psmisc \
    software-properties-common \
    gnupg2 \
    procps \
    lsof \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22.5.1 from the provided tarball
COPY node-v22.5.1-linux-x64.tar.xz /tmp/
RUN tar -xf /tmp/node-v22.5.1-linux-x64.tar.xz -C /usr/local --strip-components=1 && \
    rm /tmp/node-v22.5.1-linux-x64.tar.xz

# Set Node.js path
ENV PATH=/usr/local/bin:$PATH

# Install Appium globally with unsafe-perm flag
RUN npm install -g appium@1.22.3 --unsafe-perm=true

# Install appium-doctor
RUN npm install -g @appium/doctor

# Install optional dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gstreamer1.0-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome from local .deb file
COPY google-chrome-stable_current_amd64.deb /tmp/google-chrome.deb
RUN dpkg -i /tmp/google-chrome.deb || apt-get install -f -y \
    && rm /tmp/google-chrome.deb

# Install ChromeDriver from provided ZIP file
COPY chromedriver-linux64.zip /tmp/chromedriver.zip
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver-linux64/chromedriver \
    && ln -s /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

# Set up Android SDK
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/latest

# Install Android SDK command line tools and platform-tools
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O android-sdk.zip && \
    unzip -o android-sdk.zip -d ${ANDROID_HOME}/cmdline-tools && \
    mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/latest && \
    rm android-sdk.zip

RUN wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip && \
    unzip -o platform-tools-latest-linux.zip -d ${ANDROID_HOME} && \
    rm platform-tools-latest-linux.zip

# Accept licenses and install platform-tools, build-tools, and emulator
RUN yes | ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager --licenses --sdk_root=${ANDROID_HOME} --verbose && \
    ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager "platform-tools" "build-tools;30.0.3" "emulator" --sdk_root=${ANDROID_HOME} --verbose

# Verify Android SDK installation
RUN ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager --list --sdk_root=${ANDROID_HOME}
RUN if [ -f "${ANDROID_HOME}/platform-tools/adb" ]; then \
        ${ANDROID_HOME}/platform-tools/adb --version; \
    else \
        echo "ADB not found"; \
        exit 1; \
    fi



# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set PYTHONPATH to include necessary directories
ENV PYTHONPATH=/app/PartnerDevices_Automation/Libraries:/app/PartnerDevices_Automation/resources/keywords:/app/PartnerDevices_Automation:/usr/lib/python3.8

# Copy the requirements file and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


# Ensure these commands are in the system PATH
ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /app

# Run the startup script
CMD ["/bin/bash"]
